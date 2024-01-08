"""Implements the Redis INFO command."""
from commands.base import BaseCommand
from config import get_redis


class InfoCommand(BaseCommand):
    """Implements the Redis INFO command."""
    async def execute(self, credentials, body):
        """Executes the Redis INFO command."""
        client = get_redis()
        value = await client.info()
        return value

Info = InfoCommand()