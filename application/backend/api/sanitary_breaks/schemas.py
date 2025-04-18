from pydantic import BaseModel, ConfigDict

from application.backend.api.objects.schemas import Object
from application.backend.core.models import SanitaryTypeEnum


class SanitaryBreakBase(BaseModel):
    object_from_id: int
    object_to_id: int
    time_break: int
    model_config = ConfigDict(from_attributes=True)

class SanitaryBreak(BaseModel):
    id: int
    object_from: Object
    object_to: Object
    time_break: int
    sanitary_type: SanitaryTypeEnum
    model_config = ConfigDict(from_attributes=True)

class SanitaryBreakObjectInfo(BaseModel):
    object_from: Object
    object_to: Object