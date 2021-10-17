import sqlite3 as sqlite

class UtilsDataBase():

    connection = None

    def createTableIfNotExits():
        conn = sqlite.connect('DataBase.db')
        conn.execute('''CREATE TABLE IF NOT EXISTS RESULTADOS
                                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                             PUNTOS INT NOT NULL,
                                             NIVEL INT NOT NULL);''')
        conn.close()

    def insertPointsAndLevel(points, level):
        conn = sqlite.connect('DataBase.db')
        conn.execute("INSERT INTO RESULTADOS (PUNTOS, NIVEL) VALUES ("+ str(points)+","+str(level)+")")
        conn.commit()
        conn.close()

    def selectAllTable():
        conn = sqlite.connect('DataBase.db')
        cursor = conn.execute("SELECT ID, PUNTOS, NIVEL from RESULTADOS")
        for row in cursor:
            print("ID = ", row[0])
            print("PUNTOS = ", row[1])
            print("NIVEL = ", row[2])

        conn.close()
        

    def deleteTable():
        conn = sqlite.connect('DataBase.db')
        conn.execute('DROP TABLE RESULTADOS;')
        conn.close()