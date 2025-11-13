from typing import Optional
from pydantic import BaseModel, Field


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    body: str
    userId: int = Field(alias="userId")

    class Config:
        populate_by_name = True


class Comment(BaseModel):
    id: Optional[int] = None
    postId: int
    name: str
    email: str
    body: str


class Album(BaseModel):
    id: Optional[int] = None
    title: str
    userId: int


class Photo(BaseModel):
    id: Optional[int] = None
    albumId: int
    title: str
    url: str
    thumbnailUrl: str


class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool
    userId: int


class Address(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: dict


class Company(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class User(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company