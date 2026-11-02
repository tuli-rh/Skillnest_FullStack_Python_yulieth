from flask_app.config.mysqlconnection import connectToMySQL


class Estudiante:
    def __init__(self, data):
        self.id_estudiante = data["id_estudiante"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.created_at = data["created_at"]

    @classmethod
    def get_all(cls):
        query = """
            SELECT *
            FROM estudiantes
            ORDER BY nombre;
        """

        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query)

        return [cls(estudiante) for estudiante in resultados]

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT *
            FROM estudiantes
            WHERE id_estudiante = %(id_estudiante)s;
        """

        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None