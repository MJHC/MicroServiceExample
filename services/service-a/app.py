from fastapi import FastAPI, HTTPException
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
        self.__dest = dest
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
            req = client.build_request(method, self.__dest + endpoint, data=data)
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

s_b = Service(os.environ["SERVICE_B"])

@app.get("/")
async def a():
    return {"message": "Hello from service A"}

@app.get("/ab")
async def ab():
    res = await s_b.request("get", "/", dict)
    return {"messages":[
        res,
        {"message": "Hello from service A"}
    ], "message": "Aggregated"}