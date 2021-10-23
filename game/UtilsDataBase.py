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
        list = []
        conn = sqlite.connect('DataBase.db')
        cursor = conn.execute("SELECT ID, PUNTOS, NIVEL from RESULTADOS ORDER BY CAST(PUNTOS AS INT) DESC LIMIT 5")
        for row in cursor:
            list.append(str(row[1]) + " con nivel " + str(row[2]))

        conn.close()
        return list

    def resetTable():
        conn = sqlite.connect('DataBase.db')
        conn.execute('DROP TABLE IF EXISTS RESULTADOS;')
        conn.close()
        UtilsDataBase.createTableIfNotExits()
