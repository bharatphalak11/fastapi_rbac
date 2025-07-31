from typing import Optional
from pydantic import BaseModel, model_validator
from app.helper.enums import RoleEnum


class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdateRequest(BaseModel):
    role: Optional[RoleEnum] = None

    # Password fields
    last_password: Optional[str] = None
    new_password: Optional[str] = None
    confirm_password: Optional[str] = None

    @model_validator(mode="after")
    def validate_passwords(cls, model):
        if model.new_password or model.confirm_password:

            if model.new_password != model.confirm_password:
                raise ValueError("New password and confirm password do not match")

        return model