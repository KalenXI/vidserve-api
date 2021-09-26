import pymongo
from fastapi import APIRouter, Body, Request, HTTPException, status, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from passlib.hash import sha256_crypt
from fastapi_auth0 import Auth0, Auth0User
from dotenv import load_dotenv
import os

load_dotenv()

auth = Auth0(domain=os.environ['AUTH0_DOMAIN'], api_audience=os.environ['AUTH0_AUDIENCE'], scopes={'read:test': ''})
optional_auth = Auth0(domain=os.environ['AUTH0_DOMAIN'], api_audience=os.environ['AUTH0_AUDIENCE'], auto_error=False)

router = APIRouter()


@router.get("/", response_description="List all libraries", dependencies=[Depends(auth.implicit_scheme)])
async def list_jobs(request: Request, user: Auth0User = Security(auth.get_user)):
    jobs = []
    if 'read:all' in user.permissions:
        for doc in await request.app.mongodb["jobs"].find().to_list(length=100):
            jobs.append(doc)
        return jobs
