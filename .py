import mysql.connector
from mysql.connector import Error

try:
    # Establish the connection
    mydb = mysql.connector.connect(host="localhost", user="root", database="auth")

    if mydb.is_connected():
        print("Successfully connected to MySQL database!")
        # Perform your database operations here

except Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    # Close the connection when done
    if "mydb" in locals() and mydb.is_connected():
        mydb.close()
        print("MySQL connection closed.")
