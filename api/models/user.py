from pydantic import BaseModel


class User(BaseModel):
    id: int | None
    email: str


class UserIn(BaseModel):
    password: str
