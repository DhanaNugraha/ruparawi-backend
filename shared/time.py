from datetime import datetime, timezone, date

def now():
    return datetime.now(timezone.utc)

def datetime_from_string(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f%z")

def date_now():
    return date.today()
