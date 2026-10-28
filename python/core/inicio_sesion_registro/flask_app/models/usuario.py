from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, date
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d).+$') # Bonus Plata: Al menos 1 mayúscula y 1 número

class Usuario:
    DB = "esquema_usuarios"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.fecha_nacimiento = data['fecha_nacimiento']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO usuarios (first_name, last_name, email, password, fecha_nacimiento) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(fecha_nacimiento)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = {'id': user_id}
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_register(form):
        is_valid = True

        # Validar Nombre
        if len(form['first_name'].strip()) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "register")
            is_valid = False
        elif not NOMBRE_REGEX.match(form['first_name']):
            flash("El nombre solo debe contener letras.", "register")
            is_valid = False

        # Validar Apellido
        if len(form['last_name'].strip()) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "register")
            is_valid = False
        elif not NOMBRE_REGEX.match(form['last_name']):
            flash("El apellido solo debe contener letras.", "register")
            is_valid = False

        # Validar Email
        if not EMAIL_REGEX.match(form['email']):
            flash("El correo electrónico no tiene un formato válido.", "register")
            is_valid = False
        else:
            if Usuario.get_by_email(form['email']):
                flash("El correo electrónico ya se encuentra registrado.", "register")
                is_valid = False

        # Validar Fecha de Nacimiento (Bonus Oro)
        if not form.get('fecha_nacimiento'):
            flash("Debes ingresar tu fecha de nacimiento.", "register")
            is_valid = False
        else:
            fecha_nac = datetime.strptime(form['fecha_nacimiento'], '%Y-%m-%d').date()
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            if edad < 18:
                flash("Debes tener al menos 18 años para poder registrarte.", "register")
                is_valid = False

        # Validar Contraseña
        if len(form['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "register")
            is_valid = False
        elif not PASSWORD_REGEX.match(form['password']):
            flash("La contraseña debe incluir al menos un número y una letra mayúscula.", "register") # Bonus Plata
            is_valid = False

        # Confirmación de contraseña
        if form['password'] != form['confirm_password']:
            flash("Las contraseñas no coinciden.", "register")
            is_valid = False

        return is_valid