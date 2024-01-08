"""Crud operations for databases management"""
import logging
import os
from typing import Annotated

from auth.auth import User, get_current_active_user
from config import get_settings
from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from redis import asyncio as aioredis

logger = logging.getLogger("uvicorn")
settings = get_settings()
admin = aioredis.from_url('redis://{redis_host}:{redis_port}/{redis_db}'.format(
        redis_host=settings.redis_admin_host,
        redis_port=settings.redis_admin_port,
        redis_db=settings.redis_admin_db,
), decode_responses=True)
router = APIRouter(
    prefix="/databases",
    tags=["databases"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_databases(current_user: Annotated[User, Security(get_current_active_user)]):
    """Get all databases"""
    search_key = f'{current_user.user_id}:databases'
    databases = await admin.smembers(search_key)
    user_id = current_user.user_id
    return JSONResponse(content=[f'{user_id}:{x}' for x in databases])

@router.post("/")
async def create_database(current_user: Annotated[User, Security(get_current_active_user)]):
    """Create a database"""
    """Generate a new id/token pair and store it in the database."""
    token = os.urandom(16).hex()

    search_key = f'{current_user.user_id}:databases'
    await admin.sadd(search_key, token)
    return JSONResponse(content={"database": f'{current_user.user_id}:{token}'})

@router.delete("/{database_name}")
async def delete_database(database_token: str, current_user: User = Depends(get_current_active_user)):
    """Delete a database"""
    user_id = database_token.split(':')[0]
    if user_id != current_user.user_id:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    database = database_token.split(':')[1]
    search_key = f'{current_user.user_id}:databases'
    await admin.srem(search_key, database)
    return JSONResponse(content={"database": database_token})

