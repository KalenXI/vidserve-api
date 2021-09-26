import pymongo
from fastapi import APIRouter, Body, Request, HTTPException, status, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_auth0 import Auth0, Auth0User
from dotenv import load_dotenv
import os

load_dotenv()

auth = Auth0(domain=os.environ['AUTH0_DOMAIN'], api_audience=os.environ['AUTH0_AUDIENCE'], scopes={'read:test': ''})
optional_auth = Auth0(domain=os.environ['AUTH0_DOMAIN'], api_audience=os.environ['AUTH0_AUDIENCE'], auto_error=False)

router = APIRouter()


@router.get("/", response_description="List categories")
async def list_categories(request: Request):
    categories = []
    for doc in await request.app.mongodb["videos"].find({"unlisted": False}).distinct("categories"):
        categories.append(doc)
    categories.sort()
    return categories


@router.get("/{category}", response_description="List videos from category")
async def list_category_videos(category: str, request: Request, skip: int = 0, limit: int = 10):
    videos = []
    categories = category.split('+')
    total = await request.app.mongodb["videos"].count_documents({"unlisted": False, "categories": {"$all": categories}})
    query = await request.app.mongodb["videos"].find({"unlisted": False, "categories": {"$all": categories}}).skip(
        skip).to_list(
        length=limit)
    for doc in query:
        videos.append(doc)
    result = {
        "total": total,
        "videos": videos
    }

    return result
