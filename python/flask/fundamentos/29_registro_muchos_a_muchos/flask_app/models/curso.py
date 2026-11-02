from flask_app.config.mysqlconnection import connectToMySQL


class Curso:
    def __init__(self, data):
        self.id_curso = data["id_curso"]
        self.nombre_curso = data["nombre_curso"]
        self.descripcion = data["descripcion"]
        self.created_at = data["created_at"]

    @classmethod
    def get_all(cls):
        query = """
            SELECT *
            FROM cursos
            ORDER BY nombre_curso;
        """

        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query)

        return [cls(curso) for curso in resultados]

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT *
            FROM cursos
            WHERE id_curso = %(id_curso)s;
        """

        resultados = connectToMySQL(
            "esquema_educacion"
        ).query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None