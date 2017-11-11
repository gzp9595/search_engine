from application import app
import MySQLdb
from application.util import *

db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                     app.config["DATABASE_NAME"])


def execute_write(sql):
    db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                         app.config["DATABASE_NAME"])
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except Exception as e:
        print e
        db.rollback()
        return False


def execute_read(sql):
    db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                         app.config["DATABASE_NAME"])
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        return cursor
    except Exception as e:
        print e
        return None


def add_user(obj, code_level):
    if not ("username" in obj):
        return create_error(1, "Username not found")
    if not ("password" in obj):
        return create_error(2, "Password not found")
    if not ("nickname" in obj):
        obj["nickname"] = obj["username"]
    if not ("phone_number" in obj):
        return create_error(3, "phone_number not found")
    if not ("mail" in obj):
        return create_error(4, "mail not found")
    if not ("user_photo" in obj):
        obj["user_phoho"] = ""
    if not ("user_org" in obj):
        obj["user_org"] = ""
    if not ("user_identity" in obj):
        obj["user_identity"] = 0

    cursor = execute_read("""
        SELECT * FROM user WHERE
          username='%s'
    """ % obj["username"])

    if not (cursor is None):
        if len(cursor.fetchall()) > 0:
            return create_error(5, "User exists")

    success = execute_write("""
        INSERT INTO user(username,password,nickname,phone_number,mail,user_type,user_photo,user_org,user_identity)
        VALUES ('%s','%s','%s','%s','%s',%d,'%s','%s',%d)
    """ % (
        obj["username"], obj["password"], obj["nickname"], obj["phone_number"], obj["mail"], code_level,
        obj["user_photo"],
        obj["user_org"], obj["user_identity"]))

    if success:
        return create_success("Success")
    else:
        return create_error(255, "Unknown error")


def check_code(code):
    cursor = execute_read("""
        SELECT leveltype FROM code WHERE
          code = '%s'
    """ % code)

    if cursor is None:
        return False

    result = cursor.fetchall()

    if len(result) == 0:
        return -1
    else:
        return result[0][0]


def move_code(code):
    if execute_write("""
        DELETE FROM code WHERE
          code = '%s'
    """ % code):
        return True
    else:
        return False


def gen_code(args):
    import random
    level = 0
    if "type" in args:
        level = int(args["type"])
    code = str(random.randint(100000, 999999))
    execute_write("""
        INSERT INTO code(code,leveltype)
        VALUES ('%s',%d)
    """ % (code, level))

    return code


def check_user(args):
    if not ("username" in args):
        return create_error(1, "Username not found")
    if not ("password" in args):
        return create_error(2, "Password not found")

    cursor = execute_read("""SELECT * FROM user WHERE
      username='%s' AND password='%s'
    """ % (args["username"], args["password"]))

    if cursor is None:
        return create_error(255, "Unknown error")

    result = cursor.fetchall()
    if len(result) > 0:
        return create_success("Success")
    else:
        return create_error(3, "Password doesn't match")


def get_user_info(args):
    if not ("username" in args):
        return create_error(1, "Username not found")

    cursor = execute_read("""SELECT * FROM user WHERE
      username='%s'
    """ % args["username"])

    if cursor is None:
        return create_error(255, "Unknown error")

    result = cursor.fetchall()

    if len(result) == 0:
        return create_error(2, "User not found")
    else:
        one = {
            "username": result[0][0],
            "nickname": result[0][2],
            "rest_money": result[0][3],
            "phone_number": result[0][4],
            "mail": result[0][5],
            "user_type": result[0][6],
            "user_photo": result[0][7],
            "user_org": result[0][8],
            "user_identity": result[0][9]
        }

        return create_success(one)

def check_searchable(args):
    if not("username" in args):
        return create_error(1,"Username not found")

    cursor = execute_read("""SELECT usertype FROM user WHERE
      username='%s'
    """ % args["username"])

    if cursor is None:
        return create_error(255,"Unkonwn error")

    result = cursor.fetchall()
    if len(result)==0:
        return create_error(2,"No such user")

    leveltype = result[0][0]
    cursor = execute_read("""SELECT * FROM usertype WHERE
      type_id = %d""" % leveltype)

    if cursor is None:
        return create_error(255,"Unknown error")

    result = cursor.fetchall()

    search_perminute = result[0][1]
    search_perday = result[0][2]


def check_viewable(args):
    if not("username" in args):
        return create_error(1,"Username not found")

    cursor = execute_read("""SELECT usertype FROM user WHERE
      username='%s'
    """ % args["username"])

    if cursor is None:
        return create_error(255,"Unkonwn error")

    result = cursor.fetchall()
    if len(result)==0:
        return create_error(2,"No such user")

    leveltype = result[0][0]
    cursor = execute_read("""SELECT * FROM usertype WHERE
      type_id = %d""" % leveltype)

    if cursor is None:
        return create_error(255,"Unknown error")

    result = cursor.fetchall()

    view_perminute = result[0][1]
    view_perday = result[0][2]

def add_favor_list(args):
    if not("username" in args):
        return create_error(1,"Username not found")
    if not("favor_name" in args):
        return create_error(2,"Favorite list name not found")
    