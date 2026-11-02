from flask_app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_app.models.estudiante import Estudiante
from flask_app.models.curso import Curso
from flask_app.models.inscripcion import Inscripcion


@app.route("/")
def index():
    estudiantes = Estudiante.get_all()
    cursos = Curso.get_all()
    inscripciones = Inscripcion.get_all()

    return render_template(
        "index.html",
        estudiantes=estudiantes,
        cursos=cursos,
        inscripciones=inscripciones
    )


@app.route("/inscribir", methods=["POST"])
def inscribir():
    estudiante_id_texto = request.form.get("estudiante_id")
    curso_id_texto = request.form.get("curso_id")

    # Comprobar que se hayan seleccionado ambas opciones.
    if not estudiante_id_texto or not curso_id_texto:
        flash(
            "Debes seleccionar un estudiante y un curso.",
            "danger"
        )
        return redirect(url_for("index"))

    # Comprobar que los identificadores sean números positivos.
    try:
        estudiante_id = int(estudiante_id_texto)
        curso_id = int(curso_id_texto)

        if estudiante_id <= 0 or curso_id <= 0:
            raise ValueError

    except ValueError:
        flash("Los datos seleccionados no son válidos.", "danger")
        return redirect(url_for("index"))

    datos_estudiante = {
        "id_estudiante": estudiante_id
    }

    datos_curso = {
        "id_curso": curso_id
    }

    # Comprobar que el estudiante exista.
    estudiante = Estudiante.get_by_id(datos_estudiante)

    if estudiante is None:
        flash("El estudiante seleccionado no existe.", "danger")
        return redirect(url_for("index"))

    # Comprobar que el curso exista.
    curso = Curso.get_by_id(datos_curso)

    if curso is None:
        flash("El curso seleccionado no existe.", "danger")
        return redirect(url_for("index"))

    # Preparar los datos de la relación.
    datos_inscripcion = {
        "estudiante_id": estudiante_id,
        "curso_id": curso_id
    }

    # Evitar una inscripción duplicada.
    if Inscripcion.existe(datos_inscripcion):
        flash(
            "El estudiante ya está inscrito en este curso.",
            "warning"
        )
        return redirect(url_for("index"))

    # Guardar la relación en MySQL.
    Inscripcion.inscribir_estudiante_en_curso(
        datos_inscripcion
    )

    flash("Inscripción realizada correctamente.", "success")

    return redirect(url_for("index"))