from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/", response_description="List categories")
async def list_categories(request: Request):
    tasks = []
    for doc in await request.app.mongodb["videos"].distinct("categories"):
        tasks.append(doc)
    return tasks


@router.get("/{category}", response_description="List videos from category")
async def list_category_videos(category: str, request: Request):
    tasks = []
    categories = category.split('+')
    for doc in await request.app.mongodb["videos"].find({"categories": {"$all": categories}}).to_list(length=100):
        tasks.append(doc)
    return tasks
