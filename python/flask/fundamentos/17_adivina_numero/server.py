import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Clave secreta necesaria para cifrar las cookies de sesión
app.secret_key = "clave_secreta_adivina_numero"

@app.route('/')
def index():
    # Inicializar las variables del juego en la sesión si no existen
    if 'numero_secreto' not in session:
        session['numero_secreto'] = random.randint(1, 10)
        session['intentos'] = 0
        session['mensaje'] = "¡Adivina un número entre 1 y 10!"
        session['estado'] = "inicio"  # Posibles estados: inicio, pista_mayor, pista_menor, ganado

    return render_template('index.html')

@app.route('/adivinar', methods=['POST'])
def adivinar():
    # Validar que el usuario haya enviado un número válido
    try:
        intento = int(request.form['numero'])
    except (ValueError, KeyError):
        return redirect(url_for('index'))

    # Incrementar el contador de intentos
    session['intentos'] = session.get('intentos', 0) + 1
    numero_secreto = session.get('numero_secreto')

    # Lógica de comparación
    if intento < numero_secreto:
        session['mensaje'] = f"¡El número secreto es MAYOR que {intento}!"
        session['estado'] = "pista_mayor"
    elif intento > numero_secreto:
        session['mensaje'] = f"¡El número secreto es MENOR que {intento}!"
        session['estado'] = "pista_menor"
    else:
        session['mensaje'] = f"¡Felicidades! Adivinaste el número {intento} en {session['intentos']} intento(s)."
        session['estado'] = "ganado"

    return redirect(url_for('index'))

@app.route('/reiniciar')
def reiniciar():
    # Limpiar todos los datos guardados en la sesión para reiniciar el juego
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)