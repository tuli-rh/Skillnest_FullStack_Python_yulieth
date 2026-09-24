# Nombre: Yulieth Gonzalez
# Curso: 4°C

# Ranking de puntajes de un torneo de eSports
puntajes = [[1000, 1500, 2000], [300, 700, 1400]]

puntajes[1][0] = 600


# Lista de creadores de contenido en una plataforma de streaming
streamers = [
    {"nombre": "GameNinjaPro", "seguidores": 250000},
    {"nombre": "PixelWarrior", "seguidores": 180000}
]

streamers[0]["nombre"] = "EliteGamerX"


# Eventos en distintas ciudades del mundo
eventos = {
    "Estados Unidos": ["Los Ángeles", "Nueva York", "Las Vegas"],
    "España": ["Madrid", "Barcelona", "Valencia"]
}

eventos["Estados Unidos"][2] = "San Francisco"


# Coordenadas de la sede de un torneo internacional
ubicacion = [
    {"latitud": 34.052235, "longitud": -118.243683}
]

ubicacion[0]["latitud"] = 40.712776


# Función para recorrer una lista de diccionarios
def iterar_diccionario(lista):
    for streamer in lista:
        print(f"nombre - {streamer['nombre']}, seguidores - {streamer['seguidores']}")


iterar_diccionario(streamers)


# Función para obtener valores de una clave
def obtener_valores(clave, lista):
    for diccionario in lista:
        print(diccionario[clave])


obtener_valores("nombre", streamers)

print()

obtener_valores("seguidores", streamers)


# Diccionario con listas
categorias = {
    "juegos_populares": [
        "Fortnite",
        "Minecraft",
        "Valorant",
        "GTA V"
    ],
    "ciudades_eventos": [
        "Nueva York",
        "Madrid",
        "Tokio"
    ]
}


# Función para mostrar información
def mostrar_informacion(diccionario):
    for categoria, items in diccionario.items():
        print(f"{len(items)} {categoria.upper()}")

        for item in items:
            print(item)

        print()


mostrar_informacion(categorias)
