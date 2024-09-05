from app.common.repository.user_repository import UserRepository

async def get_base_filter(data: dict) -> dict:
    
    user = await UserRepository.get_by_telegram_id(telegram_id=data["telegram_id"])
    
    filter = {
        'user_id': user.id,
        'telegram_id': user.telegram_id,
        'project_uni_id': user.uni_id,
        'profile_uni_id': user.uni_id,
        'profile_topic': None,
        'project_topic': None
    }
    
    return filter