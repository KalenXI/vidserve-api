from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import VideoModel, UpdateVideoModel

router = APIRouter()


@router.post("/", response_description="Add new video")
async def create_video(request: Request, video: VideoModel = Body(...)):
    video = jsonable_encoder(video)
    new_video = await request.app.mongodb["videos"].insert_one(video)
    created_video = await request.app.mongodb["videos"].find_one(
        {"_id": new_video.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_video)


@router.get("/", response_description="List all videos")
async def list_videos(request: Request, skip: int = 0, limit: int = 10):
    videos = []
    for doc in await request.app.mongodb["videos"].find({"unlisted": False}).skip(skip).to_list(length=limit):
        videos.append(doc)
    return videos


@router.get("/{id}", response_description="Get a single task")
async def show_video(id: str, request: Request):
    if (video := await request.app.mongodb["videos"].find_one({"_id": id})) is not None:
        return video

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.put("/{id}", response_description="Update a video")
async def update_video(id: str, request: Request, video: UpdateVideoModel = Body(...)):
    video = {k: v for k, v in video.dict().items() if v is not None}

    if len(video) >= 1:
        update_result = await request.app.mongodb["videos"].update_one({"_id": id}, {"$set": video})

        if update_result.modified_count == 1:
            if (updated_video := await request.app.mongodb["videos"].find_one({"_id": id})) is not None:
                return updated_video

    if (existing_video := await request.app.mongodb["tasks"].find_one({"_id": id})) is not None:
        return existing_video

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", response_description="Delete Video")
async def delete_video(id: str, request: Request):
    delete_result = await request.app.mongodb["tasks"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
