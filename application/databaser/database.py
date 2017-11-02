from application import app
import MySQLdb

db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                     app.config["DATABASE_NAME"])


def execute_write(sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except:
        db.rollback()
        return False


def execute_read(sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        return cursor
    except:
        return None


def add_user(obj):
    if not ("username" in obj):
        return False
    if not ("password" in obj):
        return False
    if not ("nickname" in obj):
        obj["nickname"] = obj["username"]
    if not ("phone_number" in obj):
        return False
    if not ("mail" in obj):
        return False

    return execute_write("""
        INSERT INTO user(create_time,username,password,nickname,phone_number,mail,user_type)
        VALUES (NOW(),'%s','%s','%s','%s','%s','%d')
    """ % (obj["username"], obj["password"], obj["nickname"], obj["phone_number"], obj["mail"], 0))


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
        if execute_write("""
            DELETE FROM law WHERE
              code = '%s'
        """ % code):
            return True
        else:
            return False


def gen_code():
    import random
    code = str(random.randint(100000, 999999))
    execute_write("""
        INSERT INTO law(code,create_time)
        VAKUES ('%s',NOW())
    """ % code)

    return code


def check_user(args):
    if not ("username" in args):
        return False
    if not ("password" in args):
        return False

    cursor = execute_read("""SELECT * FROM user WHERE
      username='%s' AND password='%s'
    """ % (args["username"], args["password"]))

    if cursor is None:
        return False

    result = cursor.fetch_all()
    if len(result) > 0:
        return True
    else:
        return False
