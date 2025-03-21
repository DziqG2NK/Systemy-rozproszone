# Based on course under link:
# https://www.youtube.com/watch?v=MCVcAAoDJS8

from fastapi import FastAPI, HTTPException
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

@app.put("/{book_id}")
def update_book(book_id: UUID, book: Book):
    cnt = 0

    for book_p in all_titles:
        cnt += 1
        if book_p.id == book_id:
            all_titles[cnt - 1] = book
            return all_titles[cnt - 1]
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} : does not exist"
    )

@app.delete("/{book_id}")
def delete_book(book_id: UUID):

    for i, book in enumerate(all_titles):
        if book.id == book_id:
            del all_titles[i]
            return f"ID {book_id} : deleted"
    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} : does not exist"
    )
