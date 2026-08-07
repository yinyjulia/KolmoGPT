import json
import os
from datetime import datetime

import config


ARCHIVO = os.path.join(
    config.MEMORY_PATH,
    "usuarios.json"
)


def iniciar_memoria():

    os.makedirs(
        config.MEMORY_PATH,
        exist_ok=True
    )

    if not os.path.exists(ARCHIVO):

        with open(
            ARCHIVO,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {},
                f,
                ensure_ascii=False,
                indent=4
            )


def cargar():

    iniciar_memoria()

    with open(
        ARCHIVO,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def guardar(datos):

    with open(
        ARCHIVO,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=4
        )


def obtener_usuario(nombre):

    datos = cargar()

    nombre = nombre.lower()

    if nombre not in datos:

        datos[nombre] = {

            "mensajes": 0,

            "ultima_visita": "",

            "recuerdos": []

        }

        guardar(datos)

    return datos[nombre]


def actualizar_usuario(nombre):

    datos = cargar()

    nombre = nombre.lower()

    if nombre not in datos:

        datos[nombre] = {

            "mensajes": 0,

            "ultima_visita": "",

            "recuerdos": []

        }

    datos[nombre]["mensajes"] += 1

    datos[nombre]["ultima_visita"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    guardar(datos)


def obtener_recuerdos(nombre):

    usuario = obtener_usuario(nombre)

    return usuario["recuerdos"]


def añadir_recuerdo(nombre, recuerdo):

    recuerdo = recuerdo.strip()

    if recuerdo == "":
        return

    datos = cargar()

    nombre = nombre.lower()

    if nombre not in datos:

        datos[nombre] = {

            "mensajes": 0,

            "ultima_visita": "",

            "recuerdos": []

        }

    if recuerdo not in datos[nombre]["recuerdos"]:

        datos[nombre]["recuerdos"].append(
            recuerdo
        )

        guardar(datos)


def mostrar_usuario(nombre):

    usuario = obtener_usuario(nombre)

    print()

    print("Usuario:", nombre)

    print("Mensajes:", usuario["mensajes"])

    print("Última visita:", usuario["ultima_visita"])

    print()

    print("Recuerdos:")

    for r in usuario["recuerdos"]:

        print("-", r)