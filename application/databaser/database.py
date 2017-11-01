from application import app
import MySQLdb

db = MySQLdb.connect(app.config["DATABASE_IP"], app.config["DATABASE_USER"], app.config["DATABASE_PASS"],app.config["DATABASE_NAME"])

cursor = db.cursor()