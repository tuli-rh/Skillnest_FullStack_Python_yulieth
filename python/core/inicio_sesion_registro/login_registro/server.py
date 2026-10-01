from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import mysql.connector
import re
from functools import wraps

app = Flask(__name__)

app.secret_key = "una-clave-secreta-muy-segura"

bcrypt = Bcrypt(app)


# --------------------------------
# CONEXIÓN A MYSQL
# --------------------------------

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="login_registro"
    )


# --------------------------------
# VALIDAR SESIÓN
# --------------------------------

def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/")

        return route_function(*args, **kwargs)

    return wrapper


# --------------------------------
# PÁGINA PRINCIPAL
# --------------------------------

@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------
# REGISTRO
# --------------------------------

@app.route("/register", methods=["POST"])
def register():

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    errors = []

    # Validar nombre
    if not first_name:
        errors.append("El nombre es obligatorio.")
    elif not re.fullmatch(
        r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü]{2,}",
        first_name
    ):
        errors.append(
            "El nombre debe tener solamente letras y al menos 2 caracteres."
        )

    # Validar apellido
    if not last_name:
        errors.append("El apellido es obligatorio.")
    elif not re.fullmatch(
        r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü]{2,}",
        last_name
    ):
        errors.append(
            "El apellido debe tener solamente letras y al menos 2 caracteres."
        )

    # Validar email
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not email:
        errors.append("El correo electrónico es obligatorio.")
    elif not re.fullmatch(email_regex, email):
        errors.append("El correo electrónico no tiene un formato válido.")

    # Validar contraseña
    if not password:
        errors.append("La contraseña es obligatoria.")
    else:

        if len(password) < 8:
            errors.append(
                "La contraseña debe tener al menos 8 caracteres."
            )

        # Bonus de plata: número
        if not re.search(r"\d", password):
            errors.append(
                "La contraseña debe contener al menos un número."
            )

        # Bonus de plata: mayúscula
        if not re.search(r"[A-Z]", password):
            errors.append(
                "La contraseña debe contener al menos una letra mayúscula."
            )

    # Confirmación
    if password != confirm_password:
        errors.append("Las contraseñas no coinciden.")

    # --------------------------------
    # VERIFICAR CORREO EN BASE DE DATOS
    # --------------------------------

    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    query = "SELECT id FROM users WHERE email = %s"
    cursor.execute(query, (email,))

    existing_user = cursor.fetchone()

    cursor.close()
    db.close()

    if existing_user:
        errors.append("El correo electrónico ya está registrado.")

    # --------------------------------
    # SI HAY ERRORES
    # --------------------------------

    if errors:
        return render_template(
            "index.html",
            register_errors=errors,
            register_data={
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            }
        )

    # --------------------------------
    # HASH DE CONTRASEÑA
    # --------------------------------

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # --------------------------------
    # GUARDAR USUARIO
    # --------------------------------

    db = connect_to_db()
    cursor = db.cursor()

    query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (first_name, last_name, email, hashed_password)
    )

    db.commit()

    # Obtener ID del usuario recién creado
    user_id = cursor.lastrowid

    cursor.close()
    db.close()

    # Guardar usuario en sesión
    session["user_id"] = user_id

    return redirect("/success")


# --------------------------------
# LOGIN
# --------------------------------

@app.route("/login", methods=["POST"])
def login():

    email = request.form.get("login_email", "").strip()
    password = request.form.get("login_password", "")

    errors = []

    if not email:
        errors.append("El correo electrónico es obligatorio.")

    if not password:
        errors.append("La contraseña es obligatoria.")

    if errors:
        return render_template(
            "index.html",
            login_errors=errors
        )

    # Buscar usuario
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT id, first_name, last_name, email, password
        FROM users
        WHERE email = %s
    """

    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    # Usuario no encontrado
    if not user:
        errors.append("El correo electrónico no está registrado.")

        return render_template(
            "index.html",
            login_errors=errors
        )

    # Verificar contraseña
    if not bcrypt.check_password_hash(user["password"], password):

        errors.append("La contraseña es incorrecta.")

        return render_template(
            "index.html",
            login_errors=errors
        )

    # --------------------------------
    # LOGIN EXITOSO
    # --------------------------------

    session["user_id"] = user["id"]

    return redirect("/success")


# --------------------------------
# PÁGINA DE ÉXITO
# --------------------------------

@app.route("/success")
@login_required
def success():

    user_id = session["user_id"]

    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT first_name, last_name, email
        FROM users
        WHERE id = %s
    """

    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    db.close()

    if not user:
        session.clear()
        return redirect("/")

    return render_template(
        "success.html",
        user=user
    )


# --------------------------------
# LOGOUT
# --------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# --------------------------------
# EJECUTAR SERVIDOR
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)
