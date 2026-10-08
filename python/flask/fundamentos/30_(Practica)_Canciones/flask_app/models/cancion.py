@app.route("/usuarios/<int:id>")
def mostrar_usuario(id):

    usuario = Usuario.get_by_id_with_favorites({
        "id": id
    })

    if usuario is None:

        return "Usuario no encontrado", 404

    return render_template(
        "mostrar_usuario.html",
        usuario=usuario
    )
