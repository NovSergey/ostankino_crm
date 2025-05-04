from datetime import datetime

from application.backend.api.general_schemas.base import CustomBaseModel


class NotificationBase(CustomBaseModel):
    id: int
    title: str
    message: str
    time: datetime
    is_read: bool
