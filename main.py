from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps.video.routers import router as video_router
from apps.category.routers import router as category_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://10.0.0.238:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(
        "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
    app.mongodb = app.mongodb_client["vidserver"]


app.mount("/files", StaticFiles(directory="static"), name="static")
app.include_router(video_router, tags=['videos'], prefix='/video')
app.include_router(category_router, tags=['category'], prefix='/category')

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        reload=True,
        port=8000
    )