import mysql.connector
from mysql.connector import Error

cnx = mysql.connector.connect(user='m', password='hibaiich', host='192.168.0.65', database='bearings')

try:
    if cnx.is_connected():
        db_Info = cnx.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        print("Vous êtes connecté au serveur. Bienvenue au système d'identification des roulements GBS.")
        print("You are connected to the server. Welcome to the GBS bearing identification system.")
        record = cursor.fetchone()
        print("Tapez 1 pour chercher un roulement, 2 pour ajouter un roulement à la base de données, 3 pour supprimer un roulement de la base de données, ou 4 pour arrêter le programme. ")
        choice  = input("Input 1 to identify a bearing, 2 to add a bearing to the database, 3 to delete a bearing from the database, or 4 to stop the program: ")
        while(choice!="4"):

            if(choice == "1"):
                print("Entrez le diamètre intérieur, le diamètre extérieur et la largeur du roulement. Les dimensions sont en mm.")
                print("Enter the inner diameter, the outer diameter and the width of the bearing to be identified. The dimensions should be in mm.")

                i = input("Diamètre intérieur/Inner diameter: ")
                o = input("Diamètre extérieur/Outer diameter: ")
                w = input("Largeur/Width: ")

                sql = "SELECT identification FROM bearings.ball WHERE width = %s AND in_diam = %s AND out_diam = %s"

                dim = (w, i, o)

                cursor.execute(sql, dim)
                results = cursor.fetchall()

                if results == []:
                    print("Les dimensions ne correspondent à aucun roulement catalogué.")
                    print("These dimensions do not match any bearing in our catalogue.")
                    sql = "SELECT identification FROM bearings.ball WHERE width BETWEEN %s AND %s AND in_diam BETWEEN %s AND %s AND out_diam BETWEEN %s AND %s"
                    range = (float(w)*80/100, float(w)*120/100, float(i)*80/100, float(i)*120/100, float(o)*80/100, float(o)*120/100,)
                    cursor.execute(sql, range)
                    r = cursor.fetchmany(10)

                    print("Des roulements possibles (intervalle de confiance = 80%).")
                    print("Possible bearings (confidence interval = 80%): ")

                    for result in r:
                        print(result)
                        
                    print("Veuillez demander de l'assistance auprès d'un employé du magasin.")
                    print("Please request assistance from one the employees on site.")

                else:
                    print("Les roulements correspondants.")
                    print("Identified bearings:")
                    for result in results:
                        print(result)
                
                choice = input("Vous pouvez exécuter une autre tache, ou arrêter le programme. You can start another task, or quit the program: ")

            if(choice == "2"):

                print("Entrez les dimensions du nouveau roulement en mm.")
                print("Enter the dimensions of the new bearing in mm.")

                id = input("Nom du roulement/Name of the bearing: ")
                i = input("Diamètre intérieur/Inner diameter: ")
                o = input("Diamètre extérieur/Outer diameter: ")
                w = input("Largeur/Width: ")

                sql = "INSERT INTO bearings.ball (identification, in_diam, out_diam, width) VALUES (%s, %s, %s, %s)"
                val = (id, i, o, w)

                cursor.execute(sql, val)

                cnx.commit()
                print("Le roulement est ajouté. The bearing is added.")

                #print(cnx.rowcount, "entrée(s) finie(s)")

                cursor.execute("SELECT * FROM bearings.ball")
                rows = cursor.fetchall()
    
                #for row in rows:
                   # print(row)
                   # print("\n")
                choice = input("Vous pouvez exécuter une autre tache, ou arrêter le programme. You can start another task, or quit the program: ")

            if(choice == "3"):

                print("Enter the name of the bearing to be deleted from the database.")
                t = input("Entrez le nom du roulement à supprimer de la base de données: ")

                sql = "DELETE FROM bearings.ball WHERE identification = %s "

                cursor.execute(sql, (t,))
                cnx.commit()
                print("Le roulement est supprimé. The bearing is deleted.")

                #print(cnx.rowcount, "entrée(s) supprimée(s)")
                cursor.execute("SELECT * FROM bearings.ball")
                rows = cursor.fetchall()
    
                #for row in rows:
                  #  print(row)
                  #  print("\n")
                choice = input("Vous pouvez exécuter une autre tache, ou arrêter le programme. You can start another task, or quit the program: ")
      
except Error as e:
    print("Error while connecting to MySQL ", e)

finally:
    cursor.close()
    cnx.close()
    print("MySQL connection is closed.")
