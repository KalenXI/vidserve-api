from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from passlib.hash import sha256_crypt

from .models import LibraryModel, UpdateLibraryModel

router = APIRouter()


@router.post("/", response_description="Add new library")
async def create_library(request: Request, library: LibraryModel = Body(...)):
    library = jsonable_encoder(library)
    new_library = await request.app.mongodb["libraries"].insert_one(library)
    created_library = await request.app.mongodb["libraries"].find_one(
        {"_id": new_library.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_library)


@router.get("/", response_description="List all public libraries")
async def list_libraries(request: Request):
    library = []
    for doc in await request.app.mongodb["libraries"].find({"private": False}).to_list(length=100):
        library.append(doc)
    return library


@router.get("/{id}", response_description="Get a single library")
async def show_library(id: str, request: Request, passwd: Optional[str] = None):
    if (library := await request.app.mongodb["libraries"].find_one({"_id": id})) is not None:
        if library['private'] == 'False':
            return library
        else:
            if passwd is None:
                raise HTTPException(status_code=401, detail=f"Unauthorized")
            elif sha256_crypt.verify(passwd, library['password']):
                return library
            else:
                raise HTTPException(status_code=401, detail=f"Unauthorized")

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.put("/{id}", response_description="Update a library")
async def update_library(id: str, request: Request, video: UpdateLibraryModel = Body(...)):
    video = {k: v for k, v in video.dict().items() if v is not None}

    if len(video) >= 1:
        update_result = await request.app.mongodb["libraries"].update_one({"_id": id}, {"$set": video})

        if update_result.modified_count == 1:
            if (updated_video := await request.app.mongodb["libraries"].find_one({"_id": id})) is not None:
                return updated_video

    if (existing_video := await request.app.mongodb["libraries"].find_one({"_id": id})) is not None:
        return existing_video

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", response_description="Delete Video")
async def delete_video(id: str, request: Request):
    delete_result = await request.app.mongodb["libraries"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
