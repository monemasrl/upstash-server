"""Implements the Redis GET command."""
from commands.base import BaseCommand
from config import get_redis


class GetCommand(BaseCommand):
    """Implements the Redis GET command."""
    async def execute(self, credentials, body):
        """Executes the Redis GET command."""
        client = get_redis()
        key = body[1]
        value = await client.get(f'{credentials.credentials}:{key}')
        return value

Get = GetCommand()