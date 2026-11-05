
# 🐾 Primera aplicación Flask + MySQL

## Descripción

Aplicación web desarrollada con Python, Flask y MySQL que permite visualizar y registrar mascotas mediante un formulario HTML.

## Objetivos

- Conectar Flask con una base de datos MySQL.
- Mostrar registros almacenados.
- Crear nuevos registros mediante formularios.
- Utilizar sentencias preparadas INSERT.
- Trabajar con métodos de clase.
- Utilizar POST y redirect.

## Tecnologías

- Python
- Flask
- MySQL
- PyMySQL
- HTML
- CSS
- Bootstrap
- Jinja2

## Estructura

```text
primera_app_mysql/
│
├── server.py
├── mascota.py
├── mysqlconnection.py
├── requirements.txt
├── schema.sql
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## Base de datos

Nombre: `primera_flask`

Tabla: `mascotas`

Campos:
- id
- nombre
- tipo
- color
- created_at
- updated_at

## Instalación

Crear entorno virtual:

```cmd
py -m venv venv
```

Activar entorno:

```cmd
venv\Scripts\activate
```

Instalar dependencias:

```cmd
python -m pip install -r requirements.txt
```

## Ejecución

```cmd
python server.py
```

Abrir en el navegador:

http://127.0.0.1:5000/

## Funcionalidades

### READ

Muestra todas las mascotas registradas en MySQL.

### CREATE

Permite agregar mascotas mediante un formulario.

Los datos se reciben con request.form y se guardan utilizando Mascota.save().

## Sentencias preparadas

Se utilizan parámetros para separar la consulta SQL de los datos proporcionados por el usuario.

## Flujo

Formulario HTML
→ POST
→ Flask
→ Mascota.save()
→ INSERT
→ MySQL
→ redirect()
→ GET
→ listado actualizado
