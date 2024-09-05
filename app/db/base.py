# Import all the models, so that Base has them before being
# imported by Alembic

from app.common.models.uni import Uni
from app.common.models.user import User
from app.common.models.project import Project
from app.common.models.request import Request
from app.common.models.invite import Invite
from app.common.models.filter import Filter
from app.common.models.banned_user import BannedUser
from app.common.models.banned_project import BannedProject
from app.common.models.premium import Premium
from app.common.models.report import Report
from app.db.base_class import Base