from datetime import timedelta, datetime


def get_start_of_week_and_end_of_week():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday() + 1)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week
