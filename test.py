# from flask import Flask, jsonify
# import mysql.connector

# app = Flask(__name__)

# # MySQL Connection setup
# db = mysql.connector.connect(
#     host="localhost", user="root", password="av.en.u4aie22060", database="m"
# )
# cursor = db.cursor(dictionary=True)


# # cursor.execute("SELECT * FROM mani")
# # rows = cursor.fetchall()
# # print(rows)
# @app.route("/get-users")
# def get_users():
#     cursor = db.cursor(dictionary=True)
#     cursor.execute(
#         """SELECT * FROM mani
#                    where depid =11 """
#     )
#     rows = cursor.fetchall()
#     return jsonify(rows)


# if __name__ == "__main__":
#     app.run(debug=True)
# # import sqlite3
# # from flask import Flask, jsonify

# # app = Flask(__name__)


# # @app.route("/get-users")
# # def get_users():
# #     c = sqlite3.connect("test.db")
# #     c.row_factory = sqlite3.Row
# #     cursor = c.cursor()
# #     cursor.execute("select * from department where dep=1;")
# #     r = cursor.fetchall()
# #     c.close()
# #     return r


# # if __name__ == "__main__":
# #     app.run(debug=True)
import mysql.connector

db = {
    "host": "localhost",
    "user": "root",
    "password": "av.en.u4aie22060",
    "database": "auth",
}

try:
    print("Script started!")
    dbc = mysql.connector.connect(
        host="localhost",
        user="root",
        password="av.en.u4aie22060",
    )
    myconn = dbc.cursor()
    myconn.execute("show databases")
    print("Connected to MySQL!")
    dbc.close()
except mysql.connector.Error as e:
    print("Failed to connect:", e)
