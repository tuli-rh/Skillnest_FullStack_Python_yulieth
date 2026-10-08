Estudiantes y Cursos — Core
Descripción
Aplicación web desarrollada con Flask + MySQL + PyMySQL + Jinja2 + Bootstrap para administrar cursos y estudiantes.
La aplicación implementa una relación uno a muchos (1:N):
CURSOS
   │
   │ 1
   │
   │ N
   ▼
ESTUDIANTES
Un curso puede tener varios estudiantes y cada estudiante pertenece a un curso.

🎯 Objetivo
Practicar:
conexión entre Flask y MySQL;
arquitectura MVC;
POO;
relaciones 1:N;
claves foráneas;
formularios POST;
request.form;
consultas preparadas;
JOIN;
Jinja2;
navegación mediante url_for();
redirecciones con redirect();
Bootstrap.

🗃️ Modelo de datos
Tabla cursos
cursos
├── id
├── nombre
├── created_at
└── updated_at
Tabla estudiantes
estudiantes
├── id
├── nombre
├── apellido
├── edad
├── created_at
├── updated_at
└── curso_id → cursos.id
Relación
cursos.id
     ▲
     │
     │ FOREIGN KEY
     │
estudiantes.curso_id
Un curso:
1
puede estar asociado con:
N estudiantes

📁 Estructura del proyecto
ESTUDIANTES_CURSOS/
│
├── flask_app/
│   │
│   ├── __init__.py
│   │
│   ├── config/
│   │   └── mysqlconnection.py
│   │
│   ├── controllers/
│   │   ├── cursos.py
│   │   └── estudiantes.py
│   │
│   ├── models/
│   │   ├── curso.py
│   │   └── estudiante.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── cursos.html
│   │   ├── nuevo_estudiante.html
│   │   └── mostrar_curso.html
│   │
│   └── static/
│       └── css/
│           └── style.css
│
├── resources/
│   └── esquema_estudiantes_cursos_erd.mwb
│
├── flask_app/bd/
│   └── esquema_estudiantes_cursos.sql
│
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
flask_app/__init__.py es el archivo de inicialización principal. Las carpetas templates, static y resources no requieren __init__.py.

🧰 Tecnologías
Python
Flask
MySQL
PyMySQL
Jinja2
Bootstrap 5
Pipenv

🐍 Configuración con Pipenv
Instalar:
pipenv install flask pymysql
Activar entorno:
pipenv shell
Ejecutar:
python server.py

📄 Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
pymysql = "*"

[dev-packages]

[requires]
python_version = "3"

🚫 .gitignore
__pycache__/
*.pyc
.venv/
venv/
.DS_Store

🗄️ Base de datos
flask_app/bd/esquema_estudiantes_cursos.sql
-- ==========================================================
-- CREACIÓN DE LA BASE DE DATOS
-- ==========================================================

CREATE DATABASE IF NOT EXISTS esquema_estudiantes_cursos;

USE esquema_estudiantes_cursos;


-- ==========================================================
-- TABLA CURSOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);


-- ==========================================================
-- TABLA ESTUDIANTES
-- ==========================================================

CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    apellido VARCHAR(45) NOT NULL,
    edad INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    curso_id INT NOT NULL,

    CONSTRAINT fk_estudiantes_curso
        FOREIGN KEY (curso_id)
        REFERENCES cursos(id)
);


-- ==========================================================
-- DATOS DE PRUEBA
-- ==========================================================

INSERT INTO cursos
(nombre)
VALUES
("MERN"),
("Java"),
("Python"),
("Fundamentos de la Web");


INSERT INTO estudiantes
(nombre, apellido, edad, curso_id)
VALUES
("Valeria", "Romero", 25, 1),
("Cynthia", "Castillo", 26, 1),
("Patricio", "Fuentelba", 27, 1),
("Kevin", "Duque", 27, 1),
("Andrea", "Pérez", 22, 2),
("Matías", "Soto", 24, 3);

📐 ERD
El ERD debe representar:
┌─────────────────────┐
│       cursos        │
├─────────────────────┤
│ PK id               │
│ nombre              │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────┐
│    estudiantes      │
├─────────────────────┤
│ PK id               │
│ nombre              │
│ apellido            │
│ edad                │
│ created_at          │
│ updated_at          │
│ FK curso_id         │
└─────────────────────┘
Guardar el archivo del ERD en:
resources/esquema_estudiantes_cursos_erd.mwb

