import logging
from aiogram import BaseMiddleware


logger = logging.getLogger(__name__)


class Logging(BaseMiddleware):
    """Логирование"""
    async def __call__(self, handler, event, data):

        if hasattr(event, "text"):
            logger.info(f"User command: {event.text}")

        return await handler(event, data)