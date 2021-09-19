from fastapi import APIRouter, Body, Request, HTTPException, status, Depends, Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_auth0 import Auth0, Auth0User
from .models import User

auth = Auth0(domain='dev-uxge00vy.us.auth0.com', api_audience='http://10.0.0.238:8000', scopes={'read:test': ''})

router = APIRouter()


@router.get("/roles", response_description="Get roles for current user", dependencies=[Depends(auth.implicit_scheme)])
async def get_roles(request: Request, user: Auth0User = Security(auth.get_user)):
    return user.permissions
