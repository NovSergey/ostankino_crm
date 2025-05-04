from datetime import datetime

from pydantic import field_serializer

from application.backend.api.employees.schemas import Employee
from application.backend.api.visit_history.schemas import VisitHistoryLast


class EmployeeScanResult(Employee):
    last_visit: VisitHistoryLast | None
    can_visit: bool
    time_to_visit: datetime | None

    @field_serializer('time_to_visit')
    def serialize_time(self, dt: datetime | None, _info):
        if dt is None:
            return None  # или можешь вернуть какой-то дефолтный формат
        return dt.strftime("%d-%m-%Y %H:%M:%S")