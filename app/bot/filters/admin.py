from aiogram.filters import Filter

from app.core.config import settings

class IsAdmin(Filter):
    async def __call__(self, message):
        return message.from_user.id == settings.ADMIN_ID