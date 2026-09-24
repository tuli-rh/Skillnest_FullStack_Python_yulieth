class SuscripcionStreaming:
    costos_suscripcion = {
        "Gratis": 0,
        "Estándar": 5.99,
        "Premium": 10.99
    }

    def __init__(self, usuario, tipo_suscripcion="Gratis"):
        self.usuario = usuario

        if tipo_suscripcion in self.costos_suscripcion:
            self.tipo_suscripcion = tipo_suscripcion
        else:
            self.tipo_suscripcion = "Gratis"

        self.costo_mensual = self.costos_suscripcion[self.tipo_suscripcion]
        self.saldo_pendiente = self.costo_mensual

    def realizar_pago(self, monto):
        """Reduce el saldo pendiente según el monto pagado."""

        if monto <= 0:
            print("El monto del pago debe ser mayor que 0.")
            return

        if monto >= self.saldo_pendiente:
            self.saldo_pendiente = 0
            print(f"{self.usuario} ha pagado su saldo pendiente.")
        else:
            self.saldo_pendiente -= monto
            print(f"{self.usuario} realizó un pago de ${monto:.2f}.")
            print(f"Saldo pendiente: ${self.saldo_pendiente:.2f}")

    def cambiar_suscripcion(self, nuevo_tipo):
        """Cambia el tipo de suscripción y actualiza el costo mensual."""

        if nuevo_tipo not in self.costos_suscripcion:
            print("Tipo de suscripción no válido.")
            return

        self.tipo_suscripcion = nuevo_tipo
        self.costo_mensual = self.costos_suscripcion[nuevo_tipo]

        # Se agrega el nuevo costo al saldo pendiente
        self.saldo_pendiente += self.costo_mensual

        print(f"{self.usuario} cambió su suscripción a {nuevo_tipo}.")
        print(f"Nuevo costo mensual: ${self.costo_mensual:.2f}")

    def ver_contenido_exclusivo(self):
        """Permite ver contenido exclusivo según el tipo de suscripción."""

        if self.tipo_suscripcion == "Gratis":
            print(f"{self.usuario} no tiene acceso al contenido exclusivo.")
        else:
            print(f"{self.usuario} puede acceder al contenido exclusivo.")

    def mostrar_info_suscripcion(self):
        """Muestra la información de la suscripción del usuario."""

        print("\n--- Información de suscripción ---")
        print(f"Usuario: {self.usuario}")
        print(f"Tipo de suscripción: {self.tipo_suscripcion}")
        print(f"Costo mensual: ${self.costo_mensual:.2f}")
        print(f"Saldo pendiente: ${self.saldo_pendiente:.2f}")


# ==========================================
# PRUEBAS
# ==========================================

# 1. Crear tres usuarios con diferentes suscripciones
usuario1 = SuscripcionStreaming("Ana", "Gratis")
usuario2 = SuscripcionStreaming("Carlos", "Estándar")
usuario3 = SuscripcionStreaming("María", "Premium")


# ==========================================
# PRIMER USUARIO
# ==========================================

print("\n===== USUARIO 1 =====")

usuario1.mostrar_info_suscripcion()

# Intenta ver contenido exclusivo
usuario1.ver_contenido_exclusivo()

# Mejora su suscripción a Estándar
usuario1.cambiar_suscripcion("Estándar")

# Paga su saldo
usuario1.realizar_pago(5.99)

usuario1.mostrar_info_suscripcion()


# ==========================================
# SEGUNDO USUARIO
# ==========================================

print("\n===== USUARIO 2 =====")

usuario2.mostrar_info_suscripcion()

# Ve contenido exclusivo
usuario2.ver_contenido_exclusivo()

# Cambia su suscripción a Premium
usuario2.cambiar_suscripcion("Premium")

# Paga dos veces
usuario2.realizar_pago(5.99)
usuario2.realizar_pago(10.99)

usuario2.mostrar_info_suscripcion()


# ==========================================
# TERCER USUARIO
# ==========================================

print("\n===== USUARIO 3 =====")

usuario3.mostrar_info_suscripcion()

# Intenta pagar menos que su saldo pendiente
usuario3.realizar_pago(5.00)

# Intenta ver contenido exclusivo
usuario3.ver_contenido_exclusivo()

usuario3.mostrar_info_suscripcion()