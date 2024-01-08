import os
from functools import lru_cache

from pydantic_settings import BaseSettings
from redis import asyncio as redis


class Settings(BaseSettings):
    auth_domain: str = 'auth.service.monema.dev'
    auth_api_audience: str = 'account'
    auth_issuer: str = 'https://auth.service.monema.dev/realms/upstash'
    auth_algorithms: str = 'RS256'
    redis_host: str = 'localhost'
    redis_port: str = '6379'
    redis_db: str = '1'
    redis_admin_host: str = 'localhost'
    redis_admin_port: str = '6379'
    redis_admin_db: str = '0'
    token: str = os.urandom(16).hex()

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

def create_redis():
    return redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)

pool = create_redis()

def get_redis():
  # Here, we re-use our connection pool
  # not creating a new one
  return redis.Redis(connection_pool=pool)

def create_redis_admin():
    return redis.ConnectionPool(host=settings.redis_admin_host, port=settings.redis_admin_port, db=settings.redis_admin_db)

admin_pool = create_redis_admin()

def get_redis_admin():
  # Here, we re-use our connection pool
  # not creating a new one
  return redis.Redis(connection_pool=admin_pool)
