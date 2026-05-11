import re
from datetime import date, timedelta

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

MONTHS = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}


def _parse_absolute(s: str) -> date | None:
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})$", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})$", s)
    if m:
        return date(int(m.group(3)), int(m.group(1)), int(m.group(2)))

    m = re.match(r"([A-Za-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})$", s)
    if m:
        month = MONTHS[m.group(1).lower()]
        day = int(m.group(2))
        year = int(m.group(3))
        return date(year, month, day)

    return None


def _next_weekday(from_date: date, target_weekday: int) -> date:
    days_ahead = 7 + target_weekday - from_date.weekday()
    return from_date + timedelta(days=days_ahead)


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip()

    abs_date = _parse_absolute(s)
    if abs_date:
        return abs_date

    if s == "today":
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s == "yesterday":
        return today + timedelta(days=-1)

    m = re.search(r"in\s+(\d+)\s+days?$", s)
    if m:
        return today + timedelta(days=int(m.group(1)))

    m = re.search(r"in\s+(\d+)\s+weeks?$", s)
    if m:
        return today + timedelta(weeks=int(m.group(1)))

    m = re.search(r"in\s+(\d+)\s+months?$", s)
    if m:
        n = int(m.group(1))
        total = today.month - 1 + n
        return date(today.year + total // 12, total % 12 + 1, today.day)

    m = re.search(r"in\s+(\d+)\s+years?$", s)
    if m:
        return date(today.year + int(m.group(1)), today.month, today.day)

    m = re.search(r"(\d+)\s+days?\s+ago$", s)
    if m:
        return today - timedelta(days=int(m.group(1)))

    m = re.search(r"(\d+)\s+weeks?\s+ago$", s)
    if m:
        return today - timedelta(weeks=int(m.group(1)))

    m = re.search(r"(\d+)\s+months?\s+ago$", s)
    if m:
        n = int(m.group(1))
        total = today.month - 1 - n
        return date(today.year + total // 12, total % 12 + 1, today.day)

    m = re.search(r"(\d+)\s+years?\s+ago$", s)
    if m:
        return date(today.year - int(m.group(1)), today.month, today.day)

    m = re.search(r"(\d+)\s+days?\s+before\s+(.+)$", s)
    if m:
        n = int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return d - timedelta(days=n)

    m = re.search(r"(\d+)\s+days?\s+after\s+(.+)$", s)
    if m:
        n = int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return d + timedelta(days=n)

    if s == "next week":
        return today + timedelta(days=7)
    if s == "last week":
        return today + timedelta(days=-7)

    m = re.search(r"(\d+)\s+weeks?\s+from\s+today$", s)
    if m:
        return today + timedelta(weeks=int(m.group(1)))

    m = re.search(r"next\s+([A-Za-z]+)$", s)
    if m:
        day_name = m.group(1).lower()
        if day_name in WEEKDAYS:
            return _next_weekday(today, WEEKDAYS[day_name])

    m = re.search(r"([A-Za-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})", s)
    if m:
        month = MONTHS.get(m.group(1).lower())
        if month:
            return date(int(m.group(3)), month, int(m.group(2)))

    raise ValueError(f"Unable to parse date: {s!r}")