⚙️ Inicialización Flask
flask_app/__init__.py
from flask import Flask

app = Flask(__name__)

🔌 Conexión MySQL
flask_app/config/mysqlconnection.py
import pymysql
import pymysql.cursors


class MySQLConnection:
    """
    Gestiona la conexión entre Flask y MySQL.
    """

    def __init__(self, db):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )


    def query_db(self, query, data=None):
        """
        Ejecuta la consulta SQL recibida.
        """

        with self.connection.cursor() as cursor:

            try:

                cursor.execute(
                    query,
                    data or {}
                )

                tipo_consulta = query.strip().lower()


                if tipo_consulta.startswith("select"):

                    return cursor.fetchall()


                if tipo_consulta.startswith("insert"):

                    return cursor.lastrowid


                return cursor.rowcount


            except Exception as e:

                print(
                    "Error en MySQL:",
                    e
                )

                return False


            finally:

                self.connection.close()


def connectToMySQL(db):
    """
    Crea una instancia de MySQLConnection.
    """

    return MySQLConnection(db)
Modifica user y password según tu instalación local de MySQL.

📘 Modelo Curso
flask_app/models/curso.py
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.estudiante import Estudiante


class Curso:
    """
    Representa un registro de la tabla cursos.
    """

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.estudiantes = []


    @classmethod
    def get_all(cls):
        """
        Obtiene todos los cursos.
        """

        query = """
            SELECT
                id,
                nombre,
                created_at,
                updated_at
            FROM cursos
            ORDER BY nombre;
        """


        resultados = connectToMySQL(
            "esquema_estudiantes_cursos"
        ).query_db(query)


        cursos = []


        for curso in resultados:

            cursos.append(
                cls(curso)
            )


        return cursos


    @classmethod
    def save(cls, data):
        """
        Crea un nuevo curso.
        """

        query = """
            INSERT INTO cursos
            (
                nombre
            )
            VALUES
            (
                %(nombre)s
            );
        """


        return connectToMySQL(
            "esquema_estudiantes_cursos"
        ).query_db(
            query,
            data
        )


    @classmethod
    def get_curso_con_estudiantes(cls, curso_id):
        """
        Obtiene un curso junto con todos
        los estudiantes asociados.

        Se utiliza LEFT JOIN para conservar
        el curso aunque todavía no tenga estudiantes.
        """

        query = """
            SELECT
                c.id AS curso_id,
                c.nombre AS curso_nombre,
                c.created_at AS curso_created_at,
                c.updated_at AS curso_updated_at,

                e.id AS estudiante_id,
                e.nombre AS estudiante_nombre,
                e.apellido AS estudiante_apellido,
                e.edad AS estudiante_edad,
                e.created_at AS estudiante_created_at,
                e.updated_at AS estudiante_updated_at

            FROM cursos c

            LEFT JOIN estudiantes e
                ON c.id = e.curso_id

            WHERE c.id = %(id)s;
        """


        data = {
            "id": curso_id
        }


        resultados = connectToMySQL(
            "esquema_estudiantes_cursos"
        ).query_db(
            query,
            data
        )


        if not resultados:

            return None


        curso_data = {
            "id": resultados[0]["curso_id"],
            "nombre": resultados[0]["curso_nombre"],
            "created_at": resultados[0]["curso_created_at"],
            "updated_at": resultados[0]["curso_updated_at"]
        }


        curso = cls(curso_data)


        for fila in resultados:

            if fila["estudiante_id"] is not None:

                estudiante_data = {
                    "id": fila["estudiante_id"],
                    "nombre": fila["estudiante_nombre"],
                    "apellido": fila["estudiante_apellido"],
                    "edad": fila["estudiante_edad"],
                    "created_at": fila["estudiante_created_at"],
                    "updated_at": fila["estudiante_updated_at"],
                    "curso_id": curso.id
                }


                curso.estudiantes.append(
                    Estudiante(estudiante_data)
                )


        return curso

