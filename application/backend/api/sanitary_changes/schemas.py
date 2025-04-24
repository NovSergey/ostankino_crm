from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

from application.backend.api.sanitary_breaks.schemas import SanitaryBreakObjectInfo
from application.backend.api.users.schemas import UserOut


class SanitaryChangeBase(BaseModel):
    id: int
    user: UserOut
    sanitary_break: SanitaryBreakObjectInfo
    time_changed: datetime
    time_from: int
    time_to: int
    model_config = ConfigDict(from_attributes=True)

    @field_serializer('time_changed')
    def serialize_time(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%d %H:%M:%S")