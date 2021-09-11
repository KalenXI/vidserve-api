from typing import Optional, List, Dict
from datetime import datetime, time, date
import uuid
from pydantic import BaseModel, Field
import shortuuid


class VideoFile(BaseModel):
    name: str
    size: str
    resolution: str
    type: str
    url: str


class VideoModel(BaseModel):
    id: str = Field(default_factory=shortuuid.uuid, alias="_id")
    title: str = None
    description: Optional[str] = None
    url: str = None
    uploaded_date: datetime
    recorded_date: Optional[date] = None
    duration: time = None
    files: Optional[List[VideoFile]]
    categories: Optional[List[str]] = None
    unlisted: bool = True
    password: Optional[str] = None

    class Config:
        allow_population_by_field_Name = True
        schema_extra = {
            "example": {
                "title": "Example Video",
                "description": "This is an example of a video description.",
                "url": "testvideo.m3u8",
                "uploaded_date": "2020-01-01T12:00:00",
                "recorded_date": "2016-01-02",
                "duration": "00:01:00",
                "files": [
                    {
                        "name": "HD 1080p",
                        "size": "11GB",
                        "resolution": "1920x1080",
                        "type": "MP4",
                        "url": "/files/test.mp4"
                    }
                ],
                "categories": {
                    "theatre",
                    "musical",
                    "1996"
                },
                "unlisted": "False",
            }
        }


class UpdateTaskModel(BaseModel):
    name: Optional[str]
    completed: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "name": "My important task",
                "completed": True,
            }
        }