👨‍🎓 Modelo Estudiante
flask_app/models/estudiante.py
from flask_app.config.mysqlconnection import connectToMySQL


class Estudiante:
    """
    Representa un registro de la tabla estudiantes.
    """

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.edad = data["edad"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.curso_id = data["curso_id"]


    @classmethod
    def save(cls, data):
        """
        Crea un nuevo estudiante
        asociado a un curso.
        """

        query = """
            INSERT INTO estudiantes
            (
                nombre,
                apellido,
                edad,
                curso_id
            )
            VALUES
            (
                %(nombre)s,
                %(apellido)s,
                %(edad)s,
                %(curso_id)s
            );
        """


        return connectToMySQL(
            "esquema_estudiantes_cursos"
        ).query_db(
            query,
            data
        )

🎮 Controlador de Cursos
flask_app/controllers/cursos.py
from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_app.models.curso import Curso


# ==========================================================
# PÁGINA PRINCIPAL
# ==========================================================

@app.route("/")
def inicio():
    """
    Redirige la raíz hacia la página de cursos.
    """

    return redirect(
        url_for("cursos")
    )


# ==========================================================
# MOSTRAR TODOS LOS CURSOS
# ==========================================================

@app.route("/cursos")
def cursos():
    """
    Obtiene y muestra todos los cursos.
    """

    todos_los_cursos = Curso.get_all()


    return render_template(
        "cursos.html",
        cursos=todos_los_cursos
    )


# ==========================================================
# CREAR CURSO
# ==========================================================

@app.route(
    "/cursos/crear",
    methods=["POST"]
)
def crear_curso():
    """
    Recibe el nombre del curso
    y crea un nuevo registro.
    """

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()


    if not nombre:

        return redirect(
            url_for("cursos")
        )


    data = {
        "nombre": nombre
    }


    Curso.save(data)


    return redirect(
        url_for("cursos")
    )


# ==========================================================
# MOSTRAR CURSO
# ==========================================================

@app.route(
    "/cursos/<int:id>"
)
def mostrar_curso(id):
    """
    Obtiene un curso y sus estudiantes.
    """

    curso = Curso.get_curso_con_estudiantes(id)


    if curso is None:

        return redirect(
            url_for("cursos")
        )


    return render_template(
        "mostrar_curso.html",
        curso=curso
    )

🎓 Controlador de Estudiantes
flask_app/controllers/estudiantes.py
from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for
)

from flask_app.models.curso import Curso
from flask_app.models.estudiante import Estudiante


# ==========================================================
# FORMULARIO NUEVO ESTUDIANTE
# ==========================================================

@app.route("/estudiantes/nuevo")
def nuevo_estudiante():
    """
    Obtiene todos los cursos para mostrarlos
    dentro del select del formulario.
    """

    cursos = Curso.get_all()


    return render_template(
        "nuevo_estudiante.html",
        cursos=cursos
    )


# ==========================================================
# CREAR ESTUDIANTE
# ==========================================================

@app.route(
    "/estudiantes/crear",
    methods=["POST"]
)
def crear_estudiante():
    """
    Recibe los datos del formulario
    y crea un nuevo estudiante.
    """

    nombre = request.form.get(
        "nombre",
        ""
    ).strip()


    apellido = request.form.get(
        "apellido",
        ""
    ).strip()


    edad = request.form.get(
        "edad",
        ""
    ).strip()


    curso_id = request.form.get(
        "curso_id",
        ""
    ).strip()


    if not nombre or not apellido or not edad or not curso_id:

        return redirect(
            url_for("nuevo_estudiante")
        )


    try:

        edad = int(edad)
        curso_id = int(curso_id)

    except ValueError:

        return redirect(
            url_for("nuevo_estudiante")
        )


    data = {
        "nombre": nombre,
        "apellido": apellido,
        "edad": edad,
        "curso_id": curso_id
    }


    Estudiante.save(data)


    return redirect(
        url_for("cursos")
    )

🧱 Template base
flask_app/templates/base.html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        {% block title %}Estudiantes y Cursos{% endblock %}
    </title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <link
        rel="stylesheet"
        href="{{ url_for(
            'static',
            filename='css/style.css'
        ) }}"
    >

