from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from typing import TypeVar, Type
from enum import Enum
import os

T = TypeVar('T')

class ResponseType(Enum):
    DICT = 0
    LIST = 1
    PRIM = 2


class Service:
    def __init__(self, dest: str):
        self.dest = dest
        self.__types = {
            ResponseType.DICT: lambda m, x: m(**x),
            ResponseType.LIST: lambda m, x: m(*x),
            ResponseType.PRIM: lambda m, x: m(x)
        }

    async def request(self, 
                      method: str,
                      endpoint: str,
                      res_model: Type[T],
                      res_type: ResponseType=ResponseType.DICT,
                      data: str = None,
                      ) -> T:
        async with httpx.AsyncClient() as client:
            req = client.build_request(method, self.dest + endpoint, data=data)
            res = (await asyncio.gather(client.send(req)))[0]
            
            if res.status_code in range(400, 599):
                err: dict = res.json()
                detail = err.get("detail", None)
                if detail is None:
                    detail = err.get("title", "Error")
                raise HTTPException(
                    status_code=res.status_code, 
                    detail=detail
                    )
            return self.__types[res_type](res_model, res.json())

app = FastAPI()
app.add_middleware(
            CORSMiddleware,
            allow_origins=[os.environ["CLIENT"]],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

s_a = Service(os.environ["SERVICE_A"])
s_b = Service(os.environ["SERVICE_B"])

@app.get("/")
async def home():
    return {"message": "APIGateway"}

@app.get("/ab")
async def service_a_b():
    res = await s_a.request("get", "/ab", dict)
    return res

@app.get("/a")
async def service_a():
    res = await s_a.request("get", "/", dict)
    return res

@app.get("/b")
async def service_b():
    res = await s_b.request("get", "/", dict)
    return res

