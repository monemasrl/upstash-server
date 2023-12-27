import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated, List

import uvicorn
from fastapi import Depends, FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic_settings import BaseSettings
from redis import asyncio as aioredis

security = HTTPBearer()
logger = logging.getLogger("uvicorn")

async def make_bearer_token():
    """
    This function generate a random bearer token on app startup.
    """

    # return os.urandom(16).hex()
    return os.environ.get('BEARER_TOKEN', os.urandom(16).hex())

class Config(BaseSettings):
    # The default URL expects the app to run using Docker and docker-compose.
    redis_url: str = 'redis://{redis_host}:{redis_port}/{redis_db}'.format(
        redis_host=os.environ.get('REDIS_HOST', 'localhost'),
        redis_port=os.environ.get('REDIS_PORT', '6379'),
        redis_db=os.environ.get('REDIS_DB', '0'),
    )
    
    token: str = 'NOT_CONFIGURED'


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5174",
]

config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    token = await make_bearer_token()
    config.token = token
    logger.info(f'Bearer token: {token}')

    yield

client = aioredis.from_url(config.redis_url, decode_responses=True)

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def post_catch_all(request: Request, response: Response, body: List[str | int], credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    
    if credentials.credentials != config.token:
        """If the token is invalid, return a 401 error."""
        response.status_code = status.HTTP_401_UNAUTHORIZED
        logger.info(f'Invalid token: {credentials.credentials}')
        return { "error": "Invalid token" }
    data = await request.json()
    command = data[0].lower() if isinstance(data[0], str) else None 

    logger.info(f'Command: {command}')
    logger.info(f'Data: {data}')
    value = None
    if command == 'set':
        key = data[1]
        value = data[2]
        logger.info(f'Setting {key} to {value}')
        await client.set(key, value)
    elif command == 'get':
        key = data[1]
        logger.info(f'Getting {key} returned {value}')
        value = await client.get(key)
        # Deserialize the value from JSON.
    elif command == 'delete':
        key = data[1]
        logger.info(f'Deleting {key}')
        await client.delete(key)
    elif command == 'keys':
        if len(data) > 1:
            pattern = data[1]
        else:
            pattern = '*'
        value = await client.keys(pattern)
    elif command == 'info':
        value = await client.info()

    return { "result": value }

@app.get("/")
async def root():
    return { "result": "OK" }

@app.get("/{path_name:path}")
async def catch_all(request: Request, response: Response, path_name: str, credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    if credentials.credentials != config.token:
        """If the token is invalid, return a 401 error."""
        response.status_code = status.HTTP_401_UNAUTHORIZED
        logger.info(f'Invalid token: {credentials.credentials}')
        return { "error": "Invalid token" }

    value = None
    request_params = path_name.split('/')
    command = request_params[0].lower() if len(request_params) > 0 else None

    if command == 'get':
        key = request_params[1]
        logger.info(f'Getting {key} returned {value}')
        value = await client.get(key)
    elif command == 'set':
        key = request_params[1]
        value = request_params[2] if len(request_params) > 2 else None
        logger.info(f'Setting {key} to {value}')
        await client.set(key, value)
    elif command == 'delete':
        key = request_params[1]
        logger.info(f'Deleting {key}')
        await client.delete(key)
    elif command == 'keys':
        if len(request_params) > 1:
            pattern = request_params[1]
        else:
            pattern = '*'
        value = await client.keys(pattern)
    elif command == 'info':
        value = await client.info()


    return { "result": value }


if __name__ == "__main__":
    token = make_bearer_token()
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
