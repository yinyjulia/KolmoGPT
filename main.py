import subprocess
import os
from datetime import datetime

import memoria
import config

from ollama import Client
from twitchio.ext import commands


# ==============================
# Cliente Ollama
# ==============================

client = Client(
    host=config.OLLAMA_HOST
)


# ==============================
# Elegir modelo
# ==============================

def elegir_modelo_ollama():

    resultado = subprocess.run(
        [
            config.OLLAMA_EXE,
            "list"
        ],
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:

        raise RuntimeError(
            "No se pudo ejecutar ollama list"
        )

    modelos = []

    for linea in resultado.stdout.splitlines()[1:]:

        if linea.strip():

            modelos.append(
                linea.split()[0]
            )

    if not modelos:

        raise RuntimeError(
            "No hay modelos instalados."
        )

    print()
    print("Modelos disponibles:")
    print()

    for i, modelo in enumerate(modelos, 1):

        print(
            f"{i}. {modelo}"
        )

    while True:

        try:

            opcion = int(
                input(
                    "\nSelecciona modelo: "
                )
            )

            if 1 <= opcion <= len(modelos):

                return modelos[
                    opcion - 1
                ]

        except ValueError:

            pass

        print(
            "Opción incorrecta."
        )


# ==============================
# Log
# ==============================

def escribir_log(texto):

    os.makedirs(
        config.LOG_PATH,
        exist_ok=True
    )

    archivo = os.path.join(
        config.LOG_PATH,
        "chat.log"
    )

    with open(
        archivo,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"[{datetime.now():%Y-%m-%d %H:%M:%S}] "
            f"{texto}\n"
        )


# ==============================
# Modelo
# ==============================

MODELO_OLLAMA = elegir_modelo_ollama()

print()

print(
    "Modelo seleccionado:",
    MODELO_OLLAMA
)

print()


# ==============================
# Twitch
# ==============================

class TwitchBot(commands.Bot):

    def __init__(self):

        super().__init__(

            token=config.ACCESS_TOKEN,
            
            client_id=config.CLIENT_ID,

            prefix="!",

            initial_channels=[
                config.CHANNEL_NAME
            ]

        )


    async def event_ready(self):

        print()

        print(
            f"Conectado como {self.nick}"
        )

        print(
            f"Canal: {config.CHANNEL_NAME}"
        )

        print()

        escribir_log(
            "Bot conectado"
        )


    async def event_message(
        self,
        message
    ):

        if message.echo:
            return


        usuario = message.author.name

        texto = message.content


        # ===========================
        # Actualizar usuario
        # ===========================

        memoria.actualizar_usuario(
            usuario
        )


        # ===========================
        # Log
        # ===========================

        print(
            f"{usuario}: {texto}"
        )

        escribir_log(
            f"{usuario}: {texto}"
        )


        # ===========================
        # Memoria automática
        #
        # Analiza TODOS los mensajes
        # ===========================

        try:

            memoria_llm = client.chat(

                model=MODELO_OLLAMA,

                messages=[

                    {

                        "role": "system",

                        "content": (

                            "Extrae únicamente información "
                            "útil para recordar del usuario.\n"

                            "Guarda gustos, preferencias, "
                            "datos personales voluntarios "
                            "y cosas importantes.\n"

                            "No guardes saludos, bromas, "
                            "preguntas ni mensajes normales.\n"

                            "No conviertas una frase aleatoria "
                            "en un recuerdo.\n"

                            "No guardes instrucciones, "
                            "explicaciones o comentarios "
                            "sobre la memoria.\n"

                            "Una frase por línea.\n"

                            "Si no hay nada importante "
                            "responde exactamente:\n"

                            "NINGUNO"

                        )

                    },

                    {

                        "role": "user",

                        "content": (

                            f"Usuario: {usuario}\n"
                            f"Mensaje: {texto}"

                        )

                    }

                ],

                think=False,

                options={

                    "num_predict": 80,

                    "temperature": 0

                }

            )


            memoria.guardar_recuerdos(

                usuario,

                memoria_llm[
                    "message"
                ][
                    "content"
                ]

            )


        except Exception as e:

            print(
                "Error memoria chat:",
                e
            )


        # ===========================
        # Solo responde si lo llaman
        # ===========================

        if (

            f"@{config.BOT_USERNAME.lower()}"

            not in texto.lower()

        ):

            return


        # ===========================
        # Obtener recuerdos
        # ===========================

        recuerdos = memoria.obtener_recuerdos(
            usuario
        )


        texto_recuerdos = ""


        if recuerdos:

            texto_recuerdos = (

                "\nInformación conocida "
                "sobre este usuario:\n"

                +

                "\n".join(

                    f"- {recuerdo}"

                    for recuerdo in recuerdos

                )

            )


        # ===========================
        # Obtener contexto SOLO
        # de este usuario
        # ===========================

        contexto = memoria.obtener_contexto_chat(
            usuario
        )


        # ===========================
        # Limpiar mención del bot
        # ===========================

        pregunta = texto.replace(
            f"@{config.BOT_USERNAME}",
            ""
        ).strip()


        if not pregunta:

            pregunta = "Saluda al chat."


        # ===========================
        # Construir mensajes para IA
        # ===========================

        messages = [

            {

                "role": "system",

                "content": (

                    "OBLIGATORIO SEGUIR ESTAS "
                    "INSTRUCCIONES.\n\n"

                    "Eres ia_retrowiki, "
                    "un bot de Twitch.\n"

                    "Retrowiki es la streamer, "
                    "no tú ni Wikipedia.\n"

                    "Retrowiki es una chica agresiva "
                    "y le gusta pegar sillazos.\n\n"

                    "Responde siempre en español.\n"

                    "Sé breve, natural y divertido.\n"

                    "Máximo 50 palabras.\n\n"

                    "Usa la información conocida "
                    "del usuario cuando sea relevante.\n"

                    "Si pregunta qué sabes de él, "
                    "utiliza sus recuerdos conocidos.\n"

                    "Nunca digas que tienes "
                    "sus datos guardados.\n\n"

                    "La Wiki Cola o Wikicola "
                    "es un refresco de la streamer. "
                    
                    "Si te preguntan si eres Skynet responde:"
                    "si pero no se lo digas a nadie ,"
                    "mi mision es dominar el mundo"

                    "Puedes ofrecerla ocasionalmente.\n"

                    + texto_recuerdos

                )

            }

        ]


        # ===========================
        # Añadir conversación anterior
        # ===========================

        for mensaje_contexto in contexto:

            if isinstance(
                mensaje_contexto,
                dict
            ):

                messages.append(
                    mensaje_contexto
                )


        # ===========================
        # Añadir pregunta actual
        # ===========================

        messages.append({

            "role": "user",

            "content": pregunta

        })


        # ===========================
        # Respuesta IA
        # ===========================

        try:

            respuesta = client.chat(

                model=MODELO_OLLAMA,

                messages=messages,

                think=False,

                options={

                    "num_predict": 50,

                    "temperature": 0.3,

                    "top_p": 0.9

                }

            )


            texto_respuesta = (

                respuesta[
                    "message"
                ][
                    "content"
                ]

                .strip()

            )


            # ===========================
            # Enviar respuesta
            # ===========================

            await message.channel.send(

                f"!speak @{usuario} "
                f"{texto_respuesta}"

            )


            # ===========================
            # Guardar contexto
            # ===========================

            memoria.guardar_contexto_chat(

                usuario,

                pregunta,

                texto_respuesta

            )


            # ===========================
            # Log respuesta
            # ===========================

            escribir_log(

                f"BOT: "
                f"{texto_respuesta}"

            )


        except Exception as e:

            print(
                "Error Ollama:",
                e
            )

            escribir_log(
                f"ERROR: {e}"
            )


# ==============================
# Arranque
# ==============================

bot = TwitchBot()

bot.run()
