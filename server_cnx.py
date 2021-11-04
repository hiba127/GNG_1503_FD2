import mysql.connector
from mysql.connector import Error

cnx = mysql.connector.connect(user='root', password='hibaiich', host='127.0.0.1', database='bearings')

try:
    if cnx.is_connected():
        db_Info = cnx.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        i = input("Enter your inside diameter in metric: ")
        o = input("Enter your outside diameter in metric: ")
        w = input("Enter your width in metric: ")

        sql = "SELECT identification FROM bearings.dim_m WHERE width = %s AND in_diam = %s AND out_diam = %s"

        dim = (w, i, o)

        cursor.execute(sql, dim)
        results = cursor.fetchall()

        for result in results:
            print(result)

except Error as e:
    print("Error while connecting to MySQL ", e)

finally:
    cursor.close()
    cnx.close()
    print("MySQL connection is closed")