</head>

<body>

<nav class="navbar navbar-dark bg-dark">

    <div class="container">

        <a
            class="navbar-brand"
            href="{{ url_for('cursos') }}"
        >
            Estudiantes y Cursos
        </a>

    </div>

</nav>


<main class="container py-5">

    {% block content %}

    {% endblock %}

</main>


<script
    src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
></script>

</body>

</html>

📚 Página Cursos
flask_app/templates/cursos.html
{% extends "base.html" %}

{% block title %}
Cursos
{% endblock %}

{% block content %}

<div class="row g-4">

    <!-- ==================================================
         NUEVO CURSO
    =================================================== -->

    <div class="col-lg-5">

        <div class="card shadow-sm h-100">

            <div class="card-body">

                <h1 class="h3 mb-4">
                    Nuevo Curso
                </h1>


                <form
                    action="{{ url_for('crear_curso') }}"
                    method="POST"
                >

                    <div class="mb-3">

                        <label
                            for="nombre"
                            class="form-label"
                        >
                            Nombre
                        </label>


                        <input
                            type="text"
                            id="nombre"
                            name="nombre"
                            class="form-control"
                            required
                        >

                    </div>


                    <button
                        type="submit"
                        class="btn btn-success"
                    >
                        Crear
                    </button>

                </form>

            </div>

        </div>

    </div>


    <!-- ==================================================
         TODOS LOS CURSOS
    =================================================== -->

    <div class="col-lg-7">

        <div class="card shadow-sm h-100">

            <div class="card-body">

                <h2 class="h3 mb-4">
                    Todos los Cursos
                </h2>


                {% if cursos %}

                    <div class="list-group">

                        {% for curso in cursos %}

                            <a
                                href="{{ url_for(
                                    'mostrar_curso',
                                    id=curso.id
                                ) }}"
                                class="list-group-item list-group-item-action"
                            >

                                {{ curso.nombre }}

                            </a>

                        {% endfor %}

                    </div>

                {% else %}

                    <div class="alert alert-info">
                        No existen cursos registrados.
                    </div>

                {% endif %}


                <div class="mt-4">

                    <a
                        href="{{ url_for('nuevo_estudiante') }}"
                        class="btn btn-primary"
                    >
                        Agregar Estudiante
                    </a>

                </div>

            </div>

        </div>

    </div>

</div>

{% endblock %}

👨‍🎓 Página Nuevo Estudiante
flask_app/templates/nuevo_estudiante.html
{% extends "base.html" %}

{% block title %}
Nuevo Estudiante
{% endblock %}

{% block content %}

<div class="row justify-content-center">

    <div class="col-lg-7">

        <div class="card shadow-sm">

            <div class="card-body">

                <h1 class="h3 mb-4">
                    Nuevo Estudiante
                </h1>


                <form
                    action="{{ url_for('crear_estudiante') }}"
                    method="POST"
                >


                    <!-- CURSO -->

                    <div class="mb-3">

                        <label
                            for="curso_id"
                            class="form-label"
                        >
                            Curso
                        </label>


                        <select
                            id="curso_id"
                            name="curso_id"
                            class="form-select"
                            required
                        >

                            <option value="">
                                Selecciona un curso
                            </option>


                            {% for curso in cursos %}

                                <option
                                    value="{{ curso.id }}"
                                >
                                    {{ curso.nombre }}
                                </option>

                            {% endfor %}

                        </select>

                    </div>


                    <!-- NOMBRE -->

                    <div class="mb-3">

                        <label
                            for="nombre"
                            class="form-label"
                        >
                            Nombre
                        </label>


                        <input
                            type="text"
                            id="nombre"
                            name="nombre"
                            class="form-control"
                            required
                        >

                    </div>


                    <!-- APELLIDO -->

                    <div class="mb-3">

                        <label
                            for="apellido"
                            class="form-label"
                        >
                            Apellido
                        </label>


                        <input
                            type="text"
                            id="apellido"
                            name="apellido"
                            class="form-control"
                            required
                        >

                    </div>


                    <!-- EDAD -->

                    <div class="mb-4">

                        <label
                            for="edad"
                            class="form-label"
                        >
                            Edad
                        </label>


                        <input
                            type="number"
                            id="edad"
                            name="edad"
                            class="form-control"
                            min="1"
                            required
                        >

                    </div>


                    <button
                        type="submit"
                        class="btn btn-success"
                    >
                        Crear
                    </button>


                    <a
                        href="{{ url_for('cursos') }}"
                        class="btn btn-outline-secondary"
                    >
                        Inicio
                    </a>

                </form>

            </div>

        </div>

    </div>

