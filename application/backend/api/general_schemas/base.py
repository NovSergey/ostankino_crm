from pydantic import BaseModel
from datetime import datetime
from application.backend.utils.time import format_datetime_local


class CustomBaseModel(BaseModel):
    model_config = {
        "from_attributes": True,
        "json_encoders": {
            datetime: format_datetime_local
        }
    }