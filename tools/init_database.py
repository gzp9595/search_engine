if __name__ == "__main__":
    import sys

    sys.path.insert(0, "/home/zhx/search_engine/")
    from application import app, initialize

    initialize(False)

    from application.databaser import database

    cursor = database.db.cursor()

    sql = """CREATE TABLE IF NOT EXISTS user(
          user_id  INT UNSIGNED AUTO_INCREMENT,
          username VARCHAR(20) NOT NULL,
          password VARCHAR(5000) NOT NULL,
          nickname VARCHAR(50) NOT NULL,
          rest_money INT NOT NULL DEFAULT 0,
          phone_number VARCHAR(30) NOT NULL,
          mail VARCHAR(100) NOT NULL,
          user_type INT NOT NULL DEFAULT 0,
          user_photo VARCHAR(5000) NOT NULL,
          user_org VARCHAR(100),
          user_identity INT,
          create_time DATETIME NOT NULL,
          last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (user_id)
        )"""
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS log(
          log_id INT UNSIGNED AUTO_INCREMENT,
          username VARCHAR(20) NOT NULL,
          create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
          type_number INT NOT NULL,
          doc_id VARCHAR(60) NOT NULL DEFAULT '',
          query_parameter TEXT NOT NULL,
          user_ip VARCHAR(50) NOT NULL DEFAULT  '',
          PRIMARY KEY (log_id)
        )"""
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS code(
          code VARCHAR(100) NOT NULL,
          leveltype INT NOT NULL DEFAULT 0,
          create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
          PRIMARY KEY (code)
        )"""
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS usertype(
          type_id INT NOT NULL DEFAULT 0,
          search_perminute INT NOT NULL DEFAULT 3,
          search_perday INT NOT NULL DEFAULT 3000,
          view_perminute INT NOT NULL DEFAULT 12,
          view_perday INT NOT NULL DEFAULT 10000,
          PRIMARY KEY (type_id)
        )"""
    cursor.execute(sql)

    for a in range(0, 4):
        sql = """
            INSERT INTO TABLE usertype(type_id,search_perminute,search_perday,view_perminute,view_perday)
            VALUES (%d,%d,%d,%d,%d)
        """ % (a, int(3 * (1.5 ** a)), int(3000 * (1.5 ** a)), int(12 * (1.5 ** a)), int(10000 * (1.5 ** a)))
        cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS favorite(
          favorite_id INT UNSIGNED AUTO_INCREMENT,
          create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL.
          username VARCHAR(20) NOT NULL,
          favoirte_name VARCHAR(20) NOT NULL,
          PRIMARY KEY (favorite_id)
    )"""

    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS favorite_item(
          item_id INT UNSIGNED AUTO_INCREMENT,
          favorite_id INT UNSIGNED NOT NULL,
          doc_id INT UNSIGNED NOT NULL,
          create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
          PRIMARY KEY (item_id)
    )"""

    cursor.execute(sql)