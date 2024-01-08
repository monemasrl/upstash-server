"""Implements the Redis KEYS command."""
from commands.base import BaseCommand
from config import get_redis


class KeysCommand(BaseCommand):
    """Implements the Redis KEYS command."""
    async def execute(self, credentials, body):
        """Executes the Redis KEYS command."""
        client = get_redis()
        if len(body) > 1:
            pattern = body[1]
        else:
            pattern = '*'
        value = await client.keys(f'{credentials.credentials}:{pattern}')
        return value

Keys = KeysCommand()