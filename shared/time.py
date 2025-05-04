from datetime import datetime, timezone, date

def now():
    return datetime.now(timezone.utc)

def datetime_from_string(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f%z")

def datetime_from_date_string(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()  # For date strings
    except ValueError:
        try:
            return datetime.fromisoformat(value)  # For ISO datetime strings
        except ValueError:
            raise ValueError(f"Time data '{value}' doesn't match expected formats")

def date_now():
    return date.today()
