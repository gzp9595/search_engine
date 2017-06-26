import datetime


def check_date(year, month, day):
    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        return False

    try:
        datetime.datetime.strftime(year + "-" + month + "-" + day, "%Y-%m-%d")
        return True
    except ValueError:
        return False
