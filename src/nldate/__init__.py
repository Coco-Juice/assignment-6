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

NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

_NUM_PAT = r"(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"


def _to_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return NUMBER_WORDS[s]


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
    days_ahead = target_weekday - from_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return from_date + timedelta(days=days_ahead)


def _prev_weekday(from_date: date, target_weekday: int) -> date:
    days_behind = from_date.weekday() - target_weekday
    if days_behind <= 0:
        days_behind += 7
    return from_date - timedelta(days=days_behind)


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip().lower()

    abs_date = _parse_absolute(s)
    if abs_date:
        return abs_date

    if s == "today":
        return today
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s == "yesterday":
        return today + timedelta(days=-1)

    m = re.search(r"in\s+" + _NUM_PAT + r"\s+days?$", s)
    if m:
        return today + timedelta(days=_to_int(m.group(1)))

    m = re.search(r"in\s+" + _NUM_PAT + r"\s+weeks?$", s)
    if m:
        return today + timedelta(weeks=_to_int(m.group(1)))

    m = re.search(r"in\s+" + _NUM_PAT + r"\s+months?$", s)
    if m:
        n = _to_int(m.group(1))
        total = today.month - 1 + n
        return date(today.year + total // 12, total % 12 + 1, today.day)

    m = re.search(r"in\s+" + _NUM_PAT + r"\s+years?$", s)
    if m:
        return date(today.year + _to_int(m.group(1)), today.month, today.day)

    m = re.search(_NUM_PAT + r"\s+days?\s+from\s+now$", s)
    if m:
        return today + timedelta(days=_to_int(m.group(1)))

    m = re.search(_NUM_PAT + r"\s+weeks?\s+from\s+now$", s)
    if m:
        return today + timedelta(weeks=_to_int(m.group(1)))

    m = re.search(_NUM_PAT + r"\s+months?\s+from\s+now$", s)
    if m:
        n = _to_int(m.group(1))
        total = today.month - 1 + n
        return date(today.year + total // 12, total % 12 + 1, today.day)

    m = re.search(_NUM_PAT + r"\s+years?\s+from\s+now$", s)
    if m:
        return date(today.year + _to_int(m.group(1)), today.month, today.day)

    m = re.search(r"a\s+day\s+from\s+now$", s)
    if m:
        return today + timedelta(days=1)

    m = re.search(r"a\s+week\s+from\s+now$", s)
    if m:
        return today + timedelta(weeks=1)

    m = re.search(r"a\s+month\s+from\s+now$", s)
    if m:
        total = today.month
        return date(today.year + total // 12, total % 12 + 1, today.day)

    m = re.search(r"a\s+year\s+from\s+now$", s)
    if m:
        return date(today.year + 1, today.month, today.day)

    m = re.search(_NUM_PAT + r"\s+days?\s+ago$", s)
    if m:
        return today - timedelta(days=_to_int(m.group(1)))

    m = re.search(_NUM_PAT + r"\s+weeks?\s+ago$", s)
    if m:
        return today - timedelta(weeks=_to_int(m.group(1)))

    m = re.search(r"a\s+week\s+ago$", s)
    if m:
        return today - timedelta(weeks=1)

    m = re.search(_NUM_PAT + r"\s+months?\s+ago$", s)
    if m:
        n = _to_int(m.group(1))
        total = today.month - 1 - n
        return date(today.year + total // 12, total % 12 + 1, today.day)

    m = re.search(r"a\s+month\s+ago$", s)
    if m:
        total = today.month - 2
        return date(today.year + total // 12, total % 12 + 1, today.day)

    m = re.search(_NUM_PAT + r"\s+years?\s+ago$", s)
    if m:
        return date(today.year - _to_int(m.group(1)), today.month, today.day)

    m = re.search(r"a\s+year\s+ago$", s)
    if m:
        return date(today.year - 1, today.month, today.day)

    m = re.search(r"\b(before|after)\b", s)
    if m:
        raw_deltas = s[: m.start()].strip()
        base_str = s[m.end() :].strip()
        parts = re.findall(_NUM_PAT + r"\s+(days?|weeks?|months?|years?)", raw_deltas)
        if len(parts) >= 2:
            d = _parse_absolute(base_str)
            if d is None:
                base_lower = base_str.strip().lower()
                if base_lower == "today":
                    d = today
                elif base_lower == "tomorrow":
                    d = today + timedelta(days=1)
                elif base_lower == "yesterday":
                    d = today - timedelta(days=1)
            if d:
                direction = m.group(1)
                for num_str, unit in parts:
                    n = _to_int(num_str)
                    if unit.startswith("day"):
                        delta = timedelta(days=n)
                    elif unit.startswith("week"):
                        delta = timedelta(weeks=n)
                    elif unit.startswith("month"):
                        total = d.month - 1 + (n if direction == "after" else -n)
                        d = date(d.year + total // 12, total % 12 + 1, d.day)
                        continue
                    elif unit.startswith("year"):
                        d = date(
                            d.year + (n if direction == "after" else -n), d.month, d.day
                        )
                        continue
                    d = d + delta if direction == "after" else d - delta
                return d

    m = re.search(_NUM_PAT + r"\s+days?\s+before\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return d - timedelta(days=n)

    m = re.search(_NUM_PAT + r"\s+days?\s+after\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return d + timedelta(days=n)

    m = re.search(_NUM_PAT + r"\s+weeks?\s+before\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return d - timedelta(weeks=n)

    m = re.search(_NUM_PAT + r"\s+weeks?\s+after\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return d + timedelta(weeks=n)

    m = re.search(_NUM_PAT + r"\s+months?\s+before\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            total = d.month - 1 - n
            return date(d.year + total // 12, total % 12 + 1, d.day)

    m = re.search(_NUM_PAT + r"\s+months?\s+after\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            total = d.month - 1 + n
            return date(d.year + total // 12, total % 12 + 1, d.day)

    m = re.search(_NUM_PAT + r"\s+years?\s+before\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return date(d.year - n, d.month, d.day)

    m = re.search(_NUM_PAT + r"\s+years?\s+after\s+(.+)$", s)
    if m:
        n = _to_int(m.group(1))
        d = _parse_absolute(m.group(2).strip())
        if d:
            return date(d.year + n, d.month, d.day)

    if s == "next week":
        return today + timedelta(days=7)
    if s == "last week":
        return today + timedelta(days=-7)

    m = re.search(_NUM_PAT + r"\s+weeks?\s+from\s+today$", s)
    if m:
        return today + timedelta(weeks=_to_int(m.group(1)))

    m = re.search(r"next\s+([A-Za-z]+)$", s)
    if m:
        day_name = m.group(1).lower()
        if day_name in WEEKDAYS:
            return _next_weekday(today, WEEKDAYS[day_name])

    m = re.search(r"last\s+([A-Za-z]+)$", s)
    if m:
        day_name = m.group(1).lower()
        if day_name in WEEKDAYS:
            return _prev_weekday(today, WEEKDAYS[day_name])

    m = re.search(r"([A-Za-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})", s)
    if m:
        month = MONTHS.get(m.group(1).lower())
        if month:
            return date(int(m.group(3)), month, int(m.group(2)))

    raise ValueError(f"Unable to parse date: {s!r}")
