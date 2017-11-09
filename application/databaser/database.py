from application import app
import MySQLdb
from application.util import *

db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                     app.config["DATABASE_NAME"])


def execute_write(sql):
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
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        return cursor
    except Exception as e:
        print e
        return None


def add_user(obj):
    if not ("username" in obj):
        return create_error("Username not found")
    if not ("password" in obj):
        return create_error("Password not found")
    if not ("nickname" in obj):
        obj["nickname"] = obj["username"]
    if not ("phone_number" in obj):
        return create_error("phone_number not found")
    if not ("mail" in obj):
        return create_error("mail not found")

    cursor = execute_read("""
        SELECT * FROM user WHERE
          username='%s'
    """ % obj["username"])

    if not (cursor is None):
        if len(cursor.fetchall()) > 0:
            return create_error("User exists")

    success = execute_write("""
        INSERT INTO user(create_time,username,password,nickname,phone_number,mail,user_type)
        VALUES (NOW(),'%s','%s','%s','%s','%s','%d')
    """ % (obj["username"], obj["password"], obj["nickname"], obj["phone_number"], obj["mail"], 0))

    if success:
        return create_success("Success")
    else:
        return create_error("Unknown error")


def check_code(code):
    cursor = execute_read("""
        SELECT * FROM code WHERE
          code = '%s'
    """ % code)

    if cursor is None:
        return False

    result = cursor.fetchall()

    if len(result) == 0:
        return False
    else:
        return True


def move_code(code):
    if execute_write("""
        DELETE FROM code WHERE
          code = '%s'
    """ % code):
        return True
    else:
        return False


def gen_code():
    import random
    code = str(random.randint(100000, 999999))
    execute_write("""
        INSERT INTO code(code,create_time)
        VALUES ('%s',NOW())
    """ % code)

    return code


def check_user(args):
    if not ("username" in args):
        return create_error("Username not found")
    if not ("password" in args):
        return create_error("Password not found")

    cursor = execute_read("""SELECT * FROM user WHERE
      username='%s' AND password='%s'
    """ % (args["username"], args["password"]))

    if cursor is None:
        return create_error("Unknown error")

    result = cursor.fetchall()
    if len(result) > 0:
        return create_success("Success")
    else:
        return create_error("Password doesn't match")
