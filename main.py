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

        print(f"{i}. {modelo}")

    while True:

        try:

            opcion = int(
                input(
                    "\nSelecciona modelo: "
                )
            )

            if (
                opcion >= 1
                and
                opcion <= len(modelos)
            ):

                return modelos[
                    opcion - 1
                ]

        except ValueError:

            pass

        print("Opción incorrecta.")


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
            f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {texto}\n"
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

        memoria.actualizar_usuario(
            usuario
        )

        texto = message.content

        print(
            f"{usuario}: {texto}"
        )

        escribir_log(
            f"{usuario}: {texto}"
        )

        if (
            f"@{config.BOT_USERNAME.lower()}"
            not in texto.lower()
        ):
            return

        recuerdos = memoria.obtener_recuerdos(
            usuario
        )

        texto_recuerdos = ""

        if recuerdos:

            texto_recuerdos = (
                "\nInformación conocida del usuario:\n- "
                +
                "\n- ".join(
                    recuerdos
                )
            )

        pregunta = texto.replace(
            f"@{config.BOT_USERNAME}",
            ""
        ).strip()

        if not pregunta:

            pregunta = "Saluda al chat."

        try:           
            respuesta = client.chat(

                model=MODELO_OLLAMA,

                messages=[

                    {
                        "role": "system",

                        "content": (

                            "Eres un bot de Twitch. "

                            "Responde siempre en español. "

                            "Sé breve, natural y divertido. "

                            "Máximo 20 palabras."

                            + texto_recuerdos

                        )

                    },

                    {
                        "role": "user",

                        "content": pregunta
                    }

                ],

                think=False,

                options={

                    "num_predict": 40,

                    "temperature": 0.7,

                    "top_p": 0.9

                }

            )

            texto_respuesta = (

                respuesta["message"]["content"]

                .strip()

            )

            await message.channel.send(

                f"@{usuario} {texto_respuesta}"

            )


            # ===========================
            # Memoria automática
            # ===========================

            try:
                memoria_llm = client.chat(

                    model=MODELO_OLLAMA,

                    messages=[

                        {

                            "role": "system",

                            "content": (

                                "Extrae únicamente información útil "

                                "para recordar del usuario.\n"

                                "Una frase por línea.\n"

                                "No expliques nada.\n"

                                "Si no hay nada importante responde exactamente:\n"

                                "NINGUNO"

                            )

                        },

                        {

                            "role": "user",

                            "content": pregunta

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

                    memoria_llm["message"]["content"]

                )

            except Exception as e:

                print(

                    "Error memoria:",

                    e

                )

            escribir_log(

                f"BOT: {texto_respuesta}"

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
