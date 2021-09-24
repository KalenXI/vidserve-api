import asyncio

import aiofiles
import os
import sys
import ffmpeg_streaming
import datetime
from ffmpeg_streaming import Formats, Bitrate
from fastapi import APIRouter, Body, Request, HTTPException, status, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

from .models import VideoModel, UpdateVideoModel

router = APIRouter()


def monitor(ffmpeg, duration, time_, time_left, process):
    client = MongoClient(
        "mongodb://kevin:narfpoit@10.0.0.10:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
    db = client["vidserver"]
    per = round(time_ / duration * 100)
    db["jobs"].update_one(
        {"_id": process.args[3].split('/')[2]},
        {"$set": {"progress": per, "duration": duration, "remaining": time_left}})
    if per == 100:
        db["jobs"].delete_one({"_id": process.args[3].split('/')[2]})


def encode_video(vid: str, vid_id: str):
    video = ffmpeg_streaming.input(vid)
    hls = video.hls(Formats.h264())
    hls.auto_generate_representations(
        bitrate=[Bitrate(6144000, 131072), Bitrate(3072000, 131072), Bitrate(747520, 131072), Bitrate(373760, 98304),
                 Bitrate(148480, 65536), Bitrate(74240, 65536)])
    hls.output('static/videos/' + vid_id + '/master.m3u8', monitor=monitor)


@router.post("/", response_description="Add new video")
async def create_video(request: Request, video: VideoModel = Body(...)):
    video = jsonable_encoder(video)
    new_video = await request.app.mongodb["videos"].insert_one(video)
    created_video = await request.app.mongodb["videos"].find_one(
        {"_id": new_video.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_video)


@router.post("/upload", response_description="Upload new video")
async def create_video(request: Request, id: str, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    os.makedirs('static/videos/' + id + '/files/', exist_ok=True)
    video_file = 'static/videos/' + id + '/files/' + file.filename
    async with aiofiles.open(video_file, 'wb') as out_file:
        while content := await file.read(1024576):  # async read chunk
            await out_file.write(content)  # async write chunk

    await request.app.mongodb["jobs"].insert_one(
        {"_id": id, "video_file": video_file, "progress": 0, "duration": 0, "remaining": 0})

    background_tasks.add_task(encode_video, video_file, id)

    return {"Result": "OK"}


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
