from datetime import datetime

from pydantic import ConfigDict

from application.backend.api.general_schemas.base import CustomBaseModel
from application.backend.api.sanitary_breaks.schemas import SanitaryBreakObjectInfo
from application.backend.api.users.schemas import UserOut


class SanitaryChangeBase(CustomBaseModel):
    id: int
    user: UserOut
    sanitary_break: SanitaryBreakObjectInfo
    time_changed: datetime
    time_from: int
    time_to: int
    model_config = ConfigDict(from_attributes=True)