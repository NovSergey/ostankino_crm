from datetime import datetime, timezone
import pytz

moscow_tz = pytz.timezone("Europe/Moscow")

def format_datetime_local(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(moscow_tz)
    return dt.strftime("%d-%m-%Y %H:%M:%S")