</div>

{% endblock %}

🔎 Página Mostrar Curso
flask_app/templates/mostrar_curso.html
{% extends "base.html" %}

{% block title %}
{{ curso.nombre }}
{% endblock %}

{% block content %}

<div class="d-flex justify-content-between align-items-center mb-4">

    <div>

        <h1 class="mb-1">
            Estudiantes de {{ curso.nombre }}
        </h1>

        <p class="text-muted mb-0">
            Estudiantes asociados al curso seleccionado.
        </p>

    </div>


    <a
        href="{{ url_for('cursos') }}"
        class="btn btn-outline-primary"
    >
        Inicio
    </a>

</div>


<div class="card shadow-sm">

    <div class="card-body p-0">


        {% if curso.estudiantes %}

            <div class="table-responsive">

                <table class="table table-striped table-hover mb-0">

                    <thead class="table-dark">

                        <tr>

                            <th>
                                Nombre
                            </th>

                            <th>
                                Apellido
                            </th>

                            <th>
                                Edad
                            </th>

                        </tr>

                    </thead>


                    <tbody>

                        {% for estudiante in curso.estudiantes %}

                            <tr>

                                <td>
                                    {{ estudiante.nombre }}
                                </td>

                                <td>
                                    {{ estudiante.apellido }}
                                </td>

                                <td>
                                    {{ estudiante.edad }}
                                </td>

                            </tr>

                        {% endfor %}

                    </tbody>

                </table>

            </div>


        {% else %}

            <div class="p-4">

                <div class="alert alert-info mb-0">

                    Este curso todavía no tiene estudiantes.

                </div>

            </div>

        {% endif %}


    </div>

</div>

{% endblock %}

🎨 CSS
flask_app/static/css/style.css
body {
    background-color: #f5f6f8;
    color: #212529;
    font-family: Arial, Helvetica, sans-serif;
}

.navbar-brand {
    font-weight: 700;
}

.card {
    border: none;
    border-radius: 12px;
}

.form-control,
.form-select {
    border-radius: 8px;
}

.btn {
    border-radius: 8px;
}

.list-group-item {
    border-radius: 8px !important;
    margin-bottom: 8px;
}

.table {
    vertical-align: middle;
}

@media (max-width: 768px) {

    .container {
        padding-left: 16px;
        padding-right: 16px;
    }

}

🚀 server.py
from flask_app import app

# Importamos los controladores para registrar las rutas.
from flask_app.controllers import cursos
from flask_app.controllers import estudiantes


if __name__ == "__main__":
    app.run(debug=True)

🗺️ Rutas
Método
Ruta
Función
GET
/
Redirige a /cursos
GET
/cursos
Lista cursos
POST
/cursos/crear
Crea un curso
GET
/cursos/<id>
Muestra un curso y sus estudiantes
GET
/estudiantes/nuevo
Formulario de estudiante
POST
/estudiantes/crear
Crea un estudiante


🔄 Flujo de cursos
GET /
  ↓
redirect()
  ↓
/cursos
  ↓
Curso.get_all()
  ↓
MySQL
  ↓
cursos.html
Crear curso:
Formulario
    ↓
POST /cursos/crear
    ↓
request.form
    ↓
data
    ↓
Curso.save()
    ↓
INSERT
    ↓
redirect()
    ↓
/cursos

🔄 Flujo de estudiante
/cursos
    ↓
Agregar Estudiante
    ↓
/estudiantes/nuevo
    ↓
Curso.get_all()
    ↓
<select>
    ↓
seleccionar curso
    ↓
POST /estudiantes/crear
    ↓
request.form
    ↓
Estudiante.save()
    ↓
INSERT
    ↓
redirect()
    ↓
/cursos

