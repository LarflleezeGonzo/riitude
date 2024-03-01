from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int


class ReviewCreate(BaseModel):
    text: str
    rating: int