import sqlite3 as sqlite
import ModelResults as ModelResults

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
        list = []
        conn = sqlite.connect('DataBase.db')
        cursor = conn.execute("SELECT ID, PUNTOS, NIVEL from RESULTADOS ORDER BY CAST(PUNTOS AS INT) ASC")
        for row in cursor:
            list.append(row[1])

        conn.close()
        return list

    def deleteTable():
        conn = sqlite.connect('DataBase.db')
        conn.execute('DROP TABLE RESULTADOS;')
        conn.close()
