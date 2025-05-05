import enum


class SanitaryTypeEnum(enum.Enum):
    main = "main"
    car = "car"
    tractor = "tractor"

    @property
    def label(self):
        return {
            "main": "Основная",
            "car": "Водителей",
            "tractor": "Трактористов"
        }[self.value]

class ObjectStatusEnum(enum.Enum):
    open = "Открыт"
    close = "Закрыт"


class RoleEnum(enum.Enum):
    admin = "admin"
    employee = "employee"
    security = "security"


class VisitStatusEnum(enum.Enum):
    success = "Успешно"
    error = "Ошибка"

