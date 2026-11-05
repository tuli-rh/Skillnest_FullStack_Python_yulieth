from flask import Flask, render_template

from mascota import Mascota


# CREAR APLICACIÓN FLASK

app = Flask(__name__)


# RUTA PRINCIPAL

@app.route("/")
def index():

    # Obtener todas las mascotas
    mascotas = Mascota.get_all()

    # Mostrar mascotas en la terminal
    print(mascotas)

    # Enviar información a HTML
    return render_template(
        "index.html",
        todas_mascotas=mascotas
    )


# EJECUTAR SERVIDOR

if __name__ == "__main__":

    app.run(debug=True)