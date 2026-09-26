from flask_app import app

from flask import (
    render_template,
    redirect,
    request,
    url_for
)

from flask_app.models.taco import Taco


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/crear", methods=["POST"])
def crear():

    datos = {
        "tortilla": request.form["tortilla"],
        "guiso": request.form["guiso"],
        "salsa": request.form["salsa"]
    }

    Taco.save(datos)

    return redirect(
        url_for("tacos")
    )


@app.route("/tacos")
def tacos():

    todos_los_tacos = Taco.get_all()

    return render_template(
        "resultados.html",
        todos_tacos=todos_los_tacos
    )


@app.route("/mostrar/<int:taco_id>")
def detalle(taco_id):

    datos = {
        "id": taco_id
    }

    taco = Taco.get_one(datos)

    if taco is None:

        return "Taco no encontrado", 404

    return render_template(
        "detalle.html",
        taco=taco
    )


@app.route("/editar/<int:taco_id>")
def editar(taco_id):

    datos = {
        "id": taco_id
    }

    taco = Taco.get_one(datos)

    if taco is None:

        return "Taco no encontrado", 404

    return render_template(
        "editar.html",
        taco=taco
    )


@app.route(
    "/actualizar/<int:taco_id>",
    methods=["POST"]
)
def actualizar(taco_id):

    datos = {
        "id": taco_id,
        "tortilla": request.form["tortilla"],
        "guiso": request.form["guiso"],
        "salsa": request.form["salsa"]
    }

    Taco.update(datos)

    return redirect(
        url_for(
            "detalle",
            taco_id=taco_id
        )
    )


@app.route("/borrar/<int:taco_id>")
def borrar(taco_id):

    datos = {
        "id": taco_id
    }

    Taco.delete(datos)

    return redirect(
        url_for("tacos")
    )