import datetime
import time


def check_date(year, month, day):
    if len(month)==1:
        month = "0"+month
    if len(day)==1:
        day = "0"+day
    if len(year) != 4 or len(month) != 2 or len(day) != 2:
        return False

    try:
        # print year,month,day
        time.strptime(str(year) + "-" + str(month) + "-" + str(day), "%Y-%m-%d")
        # print "Accepted"
        return True
    except Exception as e:
        # print e
        return False


def print_time():
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
