from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_app.models.usuario import Usuario
from flask_app.models.cancion import Cancion
from flask_app.models.favorito import Favorito


@app.route("/")
def inicio():

    return redirect(
        url_for("usuarios")
    )


@app.route("/usuarios")
def usuarios():

    lista_usuarios = Usuario.get_all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )


@app.route("/canciones")
def canciones():

    lista_canciones = Cancion.get_all()

    return render_template(
        "canciones.html",
        canciones=lista_canciones
    )


@app.route(
    "/usuarios/crear",
    methods=["POST"]
)
def crear_usuario():

    nombre = request.form.get("nombre")
    email = request.form.get("email")
    contrasena = request.form.get("contrasena")

    if not nombre or not email or not contrasena:

        flash(
            "Todos los campos son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("usuarios")
        )

    Usuario.save({
        "nombre": nombre,
        "email": email,
        "contrasena": contrasena
    })

    flash(
        "Usuario creado correctamente.",
        "success"
    )

    return redirect(
        url_for("usuarios")
    )


@app.route(
    "/canciones/crear",
    methods=["POST"]
)
def crear_cancion():

    titulo = request.form.get("titulo")
    artista = request.form.get("artista")

    if not titulo or not artista:

        flash(
            "Título y artista son obligatorios.",
            "danger"
        )

        return redirect(
            url_for("canciones")
        )

    Cancion.save({
        "titulo": titulo,
        "artista": artista
    })

    flash(
        "Canción creada correctamente.",
        "success"
    )

    return redirect(
        url_for("canciones")
    )
