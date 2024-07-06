# Import all the models, so that Base has them before being
# imported by Alembic

import app.common.models
from app.db.base_class import Base