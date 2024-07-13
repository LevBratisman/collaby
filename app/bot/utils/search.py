from app.common.models.filter import Filter

async def transform_filter_for_search_people(filter: dict) -> dict:
    updated_filter = {}

    for key, value in filter.items():
        if value:
            if key == 'profile_topic':
                updated_filter['topic'] = value
            elif key == 'profile_uni_id':
                updated_filter['uni_id'] = value
                
    updated_filter["is_authorized"] = True
    updated_filter["is_banned"] = False
            
    return updated_filter


async def transform_filter_for_search_projects(filter: dict) -> dict:
    updated_filter = {}

    for key, value in filter.items():
        if value:
            if key == 'project_topic':
                updated_filter['topic'] = value
            elif key == 'project_uni_id':
                updated_filter['uni_id'] = value
                
    updated_filter["is_banned"] = False
                            
    return updated_filter