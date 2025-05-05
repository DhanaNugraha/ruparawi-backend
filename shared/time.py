from datetime import datetime, timedelta, timezone, date

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


def parse_mm_yy_date(value):
    """Convert MM/YY string to date object (last day of month)"""
    if isinstance(value, date):
        return value

    try:
        month, year = map(int, value.split("/"))
        # test with   expiry_date=date(2025, 2, 28), expiry_date="02/25"
        
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 01 and 12")
        if year < 0 or year > 99:
            raise ValueError("Year must be between 00 and 99")

        # Convert 2-digit year to 4-digit (2000-2099)
        full_year = 2000 + year if year < 100 else year
        # Get last day of month
        if month == 12:
            return date(full_year + 1, 1, 1) - timedelta(days=1)
        return date(full_year, month + 1, 1) - timedelta(days=1)
    except Exception as e:
        raise ValueError(f"Invalid MM/YY format: {str(e)}") from e