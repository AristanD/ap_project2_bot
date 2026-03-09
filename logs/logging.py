import logging
from aiogram import BaseMiddleware


logger = logging.getLogger(__name__)


class Logging(BaseMiddleware):
    """Логирование сообщений пользователя"""
    async def __call__(self, handler, event, data):

        if hasattr(event, "text") and event.text:
            user = event.from_user.id if event.from_user else "unknown"
            logger.info(f"user={user} message='{event.text}'")

        return await handler(event, data)