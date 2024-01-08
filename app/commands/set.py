"""Implements the Redis SET command."""
from commands.base import BaseCommand
from config import get_redis


class SetCommand(BaseCommand):
    """Implements the Redis SET command."""
    async def execute(self, credentials, body):
        """Executes the Redis SET command."""
        client = get_redis()
        key = body[1]
        value = body[2]
        await client.set(f'{credentials.credentials}:{key}', value)
        return value

Set = SetCommand()