if __name__ == "__main__":
    import sys

    sys.path.insert(0, "/home/zhx/search_engine/")
    from application import app, initialize

    initialize(False)

    from application.databaser import database

    table_list = ["user", "code", "log", "usertype", "favorite", "favorite_item", "charge"]

    cursor = database.db.cursor()

    for x in table_list:
        sql = """DROP TABLE %s IF EXISTS""" % x
        cursor.execute(sql)
