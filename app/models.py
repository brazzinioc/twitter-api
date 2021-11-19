# Python
from uuid import UUID, uuid4
from datetime import date
from datetime import datetime
from typing import Optional, Dict, List

# Pydantic
from pydantic import BaseModel, EmailStr, Field


# USER
class User(BaseModel):

    id: UUID = Field(
        default_factory=uuid4,
        unique=True,
        title="Id",
        description="The unique identifier for the user.",
        )

    email: EmailStr = Field(
        ...,
        unique=True,
        title="Email",
        description="The email address of the user.",
        )

    first_name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        title="First Name",
        description="The first name of the user.",
        )

    last_name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        title="Last Name",
        description="The last name of the user.",
        )

    born_date: Optional[date] = Field(
        default=None,
        title="Born Date",
        description="The date of birth of the user.",
        )

    created_at: datetime = Field(
        default=datetime.now(),
        title="Created At",
        description="The date and time when the user was created.",
        )

    updated_at: Optional[datetime] = Field(
        default=None,
        title="Updated At",
        description="The date and time when the user was updated.",
        )
    
    deleted_at: Optional[datetime] = Field(
        default=None,
        title="Deleted At",
        description="The date and time when the user was deleted.",
        )

    class Config:
        schema_extra = {
            "example": {
                "email": "my_email@domain.com",
                "first_name": "Jhon",
                "last_name": "Doe",
                "born_date": "2020-01-01",
            }
        }



class UserIn(User):
    # Used to create a new user
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=30, 
        title="Password",
        description="The password of the user.",
        )

    class Config:
        schema_extra = {
            "example": {
                "email": "my_email@domain.com",
                "password": "myp@ss159753",
                "first_name": "Jhon",
                "last_name": "Doe",
                "born_date": "2020-01-01",
            }
        }



class UserOut(User):
    # Used to return a user
    pass




# TWEET
class Tweet(BaseModel):

    id: UUID = Field(
        default_factory=uuid4,
        unique=True,
        title="Id",
        description="The unique identifier for the tweet.",
        )

    content: str = Field(
        ...,
        min_length=1,
        max_length=280,
        title="Content",
        description="The content of the tweet.",
        )

    created_by: UUID = Field(
        ...,
        title="Created By",
        description="The user who created the tweet.",
        )

    created_at: datetime = Field(
        default=datetime.now(),
        title="Created At",
        description="The date and time when the tweet was created.",
        )

    updated_at: Optional[datetime] = Field(
        default=None,
        title="Updated At",
        description="The date and time when the tweet was updated.",
        )
    
    deleted_at: Optional[datetime] = Field(
        default=None,
        title="Deleted At",
        description="The date and time when the tweet was deleted.",
        )


    class Config:
        schema_extra = {
            "example": {
                "content": "This is my first tweet",
                "created_by": "5e9f8f8f-e9b1-4b7b-b8b1-f9f9f9f9f9f9",
            }
        }
