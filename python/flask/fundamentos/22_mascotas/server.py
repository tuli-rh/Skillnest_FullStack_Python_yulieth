
from flask import Flask, render_template, request, redirect, url_for

from mascota import Mascota


app = Flask(__name__)


# =====================================
# RUTA PRINCIPAL
# MOSTRAR MASCOTAS
# =====================================

@app.route("/")
def index():

    mascotas = Mascota.get_all()

    return render_template(
        "index.html",
        mascotas=mascotas
    )


# =====================================
# CREAR UNA NUEVA MASCOTA
# =====================================

@app.route("/crear_mascota", methods=["POST"])
def crear_mascota():

    datos = {

        "nombre": request.form["nombre"],

        "tipo": request.form["tipo"],

        "color": request.form["color"]

    }

    resultado = Mascota.save(datos)

    if resultado is False:

        return "Error: no se pudo guardar la mascota.", 500

    return redirect(url_for("index"))


# =====================================
# EJECUTAR SERVIDOR
# =====================================

if __name__ == "__main__":

    app.run(debug=True)
