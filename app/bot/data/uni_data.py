from app.common.repository.uni_repository import UniRepository

uni_data = [
    {
        'short_name': 'Московский политех',
        'full_name': 'Московский политехнический университет',
        'city': 'Москва'
    }
]


async def set_uni_data():
    for uni in uni_data:
        existed_uni = await UniRepository.get_one_or_none(short_name=uni['short_name'])
        
        if not existed_uni:
            await UniRepository.add(**uni)