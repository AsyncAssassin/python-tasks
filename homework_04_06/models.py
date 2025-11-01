from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List


class Book(BaseModel):
    title: str
    author: str
    year: int = Field(ge=1000, le=2100)
    available: bool = True
    categories: List[str] = []

    @field_validator('categories')
    @classmethod
    def normalize_categories(cls, v):
        if not v:
            return []
        return list(set(cat.lower().strip() for cat in v if cat.strip()))


class User(BaseModel):
    name: str
    email: EmailStr
    membership_id: str


class Library(BaseModel):
    books: List[Book] = []
    users: List[User] = []

    def total_books(self):
        return len(self.books)

    def available_books(self):
        return sum(1 for book in self.books if book.available)