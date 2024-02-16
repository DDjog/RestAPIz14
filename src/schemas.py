from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr

"""
Schemas (schemas.py) module contains
definition of type data used to describe data for FastAPI/REST 
"""


class ContactBase(BaseModel):
    firstname: str = Field(max_length=50)

    secondname: str = Field(max_length=50)

    email: str = Field(max_length=50)

    telephone: int

    birthday: date | None


class ContactNotes(ContactBase):
    """

    """
    notes: str | None


class ContactResponse(ContactBase):
    """

    """
    id: int
    user_id: int

    class Config:
        orm_mode = True


class ContactNotesResponse(ContactBase):
    """

    """

    id: int
    user_id: int

    notes: str | None

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    """

    """

    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """

    """

    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """

    """

    user: UserDb
    """ user field """

    detail: str = "User successfully created"
    """ detail """


class TokenModel(BaseModel):
    """

    """

    access_token: str
    """ """

    refresh_token: str
    """ """

    token_type: str = "bearer"
    """ """


class RequestEmail(BaseModel):
    email: EmailStr

