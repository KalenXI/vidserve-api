from typing import Optional, List, Dict
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field
import shortuuid


class User(BaseModel):
    uid: str = None,
    permissions: List = [],
    name: str = None

    class Config:
        allow_population_by_field_Name = True
        schema_extra = {
            "example": {
                "uid": "000000",
                "name": "John Doe",
                "permissions": {
                    "none"
                }
            }
        }