🔗 Flujo de la relación 1:N
Supongamos:
MERN
id = 1
Al crear:
Valeria
Romero
25
curso_id = 1
MySQL guarda:
estudiantes

id | nombre  | apellido | edad | curso_id
---|---------|----------|------|---------
1  | Valeria | Romero   | 25   | 1
El 1 de curso_id corresponde a:
cursos.id = 1
Por lo tanto:
MERN
  │
  ├── Valeria Romero
  ├── Cynthia Castillo
  ├── Patricio Fuentelba
  └── Kevin Duque

🔍 Consulta utilizada para mostrar el curso
En:
models/curso.py
se utiliza:
SELECT
    c.id AS curso_id,
    c.nombre AS curso_nombre,

    e.id AS estudiante_id,
    e.nombre AS estudiante_nombre,
    e.apellido AS estudiante_apellido,
    e.edad AS estudiante_edad

FROM cursos c

LEFT JOIN estudiantes e
    ON c.id = e.curso_id

WHERE c.id = %(id)s;
La consulta permite obtener:
Curso
+
Estudiantes asociados

🧠 ¿Por qué usamos LEFT JOIN?
Porque queremos obtener el curso incluso cuando todavía no tiene estudiantes.
Por ejemplo:
Python
puede existir en la base de datos sin estudiantes.
Con:
LEFT JOIN
el curso seguirá apareciendo.
La aplicación mostrará:
Este curso todavía no tiene estudiantes.

🧩 ¿Por qué usamos alias?
En la consulta utilizamos:
cursos c
y:
estudiantes e
Por ejemplo:
c.id
corresponde al curso.
Mientras:
e.id
corresponde al estudiante.
También usamos alias de columnas:
c.id AS curso_id
e.id AS estudiante_id
Esto evita confundir los campos provenientes de las dos tablas.

📋 Jinja2
Para recorrer los cursos:
{% for curso in cursos %}
    {{ curso.nombre }}
{% endfor %}
Para recorrer los estudiantes:
{% for estudiante in curso.estudiantes %}
    {{ estudiante.nombre }}
{% endfor %}
El controlador entrega objetos Python y Jinja2 los presenta en HTML.

🔗 url_for()
Para ir a cursos:
{{ url_for('cursos') }}
Para nuevo estudiante:
{{ url_for('nuevo_estudiante') }}
Para mostrar un curso:
{{ url_for('mostrar_curso', id=curso.id) }}
Para crear:
{{ url_for('crear_curso') }}
y:
{{ url_for('crear_estudiante') }}

🧠 Correspondencia entre HTML y Flask
Curso
HTML:
<input
    type="text"
    name="nombre"
>
Flask:
request.form["nombre"]

Estudiante
HTML:
<input
    type="text"
    name="nombre"
>
<input
    type="text"
    name="apellido"
>
<input
    type="number"
    name="edad"
>
<select name="curso_id">
Flask:
request.form["nombre"]
request.form["apellido"]
request.form["edad"]
request.form["curso_id"]

🧪 Datos de prueba
La base de datos inicia con:
MERN
Java
Python
Fundamentos de la Web
Y estudiantes:
Valeria Romero     25 → MERN
Cynthia Castillo   26 → MERN
Patricio Fuentelba 27 → MERN
Kevin Duque        27 → MERN
Andrea Pérez       22 → Java
Matías Soto        24 → Python

✅ Pruebas funcionales
Crear un curso
Ingresar:
Nombre:
PHP
Resultado:
PHP
debe aparecer en:
/cursos

Crear un estudiante
Seleccionar:
Curso:
PHP
Ingresar:
Nombre:
Carlos

Apellido:
González

Edad:
20
Después de crear:
redirect → /cursos

Mostrar curso
Seleccionar:
PHP
Debe aparecer:
Estudiantes de PHP

Nombre      Apellido     Edad
Carlos      González     20

📌 Relación final
La aplicación implementa:
                   CURSOS
                       │
                       │ 1
                       │
                       │
                       │ N
                       ▼
                 ESTUDIANTES
La relación se almacena mediante:
estudiantes.curso_id
que referencia:
cursos.id

