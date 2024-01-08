import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated, List

import uvicorn
from admin.databases import router as databases_router
from commands import processor
from config import get_settings
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis import asyncio as aioredis

security = HTTPBearer()
logger = logging.getLogger("uvicorn")

settings = get_settings()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5174",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'Bearer token: {settings.token}')
    yield


admin = aioredis.from_url('redis://{redis_host}:{redis_port}/{redis_db}'.format(
        redis_host=settings.redis_admin_host,
        redis_port=settings.redis_admin_port,
        redis_db=settings.redis_admin_db,
), decode_responses=True)

app = FastAPI(
    lifespan=lifespan,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": "upstash-api",
        "clientSecret": "s2H3AyQBdse9j1sj6MrcamPc5AwbsKNM",
        "scopes": ["openid", "offline_access", "profile", "email", "roles", "web-origins", "address", "phone"]
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Add database_router to the app."""
app.include_router(databases_router)

@app.post("/")
async def post_catch_all(request: Request, response: Response, body: List[str | int], credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    user_id = credentials.credentials.split(':')[0]
    database_id = credentials.credentials.split(':')[1]
    admin_key = f'{user_id}:databases'
    databases = await admin.smembers(admin_key)
    found = False
    for database in databases:
        if database_id == database:
            found = True
            break

    if not found:
        """If the token is invalid, return a 401 error."""
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return { "error": "Invalid token" }

    
    data = await request.json()
    command = data[0].lower() if isinstance(data[0], str) else None 

    value = await processor(command, credentials, data)
    return { "result": value }

@app.get("/")
async def root():
    return { "result": "OK" }

@app.get("/{path_name:path}")
async def catch_all(request: Request, response: Response, path_name: str, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    user_id = credentials.credentials.split(':')[0]
    database_id = credentials.credentials.split(':')[1]
    admin_key = f'{user_id}:databases'
    databases = await admin.smembers(admin_key)
    found = False
    for database in databases:
        if database_id == database:
            found = True
            break

    if not found:
        """If the token is invalid, return a 401 error."""
        response.status_code = status.HTTP_401_UNAUTHORIZED
        logger.info(f'Invalid token: {credentials.credentials}')
        return { "error": "Invalid token" }

    value = None
    data = path_name.split('/')
    command = data[0].lower() if len(data) > 0 else None

    value = await processor(command, credentials, data)
    return { "result": value }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
