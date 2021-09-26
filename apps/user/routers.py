from fastapi import APIRouter, Body, Request, HTTPException, status, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_auth0 import Auth0, Auth0User
from .models import User
from dotenv import load_dotenv
import os

load_dotenv()

auth = Auth0(domain=os.environ['AUTH0_DOMAIN'], api_audience=os.environ['AUTH0_AUDIENCE'], scopes={'read:test': ''})
optional_auth = Auth0(domain=os.environ['AUTH0_DOMAIN'], api_audience=os.environ['AUTH0_AUDIENCE'], auto_error=False)

router = APIRouter()


@router.get("/roles", response_description="Get roles for current user", dependencies=[Depends(auth.implicit_scheme)])
async def get_roles(request: Request, user: Auth0User = Security(auth.get_user)):
    return user.permissions
