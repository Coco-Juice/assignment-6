from datetime import date

from nldate import parse


class TestParse:
    def test_absolute_date_with_month_name(self):
        assert parse("December 1st, 2025") == date(2025, 12, 1)

    def test_absolute_date_iso_format(self):
        assert parse("2025-12-01") == date(2025, 12, 1)

    def test_absolute_date_us_format(self):
        assert parse("12/01/2025") == date(2025, 12, 1)

    def test_today(self):
        assert parse("today", today=date(2025, 6, 15)) == date(2025, 6, 15)

    def test_tomorrow(self):
        assert parse("tomorrow", today=date(2025, 6, 15)) == date(2025, 6, 16)

    def test_yesterday(self):
        assert parse("yesterday", today=date(2025, 6, 15)) == date(2025, 6, 14)

    def test_days_before_absolute(self):
        assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)

    def test_days_after_absolute(self):
        assert parse("3 days after December 1st, 2025") == date(2025, 12, 4)

    def test_next_week(self):
        assert parse("next week", today=date(2025, 12, 1)) == date(2025, 12, 8)

    def test_last_week(self):
        assert parse("last week", today=date(2025, 12, 1)) == date(2025, 11, 24)

    def test_x_weeks_from_today(self):
        assert parse("2 weeks from today", today=date(2025, 6, 15)) == date(2025, 6, 29)

    def test_next_tuesday(self):
        assert parse("next Tuesday", today=date(2025, 12, 1)) == date(2025, 12, 9)

    def test_sentence_with_absolute_date(self):
        assert (
            parse("I have a meeting on December 1st, 2025")
            == date(2025, 12, 1)
        )

    def test_sentence_with_days_before(self):
        assert (
            parse("Please remind me 3 days before January 15, 2026")
            == date(2026, 1, 12)
        )

    def test_sentence_with_next_weekday(self):
        assert (
            parse("Can we schedule a call next Wednesday", today=date(2026, 5, 11))
            == date(2026, 5, 20)
        )
