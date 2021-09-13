from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/", response_description="List categories")
async def list_categories(request: Request):
    categories = []
    for doc in await request.app.mongodb["videos"].distinct("categories"):
        categories.append(doc)
    return categories


@router.get("/{category}", response_description="List videos from category")
async def list_category_videos(category: str, request: Request, skip: int = 0, limit: int = 10):
    videos = []
    categories = category.split('+')
    total = await request.app.mongodb["videos"].count_documents({"categories": {"$all": categories}})
    query = await request.app.mongodb["videos"].find({"categories": {"$all": categories}}).skip(
        skip).to_list(
        length=limit)
    for doc in query:
        videos.append(doc)
    result = {
        "total": total,
        "videos": videos
    }

    return result
