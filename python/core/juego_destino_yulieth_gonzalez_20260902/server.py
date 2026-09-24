from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)

# Clave para manejar las sesiones
app.secret_key = "clave_secreta"


# Ruta principal
# Muestra el formulario
@app.route("/")
def inicio():
    return render_template("index.html")


# Ruta para recibir los datos del formulario
@app.route("/enviar", methods=["POST"])
def enviar():
    # Recibimos los datos del formulario
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    sueno = request.form["sueno"]

    # Guardamos los datos en la sesión
    session["nombre"] = nombre
    session["edad"] = edad
    session["sueno"] = sueno

    # Redirigimos a la página del futuro
    return redirect("/futuro")


# Ruta que muestra la predicción
@app.route("/futuro")
def futuro():

    # Recuperamos los datos desde la sesión
    nombre = session.get("nombre")
    edad = session.get("edad")
    sueno = session.get("sueno")

    # Elegimos aleatoriamente una predicción
    predicciones = [
        "Te espera un futuro lleno de nuevas oportunidades.",
        "Tendrás que esforzarte, pero lograrás cumplir tus metas."
    ]

    prediccion = random.choice(predicciones)

    return render_template(
        "futuro.html",
        nombre=nombre,
        edad=edad,
        sueno=sueno,
        prediccion=prediccion
    )


if __name__ == "__main__":
    app.run(debug=True)