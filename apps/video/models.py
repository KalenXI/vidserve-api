from typing import Optional, List, Dict
from datetime import datetime, timezone
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
    recorded_date: Optional[datetime] = None
    duration: int = None
    files: Optional[List[VideoFile]]
    categories: Optional[List[str]] = None
    libraries: Optional[List[str]] = None
    unlisted: bool = False
    private: bool = False
    password: Optional[str] = None

    class Config:
        allow_population_by_field_Name = True
        schema_extra = {
            "example": {
                "title": "Example Video",
                "description": "This is an example of a video description.",
                "url": "testvideo.m3u8",
                "uploaded_date": "2020-01-01T12:00:00Z",
                "recorded_date": "2016-01-02T00:00:00Z",
                "duration": 3600,
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
                "libraries": {
                    "patapsco/music"
                },
                "unlisted": "False",
                "private": "False",
            }
        }


class UpdateVideoModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    uploaded_date: Optional[datetime]
    recorded_date: Optional[datetime] = None
    duration: Optional[int] = None
    files: Optional[List[VideoFile]]
    categories: Optional[List[str]] = None
    library: Optional[List[str]] = None
    unlisted: Optional[bool] = False
    private: Optional[bool] = False
    password: Optional[str] = None

    class Config:
        allow_population_by_field_Name = True
        schema_extra = {
            "example": {
                "title": "Example Video",
                "description": "This is an example of a video description.",
                "url": "testvideo.m3u8",
                "uploaded_date": "2020-01-01T12:00:00",
                "recorded_date": "2016-01-02T00:00:00",
                "duration": 3600,
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
                "libraries": {
                    "patapsco/music"
                },
                "unlisted": "False",
            }
        }
