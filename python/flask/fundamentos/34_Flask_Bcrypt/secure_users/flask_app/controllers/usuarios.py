from flask import render_template, redirect, request, session, flash

from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario


# =========================
# PÁGINA DE LOGIN
# =========================

@app.route("/")
def index():
    return render_template("login.html")


# =========================
# PÁGINA DE REGISTRO
# =========================

@app.route("/registro")
def registro():
    return render_template("registro.html")


# =========================
# REGISTRAR USUARIO
# =========================

@app.route("/registrar", methods=["POST"])
def registrar():

    datos = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": request.form["password"]
    }

    # Validamos los datos
    if not Usuario.validar_usuario(datos):
        return redirect("/registro")

    # Verificamos si el email ya existe
    if Usuario.existe_email({"email": datos["email"]}):
        flash("El email ya está registrado.", "email")
        return redirect("/registro")

    # Hasheamos la contraseña
    password_hash = bcrypt.generate_password_hash(
        datos["password"]
    ).decode("utf-8")

    # Reemplazamos la contraseña original por el hash
    datos["password"] = password_hash

    # Guardamos el usuario
    usuario_id = Usuario.guardar(datos)

    if not usuario_id:
        flash("No fue posible registrar el usuario.", "general")
        return redirect("/registro")

    # Guardamos el ID en la sesión
    session["usuario_id"] = usuario_id

    return redirect("/dashboard")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    datos = {
        "email": request.form["email"].strip().lower(),
        "password": request.form["password"]
    }

    # Buscamos el usuario por email
    usuario = Usuario.buscar_por_email({
        "email": datos["email"]
    })

    # Si no existe
    if not usuario:
        flash("Email o contraseña incorrectos.", "login")
        return redirect("/")

    # Comparamos la contraseña
    if not bcrypt.check_password_hash(
        usuario.password,
        datos["password"]
    ):
        flash("Email o contraseña incorrectos.", "login")
        return redirect("/")

    # Guardamos el ID en sesión
    session["usuario_id"] = usuario.id

    return redirect("/dashboard")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    # Verificamos que haya sesión
    if "usuario_id" not in session:
        flash("Debes iniciar sesión.", "login")
        return redirect("/")

    # Buscamos al usuario
    usuario = Usuario.buscar_por_id({
        "id": session["usuario_id"]
    })

    return render_template(
        "dashboard.html",
        usuario=usuario
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")