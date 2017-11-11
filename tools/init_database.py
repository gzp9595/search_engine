if __name__ == "__main__":
    import sys
    sys.path.insert(0,"/home/zhx/search_engine/")
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
          create_time DATETIME NOT NULL,
          last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (user_id)
        )"""
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS log(
          log_id INT UNSIGNED AUTO_INCREMENT,
          username VARCHAR(20) NOT NULL,
          create_time DATETIME NOT NULL,
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
          create_time DATETIME NOT NULL,
          PRIMARY KEY (code)
        )"""
    cursor.execute(sql)
