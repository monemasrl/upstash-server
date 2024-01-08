"""Implements the Redis DELETE command."""
from commands.base import BaseCommand
from config import get_redis


class DeleteCommand(BaseCommand):
    """Implements the Redis DELETE command."""
    async def execute(self, credentials, body):
        """Executes the Redis DELETE command."""
        client = get_redis()
        key = body[1]
        value = await client.delete(f'{credentials.credentials}:{key}')
        return value

Delete = DeleteCommand()