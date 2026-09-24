from mysqlconnection import connectToMySQL


class Mascota:

    def __init__(self, data):

        self.id = data["id"]
        self.nombre = data["nombre"]
        self.tipo = data["tipo"]
        self.color = data["color"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):

        query = """
            SELECT *
            FROM mascotas;
        """

        resultados = connectToMySQL(
            "primera_flask"
        ).query_db(query)

        mascotas = []

        for mascota in resultados:

            mascotas.append(
                cls(mascota)
            )

        return mascotas