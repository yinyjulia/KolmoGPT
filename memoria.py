import json
import os
from datetime import datetime

import config


ARCHIVO = os.path.join(
    config.MEMORY_PATH,
    "usuarios.json"
)


# ===========================
# Inicializar memoria
# ===========================

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


# ===========================
# Cargar memoria
# ===========================

def cargar():

    iniciar_memoria()

    try:

        with open(
            ARCHIVO,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except json.JSONDecodeError:

        print(
            "Aviso: usuarios.json corrupto. "
            "Reiniciando memoria."
        )

        guardar({})

        return {}


# ===========================
# Guardar memoria
# ===========================

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


# ===========================
# Usuario
# ===========================

def obtener_usuario(nombre):

    datos = cargar()

    nombre = nombre.lower()


    if nombre not in datos:

        datos[nombre] = {

            "mensajes": 0,

            "ultima_visita": "",

            "recuerdos": [],

            "contexto": []

        }

        guardar(datos)


    # Compatibilidad con usuarios
    # antiguos.

    if "recuerdos" not in datos[nombre]:

        datos[nombre]["recuerdos"] = []


    if "contexto" not in datos[nombre]:

        datos[nombre]["contexto"] = []


    return datos[nombre]


# ===========================
# Actualizar usuario
# ===========================

def actualizar_usuario(nombre):

    datos = cargar()

    nombre = nombre.lower()


    if nombre not in datos:

        datos[nombre] = {

            "mensajes": 0,

            "ultima_visita": "",

            "recuerdos": [],

            "contexto": []

        }


    if "recuerdos" not in datos[nombre]:

        datos[nombre]["recuerdos"] = []


    if "contexto" not in datos[nombre]:

        datos[nombre]["contexto"] = []


    datos[nombre]["mensajes"] += 1


    datos[nombre]["ultima_visita"] = (

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    )


    guardar(datos)


# ===========================
# Guardar recuerdos IA
# ===========================

def guardar_recuerdos(
    usuario,
    texto
):

    if not texto:

        return


    lineas = texto.splitlines()


    # ===========================
    # Respuestas que NO son
    # recuerdos
    # ===========================

    bloqueadas = [

        "NINGUNO",
        "NADA",

        "NO SE PUEDE",
        "NO HAY INFORMACIÓN",
        "NO HAY INFORMACION",

        "NO ESPECIFICADO",
        "NO ESPECIFICADA",

        "NO SE ESPECIFICA",
        "NO SE PROPORCIONA",

        "NO PROPORCIONADO",
        "NO PROPORCIONADA",

        "NO GUARDO",
        "NO GUARDAR",
        "NO GUARDES",

        "NO RECUERDO",
        "NO RECUERDES",

        "DATOS PERSONALES:",
        "DATOS PERSONALES VOLUNTARIOS:",

        "GUSTOS:",
        "PREFERENCIAS:",

        "MEMORIA:",
        "RECUERDO:",

        "NO VEO NINGÚN MENSAJE",
        "NO VEO NINGUN MENSAJE",

        "NECESITO MÁS INFORMACIÓN",
        "NECESITO MAS INFORMACION",

        "NO HAY NADA QUE RECORDAR",

        "INFORMACIÓN RELEVANTE PARA RECORDAR",
        "INFORMACION RELEVANTE PARA RECORDAR",

        "INFORMACIÓN NO ESPECIFICADA",
        "INFORMACION NO ESPECIFICADA",

        "NO SE PROPORCIONAN DATOS",

        "SOY UN BOT",
        "ERES UN BOT",

        "IA_RETROWIKI",
        "IA RETROWIKI",

        "ASISTENTE",

    ]


    # ===========================
    # Posibles secretos
    # ===========================

    secretos = [

        "CONTRASEÑA",
        "CONTRASENA",

        "PASSWORD",

        "TOKEN",

        "API KEY",
        "API_KEY",
        "APIKEY",

        "SECRET",
        "SECRETO",

        "CLAVE",

        "CREDENCIAL",
        "CREDENCIALES",

        "NÚMERO DE TARJETA",
        "NUMERO DE TARJETA",

        "TARJETA BANCARIA",
        "CUENTA BANCARIA",

        "IBAN",

        "CVV",
        "CVC",

    ]


    for linea in lineas:

        linea = linea.strip()


        if not linea:

            continue


        # ===========================
        # Limpiar prefijos
        # ===========================

        if (
            linea.startswith("-")
            or
            linea.startswith("*")
        ):

            linea = linea[
                1:
            ].strip()


        if not linea:

            continue


        linea_upper = linea.upper()


        # ===========================
        # Bloquear respuestas basura
        # ===========================

        if any(

            palabra in linea_upper

            for palabra in bloqueadas

        ):

            continue


        # ===========================
        # Bloquear posibles secretos
        # ===========================

        if any(

            palabra in linea_upper

            for palabra in secretos

        ):

            print(
                "Memoria bloqueada "
                "(posible dato sensible):",
                linea
            )

            continue


        # ===========================
        # No guardar texto enorme
        # ===========================

        if len(linea) > 120:

            continue


        # ===========================
        # No guardar cosas demasiado
        # cortas
        # ===========================

        if len(linea) < 3:

            continue


        añadir_recuerdo(
            usuario,
            linea
        )


# ===========================
# Obtener recuerdos
# ===========================

def obtener_recuerdos(nombre):

    usuario = obtener_usuario(
        nombre
    )

    return usuario["recuerdos"]


# ===========================
# Añadir recuerdo
# ===========================

def añadir_recuerdo(
    nombre,
    recuerdo
):

    recuerdo = recuerdo.strip()


    if recuerdo == "":

        return


    datos = cargar()

    nombre = nombre.lower()


    if nombre not in datos:

        datos[nombre] = {

            "mensajes": 0,

            "ultima_visita": "",

            "recuerdos": [],

            "contexto": []

        }


    if "recuerdos" not in datos[nombre]:

        datos[nombre]["recuerdos"] = []


    if "contexto" not in datos[nombre]:

        datos[nombre]["contexto"] = []


    if recuerdo not in datos[
        nombre
    ][
        "recuerdos"
    ]:

        datos[
            nombre
        ][
            "recuerdos"
        ].append(
            recuerdo
        )


        # Máximo 50 recuerdos.

        if len(
            datos[
                nombre
            ][
                "recuerdos"
            ]
        ) > 50:

            datos[
                nombre
            ][
                "recuerdos"
            ] = (

                datos[
                    nombre
                ][
                    "recuerdos"
                ][-50:]

            )


        guardar(datos)


# ===========================
# Obtener contexto individual
# ===========================

def obtener_contexto_chat(
    usuario,
    limite=10
):

    usuario = obtener_usuario(
        usuario
    )


    contexto = usuario.get(
        "contexto",
        []
    )


    return contexto[
        -limite:
    ]


# ===========================
# Guardar contexto individual
# ===========================

def guardar_contexto_chat(
    usuario,
    pregunta,
    respuesta,
    limite=10
):

    datos = cargar()

    usuario = usuario.lower()


    if usuario not in datos:

        datos[usuario] = {

            "mensajes": 0,

            "ultima_visita": "",

            "recuerdos": [],

            "contexto": []

        }


    if "contexto" not in datos[
        usuario
    ]:

        datos[
            usuario
        ][
            "contexto"
        ] = []


    datos[
        usuario
    ][
        "contexto"
    ].append({

        "role": "user",

        "content": pregunta

    })


    datos[
        usuario
    ][
        "contexto"
    ].append({

        "role": "assistant",

        "content": respuesta

    })


    # Máximo 10 mensajes de contexto
    # aproximadamente 5 intercambios.

    datos[
        usuario
    ][
        "contexto"
    ] = (

        datos[
            usuario
        ][
            "contexto"
        ][-limite:]

    )


    guardar(datos)


# ===========================
# Mostrar usuario
# ===========================

def mostrar_usuario(nombre):

    usuario = obtener_usuario(
        nombre
    )


    print()

    print(
        "Usuario:",
        nombre
    )

    print(
        "Mensajes:",
        usuario["mensajes"]
    )

    print(
        "Última visita:",
        usuario["ultima_visita"]
    )


    print()

    print(
        "Recuerdos:"
    )


    for recuerdo in usuario[
        "recuerdos"
    ]:

        print(
            "-",
            recuerdo
        )


    print()

    print(
        "Contexto:"
    )


    for mensaje in usuario.get(
        "contexto",
        []
    ):

        print(

            f'{mensaje["role"]}: '
            f'{mensaje["content"]}'

        )