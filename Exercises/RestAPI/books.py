# Based on course under link:
# https://www.youtube.com/watch?v=MCVcAAoDJS8

from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

all_titles = []

@app.get("/")
def read_api():
    return all_titles

@app.post("/")
def create_book(book: Book):
    all_titles.append(book)
    return book     # zwróci jeśli się uda, po to, żeby user wiedział co dodał

