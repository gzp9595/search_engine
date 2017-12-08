#  -*- coding:utf-8 -*-

from application import app
import MySQLdb
from application.util import *

db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                     app.config["DATABASE_NAME"])


def execute_write(sql):
    db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                         app.config["DATABASE_NAME"])
    cursor = db.cursor()
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    try:
        cursor.execute(sql)
        db.commit()
        return True
    except Exception as e:
        print e
        db.rollback()
        return False


def execute_write_return_cursor(sql):
    db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                         app.config["DATABASE_NAME"])
    cursor = db.cursor()
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    try:
        cursor.execute(sql)
        db.commit()
        return cursor
    except Exception as e:
        print e
        db.rollback()
        return None


def execute_read(sql):
    db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],
                         app.config["DATABASE_NAME"])
    cursor = db.cursor()
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    try:
        cursor.execute(sql)
        return cursor
    except Exception as e:
        print e
        return None


def add_user(obj, code_level):
    if not ("username" in obj):
        return create_error(1, u"没有用户参数")
    if not ("password" in obj):
        return create_error(2, u"没有密码参数")
    if not ("nickname" in obj):
        obj["nickname"] = obj["username"]
    if not ("phone_number" in obj):
        return create_error(3, u"没有电话号码")
    if not ("mail" in obj):
        return create_error(4, u"没有邮件地址")
    if not ("user_photo" in obj):
        obj["user_photo"] = ""
    if not ("user_org" in obj):
        obj["user_org"] = ""
    if not ("user_identity" in obj):
        obj["user_identity"] = 0
    if not ("user_code" in obj):
        return create_error(999,u"???")

    if execute_read("""SELECT COUNT(*) FROM user WHERE mail='%s'""" % obj["mail"]).fetchall()[0][0] != 0:
        return create_error(53, u"邮箱已被使用")

    if execute_read("""SELECT COUNT(*) FROM user WHERE phone_number='%s'""" % obj["phone_number"]).fetchall()[0][
        0] != 0:
        return create_error(54, u"电话号码已被使用")

    cursor = execute_read("""
        SELECT * FROM user WHERE
          username='%s'
    """ % obj["username"])

    if not (cursor is None):
        if len(cursor.fetchall()) > 0:
            return create_error(5, u"用户已存在")

    success = execute_write("""
        INSERT INTO user(create_time,username,password,nickname,phone_number,mail,user_type,user_photo,user_org,user_identity,user_code)
        VALUES (NOW(),'%s','%s','%s','%s','%s',%d,'%s','%s',%d,'%s')
    """ % (
        obj["username"], obj["password"], obj["nickname"], obj["phone_number"], obj["mail"], code_level,
        obj["user_photo"],
        obj["user_org"], obj["user_identity"],obj["user_code"]))

    if success:
        res = add_favor_list({"username": obj["username"], "favor_name": "Default"})
        print res
        if res["code"] == 0:
            return create_success("Success")
        else:
            return res
    else:
        return create_error(255, u"未知错误")


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
    import uuid
    level = 0
    if "type" in args:
        level = int(args["type"])
    if "code" in args:
        code = str(args["code"])
    else:
        code = str(uuid.uuid4())
    execute_write("""
        INSERT INTO code(code,leveltype)
        VALUES ('%s',%d)
    """ % (code, level))

    return code


def check_user(args):
    if not ("username" in args):
        return create_error(1, u"没有用户名")
    if not ("password" in args):
        return create_error(2, u"没有密码")

    cursor = execute_read("""SELECT * FROM user WHERE
      username='%s' AND password='%s'
    """ % (args["username"], args["password"]))

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()
    if len(result) > 0:
        return create_success("Success")
    else:
        return create_error(3, u"密码不正确")


