from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# base schema for user
class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=160)


# why separate: later for authentication we may add fields like password etc
class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=120)
    image_file: str | None = Field(default=None, min_length=1, max_length=200)


# api responses have more fields than creation requests (like id, generated values etc)
class UserResponse(UserBase):
    model_config = ConfigDict(
        from_attributes=True
    )  # using this, pydantic can read object attr (user.id etc) not only dict

    id: int
    image_file: str | None
    image_path: str


# base schema for posts
class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: int  # ideally the authenticated user


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)  # orm object conversion

    id: int
    user_id: int
    date_posted: datetime
    author: (
        UserResponse  # it's nested seralization, api return the complete author details
    )
