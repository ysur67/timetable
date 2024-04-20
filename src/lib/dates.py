from datetime import UTC, date, datetime, timedelta


def utc_now() -> datetime:
    return datetime.now(UTC)


def get_day_of_week(value: date) -> str:  # noqa: PLR0911
    match value.weekday():
        case 0:
            return "Понедельник"
        case 1:
            return "Вторник"
        case 2:
            return "Среда"
        case 3:
            return "Четверг"
        case 4:
            return "Пятница"
        case 5:
            return "Суббота"
        case 6:
            return "Воскресенье"
        case _:
            raise NotImplementedError


def paginate_date_range(*, start: date, end: date, page_size: timedelta) -> list[tuple[date, date]]:
    periods: list[tuple[date, date]] = []
    per_start = start
    while per_start < end:
        per_end = min(per_start + page_size, end)
        periods.append((per_start, per_end))
        per_start = per_end
    return periods
