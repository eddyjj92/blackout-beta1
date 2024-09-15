import telebot
import time
import threading
import os
from telebot.types import ForceReply
from flask import Flask

# Inicializar Flask
app = Flask(__name__)


# Definir una ruta simple para Flask
@app.route('/')
def index():
    return "Hello World!"


# Token del bot de Telegram
TELEGRAM_TOKEN = '7137585979:AAF5pjZPpnqbvo9xtneohUPBoQB5sErQubc'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# IDs de administradores
chat_id_lorenzo = 1314659664
chat_id_arturo = 1319934926
chat_id_javier = 5609400867

# Almacenar los datos de los usuarios
usuarios = {}
enviar_invitacion = [""]


# Comando /start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, 'Hola, este es el bot de Blackout. Usa "/" para ver los comandos.')


# Comando oculto para administradores
@bot.message_handler(commands=["admin"])
def cmd_admin(message):
    markup = ForceReply()
    if message.chat.id not in [chat_id_lorenzo, chat_id_arturo, chat_id_javier]:
        bot.send_message(message.chat.id, "No está autorizado para usar el modo administrador")
        return

    bot.send_chat_action(message.chat.id, 'typing')
    msg = bot.send_message(message.chat.id, "Escribe 'lista' o 'reiniciar'", reply_markup=markup)
    bot.register_next_step_handler(msg, cmd_reset)


def cmd_reset(message):
    if message.text == 'lista':
        archivo3 = open("datos.txt", "rb")
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_document(message.chat.id, archivo3, caption="Lista de invitados")
    elif message.text == "reiniciar":
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "Reiniciando...")
        time.sleep(2)
        usuarios.clear()
        with open("informacion.txt", 'w') as info2:
            info2.write("   ")
        with open("datos.txt", 'w') as data2:
            data2.write("   ")
        bot.send_message(message.chat.id, "Bot reiniciado.")
    else:
        msg = bot.send_message(message.chat.id, "Comando incorrecto.")
        bot.register_next_step_handler(msg, cmd_reset)


# Comando /ayuda
@bot.message_handler(commands=["ayuda"])
def cmd_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, "Este bot está en desarrollo para gestionar tus invitaciones.")
    time.sleep(2)
    bot.send_message(message.chat.id, 'Usa "/invitacion" para obtener tu invitación.')


# Comando /invitacion
@bot.message_handler(commands=["invitacion"])
def preguntar_nombre(message):
    markup = ForceReply()
    bot.send_chat_action(message.chat.id, 'typing')
    msg = bot.send_message(message.chat.id, "Escribe tu nombre y apellido", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_carnet)


def preguntar_carnet(message):
    if " " not in message.text:
        msg = bot.send_message(message.chat.id, "Debes escribir tu nombre y apellido.")
        bot.register_next_step_handler(msg, preguntar_carnet)
    else:
        usuarios[message.chat.id] = {"nombre_y_apellidos": message.text}
        bot.send_chat_action(message.chat.id, 'typing')
        markup = ForceReply()
        msg = bot.send_message(message.chat.id, "Envía tu número de Carnet de Identidad", reply_markup=markup)
        bot.register_next_step_handler(msg, guardar_datos_usuario)


def guardar_datos_usuario(message):
    if not message.text.isdigit() or len(message.text) != 11:
        msg = bot.send_message(message.chat.id, "ERROR: Debes enviar un número válido de 11 dígitos.")
        bot.register_next_step_handler(msg, guardar_datos_usuario)
    else:
        usuarios[message.chat.id]["numero_de_carnet"] = message.text
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, "Datos registrados. Espera...")
        time.sleep(3)

        with open("informacion.txt", "r+") as info:
            invitacion = info.readline().strip()
            if not invitacion:
                invitacion = "001"
            else:
                invitacion = str(int(invitacion) + 1).zfill(3)
            info.seek(0)
            info.write(invitacion)

        mensaje_a_enviar = f"Su invitación es la número: {invitacion}"
        bot.send_message(message.chat.id, mensaje_a_enviar)

        with open('datos.txt', 'a') as archivo:
            archivo.write(
                f"{invitacion} {usuarios[message.chat.id]['nombre_y_apellidos']} {usuarios[message.chat.id]['numero_de_carnet']}\n")

        bot.send_message(message.chat.id, "Invitación registrada. Usa /invitacion para pedir otra.")


# Responder a otros mensajes
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "Este comando no está disponible.")
    else:
        bot.send_message(message.chat.id, "No soy para chatear, usa un comando.")


# Iniciar el bot en un hilo separado
def detectar_mensajes():
    bot.infinity_polling()


if __name__ == '__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "da la bienvenida al usuario"),
        telebot.types.BotCommand("/ayuda", "breve descripción del bot"),
        telebot.types.BotCommand("/invitacion", "obtener tu invitación")
    ])
    threading.Thread(target=detectar_mensajes).start()

    # Iniciar el servidor Flask
    port = int(os.environ.get("PORT", 4000))
    app.run(debug=True, host='0.0.0.0', port=port)