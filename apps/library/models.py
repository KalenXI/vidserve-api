from __future__ import annotations

from typing import Optional, List, Dict
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field
import shortuuid


class LibraryModel(BaseModel):
    id: str = Field(default_factory=shortuuid.uuid, alias="_id")
    name: str
    private: bool = False
    unlisted: bool = False
    password: Optional[str]
    children: Optional[List[str]]

    class Config:
        allow_population_by_field_Name = True
        schema_extra = {
            "example": {
                "_id": "test_library",
                "name": "Test Library",
                "private": "False",
                "unlisted": "False",
                "password": "mysecret",
                "children": {
                    "Subfolder"
                }
            }
        }


class UpdateLibraryModel(BaseModel):
    name: Optional[str]
    private: Optional[bool] = False
    password: Optional[str]
    children: Optional[List[str]]

    class Config:
        allow_population_by_field_Name = True
        schema_extra = {
            "example": {
                "name": "Test Library",
                "private": "True",
                "password": "mysecret",
                "children": []
            }
        }
