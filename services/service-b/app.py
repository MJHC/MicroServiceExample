from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine(os.environ["DB_CONN"])
Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    publication_year = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)

    author: Mapped[Author] = relationship("Author", back_populates="books")

Session = sessionmaker(bind=engine)
db = Session()
app = FastAPI()

@app.get("/")
async def b():

    books = db.query(Book).all()
    return {
        "message": "Hello from service B",
        "books": [{"title":b.title, "author": b.author.first_name} for b in books]
        }