from datetime import date

from nldate import parse


class TestParse:
    def test_absolute_date_with_month_name(self):
        assert parse("December 1st, 2025") == date(2025, 12, 1)

    def test_absolute_date_with_abbreviated_month(self):
        assert parse("Dec 1, 2025") == date(2025, 12, 1)

    def test_absolute_date_with_abbreviated_month_dot(self):
        assert parse("Dec. 1, 2025") == date(2025, 12, 1)

    def test_absolute_date_iso_format(self):
        assert parse("2025-12-01") == date(2025, 12, 1)

    def test_absolute_date_us_format(self):
        assert parse("12/01/2025") == date(2025, 12, 1)

    def test_absolute_date_slash_format(self):
        assert parse("2025/12/01") == date(2025, 12, 1)

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
        assert parse("I have a meeting on December 1st, 2025") == date(2025, 12, 1)

    def test_sentence_with_days_before(self):
        assert parse("Please remind me 3 days before January 15, 2026") == date(
            2026, 1, 12
        )

    def test_sentence_with_next_weekday(self):
        assert parse(
            "Can we schedule a call next Wednesday", today=date(2026, 5, 11)
        ) == date(2026, 5, 20)

    def test_sentence_with_in_days(self):
        assert parse("Remind me in 5 days", today=date(2025, 6, 15)) == date(
            2025, 6, 20
        )

    def test_sentence_with_in_weeks(self):
        assert parse("Remind me in 2 weeks", today=date(2025, 6, 15)) == date(
            2025, 6, 29
        )

    def test_sentence_with_in_months(self):
        assert parse("Remind me in 3 months", today=date(2025, 6, 15)) == date(
            2025, 9, 15
        )

    def test_sentence_with_in_year(self):
        assert parse("Remind me in 1 year", today=date(2025, 6, 15)) == date(
            2026, 6, 15
        )

    def test_sentence_with_days_ago(self):
        assert parse("I did that 3 days ago", today=date(2025, 6, 15)) == date(
            2025, 6, 12
        )

    def test_sentence_with_weeks_ago(self):
        assert parse("That was 2 weeks ago", today=date(2025, 6, 15)) == date(
            2025, 6, 1
        )

    def test_sentence_with_months_ago(self):
        assert parse("That was 3 months ago", today=date(2025, 6, 15)) == date(
            2025, 3, 15
        )

    def test_sentence_with_years_ago(self):
        assert parse("That was 1 year ago", today=date(2025, 6, 15)) == date(
            2024, 6, 15
        )

    def test_sentence_with_a_week_ago(self):
        assert parse("That was a week ago", today=date(2025, 6, 15)) == date(2025, 6, 8)

    def test_sentence_with_a_month_ago(self):
        assert parse("That was a month ago", today=date(2025, 6, 15)) == date(
            2025, 5, 15
        )

    def test_sentence_with_a_year_ago(self):
        assert parse("That was a year ago", today=date(2025, 6, 15)) == date(
            2024, 6, 15
        )

    def test_sentence_with_two_days_ago(self):
        assert parse("That was two days ago", today=date(2025, 6, 15)) == date(
            2025, 6, 13
        )

    def test_sentence_with_two_weeks_ago(self):
        assert parse("That was two weeks ago", today=date(2025, 6, 15)) == date(
            2025, 6, 1
        )

    def test_sentence_with_two_months_ago(self):
        assert parse("That was two months ago", today=date(2025, 6, 15)) == date(
            2025, 4, 15
        )

    def test_sentence_with_two_years_ago(self):
        assert parse("That was two years ago", today=date(2025, 6, 15)) == date(
            2023, 6, 15
        )

    def test_sentence_with_days_from_now(self):
        assert parse("That is two days from now", today=date(2025, 6, 15)) == date(
            2025, 6, 17
        )

    def test_sentence_with_weeks_from_now(self):
        assert parse("That is two weeks from now", today=date(2025, 6, 15)) == date(
            2025, 6, 29
        )

    def test_sentence_with_months_from_now(self):
        assert parse("That is two months from now", today=date(2025, 6, 15)) == date(
            2025, 8, 15
        )

    def test_sentence_with_years_from_now(self):
        assert parse("That is two years from now", today=date(2025, 6, 15)) == date(
            2027, 6, 15
        )
