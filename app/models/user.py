from sqlmodel import SQLModel, Field
from typing import Optional
from app.helper.enums import RoleEnum


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: RoleEnum
