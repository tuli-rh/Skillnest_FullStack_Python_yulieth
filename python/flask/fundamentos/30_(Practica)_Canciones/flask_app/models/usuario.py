from flask_app.config.mysqlconnection import connectToMySQL


class Usuario:

    def __init__(self, data):

        self.id = data["id"]
        self.nombre = data["nombre"]
        self.email = data["email"]
        self.contrasena = data["contrasena"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # Aquí guardaremos las canciones favoritas
        self.favoritos = []


    @classmethod
    def get_all(cls):

        query = """
            SELECT *
            FROM usuarios
            ORDER BY id;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query)

        usuarios = []

        for usuario in resultados:

            usuarios.append(
                cls(usuario)
            )

        return usuarios


    @classmethod
    def save(cls, data):

        query = """
            INSERT INTO usuarios
            (
                nombre,
                email,
                contrasena
            )
            VALUES
            (
                %(nombre)s,
                %(email)s,
                %(contrasena)s
            );
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)


    @classmethod
    def get_by_id(cls, id):

        query = """
            SELECT *
            FROM usuarios
            WHERE id = %(id)s;
        """

        data = {
            "id": id
        }

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)

        if resultados:

            return cls(
                resultados[0]
            )

        return None

    @classmethod
    def get_by_id_with_favorites(cls, data):

        query = """
            SELECT
                usuarios.id AS usuario_id,
                usuarios.nombre AS usuario_nombre,
                usuarios.email AS usuario_email,
                usuarios.contrasena AS usuario_contrasena,
                usuarios.created_at AS usuario_created_at,
                usuarios.updated_at AS usuario_updated_at,

                canciones.id AS cancion_id,
                canciones.titulo AS cancion_titulo,
                canciones.artista AS cancion_artista

            FROM usuarios

            LEFT JOIN favoritos
                ON favoritos.usuario_id = usuarios.id

            LEFT JOIN canciones
                ON favoritos.cancion_id = canciones.id

            WHERE usuarios.id = %(id)s;
        """

        resultados = connectToMySQL(
            "esquema_canciones"
        ).query_db(query, data)


        if not resultados:

            return None


        usuario_data = {

            "id": resultados[0]["usuario_id"],

            "nombre": resultados[0]["usuario_nombre"],

            "email": resultados[0]["usuario_email"],

            "contrasena": resultados[0]["usuario_contrasena"],

            "created_at": resultados[0]["usuario_created_at"],

            "updated_at": resultados[0]["usuario_updated_at"]

        }


        usuario = cls(usuario_data)


        for fila in resultados:

            if fila["cancion_id"] is not None:

                usuario.favoritos.append({

                    "id": fila["cancion_id"],

                    "titulo": fila["cancion_titulo"],

                    "artista": fila["cancion_artista"]

                })


        return usuario
