import datetime
import time
import json

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        print obj
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def form_date(year, month, day):
    month = str(month)
    if len(month) == 1:
        month = "0" + month
    day = str(day)
    if len(day) == 1:
        day = "0" + day
    return str(year) + "-" + str(month) + "-" + str(day)


def check_date(year, month, day):
    try:
        # print year,month,day
        time.strptime(form_date(year, month, day), "%Y-%m-%d")
        # print "Accepted"
        return True
    except Exception as e:
        # print e
        return False


def create_error(code=1, msg=''):
    return {"code": code, "msg": msg}


def create_success(msg):
    return {"code": 0, "msg": msg}


def print_time():
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def merge_dict(arr):
    dic = {}
    for x in arr:
        x = dict(x)
        for y in x:
            dic[y] = x[y][0]
    return dic

def pre_hour():
    now = datetime.datetime.now()
    ph = now - datetime.timedelta(hours=1)

    return time.mktime(ph.timetuple())

def pre_day():
    now = datetime.datetime.now()
    ph = now - datetime.timedelta(days=1)

    return time.mktime(ph.timetuple())