🧠 Arquitectura MVC
               NAVEGADOR
                    │
                    ▼
               CONTROLLERS
              /            \
             ▼              ▼
         CURSO MODEL   ESTUDIANTE MODEL
             │              │
             └──────┬───────┘
                    ▼
                  MySQL
                    │
                    ▼
                 Jinja2
                    │
                    ▼
                   HTML

📚 Responsabilidad de cada componente
Componente
Responsabilidad
server.py
Ejecutar la aplicación
__init__.py
Inicializar Flask
mysqlconnection.py
Conectar con MySQL
curso.py
Trabajar con cursos
estudiante.py
Trabajar con estudiantes
cursos.py
Controlar rutas de cursos
estudiantes.py
Controlar rutas de estudiantes
cursos.html
Mostrar y crear cursos
nuevo_estudiante.html
Crear estudiantes
mostrar_curso.html
Mostrar estudiantes del curso
base.html
Estructura común
style.css
Diseño


⚠️ Errores frecuentes
La tabla estudiantes no se crea
Crear primero:
cursos
y después:
estudiantes
porque:
estudiantes.curso_id
depende de:
cursos.id

No aparecen los cursos en el <select>
Comprobar:
cursos = Curso.get_all()
y:
{% for curso in cursos %}

No aparecen estudiantes
Revisar:
estudiantes.curso_id
y:
cursos.id

Error en url_for()
El nombre utilizado en:
url_for("mostrar_curso")
debe coincidir con la función:
def mostrar_curso(id):

No encuentra el template
La estructura debe ser:
flask_app/
└── templates/
    ├── base.html
    ├── cursos.html
    ├── nuevo_estudiante.html
    └── mostrar_curso.html

✅ Checklist
[ ] Flask instalado
[ ] PyMySQL instalado
[ ] Pipenv configurado
[ ] MySQL funcionando

[ ] Base esquema_estudiantes_cursos creada
[ ] Tabla cursos creada
[ ] Tabla estudiantes creada
[ ] FOREIGN KEY creada
[ ] Datos de prueba insertados
[ ] ERD guardado en resources/

[ ] flask_app/__init__.py
[ ] config/mysqlconnection.py
[ ] models/curso.py
[ ] models/estudiante.py
[ ] controllers/cursos.py
[ ] controllers/estudiantes.py

[ ] base.html
[ ] cursos.html
[ ] nuevo_estudiante.html
[ ] mostrar_curso.html
[ ] style.css
[ ] server.py

[ ] / funciona
[ ] /cursos funciona
[ ] Crear curso funciona
[ ] /estudiantes/nuevo funciona
[ ] Select de cursos funciona
[ ] Crear estudiante funciona
[ ] /cursos/<id> funciona
[ ] Se muestran estudiantes del curso
[ ] redirect() funciona
[ ] url_for() funciona
[ ] request.form funciona
[ ] Jinja2 funciona
[ ] LEFT JOIN funciona
[ ] Relación 1:N funciona

📦 Entregable
GitHub
Subir el proyecto completo:
ESTUDIANTES_CURSOS/
│
├── flask_app/
├── resources/
├── Pipfile
├── Pipfile.lock
├── .gitignore
└── server.py
Evidencia
Entregar una captura donde se observe:
Cursos
+
Nuevo Curso
+
Todos los Cursos
y otra donde se observe:
Estudiantes de un curso
ERD
Debe existir:
resources/
└── esquema_estudiantes_cursos_erd.mwb

🏁 Resultado esperado
La aplicación debe permitir realizar este flujo:
                   /cursos
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Crear Curso          Seleccionar Curso
             │                   │
             ▼                   ▼
          MySQL              /cursos/<id>
                                 │
                                 ▼
                         Estudiantes del curso
Y para estudiantes:
/cursos
   ↓
Agregar Estudiante
   ↓
/estudiantes/nuevo
   ↓
Seleccionar curso
   ↓
Completar estudiante
   ↓
POST
   ↓
INSERT
   ↓
redirect()
   ↓
/cursos
La aplicación final debe demostrar correctamente la relación:
CURSO
  │
  ├── ESTUDIANTE
  ├── ESTUDIANTE
  ├── ESTUDIANTE
  └── ESTUDIANTE
mediante una relación uno a muchos implementada con una clave foránea.

