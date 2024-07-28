from datetime import datetime

from app.common.repository.user_repository import UserRepository
from app.common.repository.banned_user_repository import BannedUserRepository

from app.common.models.user import User


async def ban_profile(user: User):
    await UserRepository().update(model_id=user.id, is_banned=True)
    
    term_days = 10
    date_end = datetime.now() + datetime.timedelta(days=term_days)
    
    await BannedUserRepository().add(user_id=user.id, term=term_days, date_end=date_end)
    
    
async def unban_profile(user: User):
    await UserRepository().update(model_id=user.id, is_banned=False)
    await BannedUserRepository().delete(user_id=user.id)