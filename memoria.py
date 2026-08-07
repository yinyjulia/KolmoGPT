import json
import os
from datetime import datetime

import config


ARCHIVO = os.path.join(
    config.MEMORY_PATH,
    "usuarios.json"
)



# ===========================
# Inicializar Contexto
# ===========================

def obtener_contexto_chat(usuario, limite=10):

    archivo = os.path.join(
        config.LOG_PATH,
        "chat.log"
    )

    mensajes = []

    if not os.path.exists(archivo):
        return []

    with open(
        archivo,
        "r",
        encoding="utf-8"
    ) as f:

        for linea in f:

            if f"] {usuario}:" in linea:

                mensajes.append(
                    linea
                )

    return mensajes[-limite:]


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
            "Aviso: usuarios.json corrupto. Reiniciando memoria."
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



# ===========================
# Guardar recuerdos IA
# ===========================

def guardar_recuerdos(usuario, texto):

    lineas = texto.splitlines()


    for linea in lineas:

        linea = linea.strip()


        if linea == "":
            continue


        bloqueadas = [

            "NINGUNO",

            "# NINGUNO",

            "NO SE PUEDE",

            "NO GUARDES",

            "NO GUARDAR",

            "KOLMO_YT |",

            "@IA_RETROWIKI",

            "MEMORIA",

            "RECUERDA",

        ]


        linea_upper = linea.upper()


        if any(
            palabra in linea_upper
            for palabra in bloqueadas
        ):
            continue


        añadir_recuerdo(
            usuario,
            linea
        )



# ===========================
# Obtener recuerdos
# ===========================

def obtener_recuerdos(nombre):

    usuario = obtener_usuario(nombre)

    return usuario["recuerdos"]



# ===========================
# Añadir recuerdo
# ===========================

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


        # Limitar memoria a 50 recuerdos

        if len(datos[nombre]["recuerdos"]) > 50:

            datos[nombre]["recuerdos"] = (
                datos[nombre]["recuerdos"][-50:]
            )


        guardar(datos)



# ===========================
# Mostrar usuario
# ===========================

def mostrar_usuario(nombre):

    usuario = obtener_usuario(nombre)


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


    for recuerdo in usuario["recuerdos"]:

        print(
            "-",
            recuerdo
        )
        
# ===========================
# Contexto reciente del chat
# ===========================

def obtener_contexto_chat(usuario, limite=10):

    archivo = os.path.join(
        config.LOG_PATH,
        "chat.log"
    )

    mensajes = []

    if not os.path.exists(archivo):
        return []


    with open(
        archivo,
        "r",
        encoding="utf-8"
    ) as f:

        for linea in f:

            if f"] {usuario}:" in linea:

                mensajes.append(
                    linea.strip()
                )


    return mensajes[-limite:]