if __name__ == "__main__":
    from application import app, initialize

    initialize(False)

    from application.databaser import cursor

    sql = """CREATE TABLE IF NOT EXISTS user(
          username VARCHAR(20) NOT NULL,
          password VARCHAR(5000) NOT NULL,
          nickname VARCHAR(50) NOT NULL,
          rest_money INT NOT NULL DEFAULT 0,
          phone_number VARCHAR(30) NOT NULL,
          mail VARCHAR(100) NOT NULL,
          user_type INT NOT NULL DEFAULT 0,
          create_time DATETIME NOT NULL,
          last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          PRIMARY KEY (username)
        )"""
    cursor.execute(sql)
