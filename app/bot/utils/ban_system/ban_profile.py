import datetime

from app.common.repository.user_repository import UserRepository
from app.common.repository.banned_user_repository import BannedUserRepository

from app.common.models.user import User


async def ban_profile(user: User):
    await UserRepository.update(model_id=user.id, is_banned=True)
    
    term_minutes = 1
    date_end = datetime.datetime.now() + datetime.timedelta(minutes=term_minutes)
    
    await BannedUserRepository.add(user_id=user.id, term=term_minutes, date_end=date_end)
    
    
async def unban_profile(user: User):
    await UserRepository.update(model_id=user.id, is_banned=False, claim_count=0)
    await BannedUserRepository.delete_by(user_id=user.id)