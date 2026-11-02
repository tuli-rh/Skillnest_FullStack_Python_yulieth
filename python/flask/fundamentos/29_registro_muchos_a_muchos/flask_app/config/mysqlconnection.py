import pymysql.cursors


class MySQLConnection:
    def __init__(self, nombre_base_datos):
        self.nombre_base_datos = nombre_base_datos

    def connect(self):
        return pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database=self.nombre_base_datos,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        conexion = self.connect()

        try:
            with conexion.cursor() as cursor:
                cursor.execute(query, data or {})

                if query.strip().lower().startswith("select"):
                    resultado = cursor.fetchall()
                else:
                    resultado = cursor.rowcount

            return resultado

        finally:
            conexion.close()


def connectToMySQL(nombre_base_datos):
    return MySQLConnection(nombre_base_datos)