def get_user_info(args):
    if not ("username" in args):
        return create_error(1, u"没有用户名")

    cursor = execute_read("""SELECT * FROM user WHERE
      username='%s'
    """ % args["username"])

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()

    if len(result) == 0:
        return create_error(2, u"用户不存在")
    else:
        one = {
            "username": result[0][1],
            "nickname": result[0][3],
            "rest_money": result[0][4],
            "phone_number": result[0][5],
            "mail": result[0][6],
            "user_type": result[0][7],
            "user_photo": result[0][8],
            "user_org": result[0][9],
            "user_identity": result[0][10]
        }

        return create_success(one)


def check_searchable(args):
    if not ("username" in args):
        return create_error(1, u"未找到用户名")

    cursor = execute_read("""SELECT user_type FROM user WHERE
      username='%s'
    """ % args["username"])

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()
    if len(result) == 0:
        return create_error(2, u"用户不存在")

    leveltype = result[0][0]
    cursor = execute_read("""SELECT * FROM usertype WHERE
      type_id = %d""" % leveltype)

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()

    search_perminute = result[0][1]
    search_perday = result[0][2]

    print pre_minute(), pre_day()

    cursor1 = execute_read(
        """SELECT COUNT(*) FROM log WHERE UNIX_TIMESTAMP(create_time)>=%d AND type_number=1""" % pre_minute())
    cursor2 = execute_read(
        """SELECT COUNT(*) FROM log WHERE UNIX_TIMESTAMP(create_time)>=%d AND type_number=1""" % pre_day())

    count1 = cursor1.fetchall()[0][0]
    count2 = cursor2.fetchall()[0][0]
    print count1, count2

    limit1 = \
        execute_read("""SELECT search_perminute FROM usertype WHERE type_id=%d""" % leveltype).fetchall()[
            0][0]
    limit2 = \
        execute_read("""SELECT search_perday FROM usertype WHERE type_id=%d""" % leveltype).fetchall()[0][
            0]

    if count1 >= limit1:
        return create_error(73, u"超过分钟数搜索限制")

    if count2 >= limit2:
        return create_error(74, u"超过小时数搜索限制")

    return create_success("Success")


def check_viewable(args):
    if not ("username" in args):
        return create_error(1, u"未找到用户名")

    cursor = execute_read("""SELECT user_type FROM user WHERE
      username='%s'
    """ % args["username"])

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()
    if len(result) == 0:
        return create_error(2, u"用户不存在")

    leveltype = result[0][0]
    cursor = execute_read("""SELECT * FROM usertype WHERE
      type_id = %d""" % leveltype)

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()

    search_perminute = result[0][3]
    search_perday = result[0][4]

    cursor1 = execute_read(
        """SELECT COUNT(*) FROM log WHERE UNIX_TIMESTAMP(create_time)>=%d AND type_number=2""" % pre_minute())
    cursor2 = execute_read(
        """SELECT COUNT(*) FROM log WHERE UNIX_TIMESTAMP(create_time)>=%d AND type_number=2""" % pre_day())

    count1 = cursor1.fetchall()[0][0]
    count2 = cursor2.fetchall()[0][0]

    limit1 = execute_read("""SELECT view_perminute FROM usertype WHERE type_id=%d""" % leveltype).fetchall()[0][0]
    limit2 = execute_read("""SELECT view_perday FROM usertype WHERE type_id=%d""" % leveltype).fetchall()[0][0]

    if count1 >= limit1:
        return create_error(73, u"超过分钟数查看限制")

    if count2 >= limit2:
        return create_error(74, u"超过小时数查看限制")

    return create_success("Success")


def add_favor_list(args):
    if not ("username" in args):
        return create_error(1, u"未找到用户名")
    if not ("favor_name" in args):
        return create_error(2, u"未找到收藏夹名字")

    cursor = execute_read("""SELECT * FROM favorite WHERE
      username='%s' AND favorite_name='%s'
    """ % (args["username"], args["favor_name"]))

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()

    if len(result) > 0:
        return create_error(3, u"收藏夹已存在")

    if execute_write("""
      INSERT INTO favorite(username,favorite_name)
      VALUES ('%s','%s')
    """ % (args["username"], args["favor_name"].decode("utf8"))):
        return create_success("Success")
    else:
        return create_error(255, u"未知错误")


