import mysql.connector
from mysql.connector import Error

cnx = mysql.connector.connect(user='root', password='hibaiich', host='127.0.0.1', database='bearings')

try:
    if cnx.is_connected():
        db_Info = cnx.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        print("Vous êtes connecté au serveur. Bienvenue au système d'identification des roulements GBS.")
        record = cursor.fetchone()
        choice  = input("Tapez 1 pour chercher un roulement, 2 pour ajouter un roulement à la base de données ou 3 pour supprimer un roulement de la base de données: ")
        while(choice!="4"):

            if(choice == "1"):
                print("Calculez le diamètre intérieur, le diamètre extérieur et la largeur du roulement. Les dimensions sont en mm.")

                i = input("Diamètre intérieur: ")
                o = input("Diamètre extérieur: ")
                w = input("Largeur: ")

                sql = "SELECT identification FROM bearings.dim_m WHERE width = %s AND in_diam = %s AND out_diam = %s"

                dim = (w, i, o)

                cursor.execute(sql, dim)
                results = cursor.fetchall()

                if results == []:
                    print("Les dimensions ne correspondent à aucun roulement catalogué.")
                    sql = "SELECT identification FROM bearings.dim_m WHERE width BETWEEN %s AND %s AND in_diam BETWEEN %s AND %s AND out_diam BETWEEN %s AND %s"
                    range = (float(w)*80/100, float(w)*120/100, float(i)*80/100, float(i)*120/100, float(o)*80/100, float(o)*120/100,)
                    cursor.execute(sql, range)
                    r = cursor.fetchmany(10)

                    for result in r:
                        print("Les roulements possibles: ")
                        print(result)
                        print("Veuillez demander de l'assistance auprès d'un employé du magasin.")

                else:
                    for result in results:
                        print("Les roulements correspondants: ")
                        print(result)
                
                choice = input()

            if(choice == "2"):

                print("Entrez les dimensions du nouveau roulement en mm.")

                id = input("Nom du roulement: ")
                i = input("Diamètre intérieur: ")
                o = input("Diamètre extérieur: ")
                w = input("Largeur: ")

                sql = "INSERT INTO bearings.dim_m (identification, in_diam, out_diam, width) VALUES (%s, %s, %s, %s)"
                val = (id, i, o, w)

                cursor.execute(sql, val)

                cnx.commit()

                #print(cnx.rowcount, "entrée(s) finie(s)")

                cursor.execute("SELECT * FROM bearings.dim_m")
                rows = cursor.fetchall()
    
                for row in rows:
                    print(row)
                    print("\n")

            if(choice == "3"):

                t = input("Entrez le nom du roulement à supprimer de la base de données: ")

                sql = "DELETE FROM bearings.dim_m WHERE identification = %s "

                cursor.execute(sql, (t,))
                cnx.commit()

                #print(cnx.rowcount, "entrée(s) supprimée(s)")
                cursor.execute("SELECT * FROM bearings.dim_m")
                rows = cursor.fetchall()
    
                for row in rows:
                    print(row)
                    print("\n")
      
except Error as e:
    print("Error while connecting to MySQL ", e)

finally:
    cursor.close()
    cnx.close()
    print("MySQL connection is closed")
