from flask_app.config.mysqlconnection import connectToMySQL


class Taco:

    def __init__(self, data):

        self.id = data["id"]
        self.tortilla = data["tortilla"]
        self.guiso = data["guiso"]
        self.salsa = data["salsa"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def save(cls, datos):

        query = """
            INSERT INTO tacos
            (
                tortilla,
                guiso,
                salsa
            )
            VALUES
            (
                %(tortilla)s,
                %(guiso)s,
                %(salsa)s
            );
        """

        return connectToMySQL(
            "esquema_tacos"
        ).query_db(query, datos)


    @classmethod
    def get_all(cls):

        query = """
            SELECT
                id,
                tortilla,
                guiso,
                salsa,
                created_at,
                updated_at
            FROM tacos
            ORDER BY id;
        """

        resultados = connectToMySQL(
            "esquema_tacos"
        ).query_db(query)

        tacos = []

        for taco in resultados:

            tacos.append(
                cls(taco)
            )

        return tacos


    @classmethod
    def get_one(cls, datos):

        query = """
            SELECT
                id,
                tortilla,
                guiso,
                salsa,
                created_at,
                updated_at
            FROM tacos
            WHERE id = %(id)s;
        """

        resultado = connectToMySQL(
            "esquema_tacos"
        ).query_db(query, datos)

        if not resultado:

            return None

        return cls(resultado[0])


    @classmethod
    def update(cls, datos):

        query = """
            UPDATE tacos
            SET
                tortilla = %(tortilla)s,
                guiso = %(guiso)s,
                salsa = %(salsa)s
            WHERE id = %(id)s;
        """

        return connectToMySQL(
            "esquema_tacos"
        ).query_db(query, datos)


    @classmethod
    def delete(cls, datos):

        query = """
            DELETE FROM tacos
            WHERE id = %(id)s;
        """

        return connectToMySQL(
            "esquema_tacos"
        ).query_db(query, datos)