def add_search_log(args):
    cursor = execute_write_return_cursor("""
        INSERT INTO log(username,type_number,query_parameter)
        VALUES ('%s',1,'%s')
    """ % (args["username"], json.dumps(args,ensure_ascii = False).replace("'", "\\'").encode("utf8")))

    if cursor is None:
        return create_error(255, u"未知错误")

    return create_success(cursor.lastrowid)


def add_view_log(args):
    if not ("log_id" in args):
        args["log_id"] = ""
    if execute_write("""
        INSERT INTO log(username,type_number,query_parameter,doc_id)
        VALUES ('%s',2,'%s','%s')
    """ % (args["username"], args["log_id"], args["id"])):
        return create_success("Success")
    else:
        return create_error(255, u"未知错误")


def get_favor_list(args):
    if not ("username" in args):
        return create_error(1, u"没有用户名")

    cursor = execute_read(
        """SELECT favorite_id,favorite_name FROM favorite WHERE username = '%s' ORDER BY favorite_id DESC""" % args[
            "username"])

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()

    res = []

    for x in result:
        res.append({"favorite_id": x[0], "favorite_name": x[1]})

    return create_success(res)


def get_favor_list_item(args):
    if not ("favorite_id" in args):
        return create_error(1, u"没有收藏夹id")

    cursor = execute_read(
        """SELECT doc_id FROM favorite_item WHERE favorite_id = %d ORDER BY item_id DESC""" % int(args["favorite_id"]))

    if cursor is None:
        return create_error(255, u"未知错误")

    result = cursor.fetchall()

    res = []

    for x in result:
        res.append({"doc_id": x[0]})

    return create_success(res)


def add_favor_item(args):
    if not ("docid" in args):
        return create_error(1, u"没有文书id")
    if not ("favorite_id" in args):
        return create_error(2, u"没有收藏夹id")

    cursor = execute_read("""
        SELECT COUNT(*) FROM favorite_item WHERE
        favorite_id=%d AND doc_id='%s'
    """ % (int(args["favorite_id"]), args["docid"]))

    if cursor is None:
        return create_error(255, u"未知错误")

    if cursor.fetchall()[0][0] > 0:
        return create_success("Success")

    if execute_write("""
      INSERT INTO favorite_item(favorite_id,doc_id)
      VALUES (%d,'%s')
    """ % (int(args["favorite_id"]), args["docid"])):
        return create_success("Success")
    else:
        return create_error(255, u"未知错误")


def remove_favor_item(args):
    if not ("docid" in args):
        return create_error(1, u"没有文书id")
    if not ("favorite_id" in args):
        return create_error(2, u"没有收藏夹id")

    cursor = execute_read("""
        SELECT COUNT(*) FROM favorite_item WHERE
        favorite_id=%d AND doc_id='%s'
    """ % (int(args["favorite_id"]), args["docid"]))

    if cursor is None:
        return create_error(255, u"未知错误")

    if cursor.fetchall()[0][0] == 0:
        return create_success("Success")

    if execute_write("""
      DELETE FROM favorite_item WHERE
      favorite_id=%d AND doc_id='%s'
    """ % (int(args["favorite_id"]), args["docid"])):
        return create_success("Success")
    else:
        return create_error(255, u"未知错误")


def get_history(args):
    if not ("username" in args):
        return create_error(1, u"没有用户名")

    cursor = execute_read("""
        SELECT * FROM log WHERE username='%s' ORDER BY log_id DESC LIMIT 100
    """ % args["username"])

    if cursor is None:
        return create_error(255, u"未知错误")

    res = cursor.fetchall()
    arr = []
    for a in res:
        arr.append({
            "log_id": a[0],
            "username": a[1],
            "create_time": a[2],
            "type_number": a[3],
            "doc_id": a[4],
            "query_parameter": a[5],
            "user_ip": a[6]
        })

    return create_success(arr)
