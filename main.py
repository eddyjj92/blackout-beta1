TELEGRAM_TOKEN='7137585979:AAF5pjZPpnqbvo9xtneohUPBoQB5sErQubc'
import telebot
import time
import threading
import json
import os
import sys
import platform
from telebot.types import ReplyKeyboardMarkup
from telebot.types import ForceReply
bot=telebot.TeleBot(TELEGRAM_TOKEN)
from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return "Hello World!"

chat_id_lorenzo=1314659664
chat_id_arturo=1319934926
chat_id_javier=5609400867
enviar_invitación=[""]
#ADMINS= ("1314659664","1319934926","5609400867")
usuarios={}
x="datos.txt"
contenido="\n"

@bot.message_handler(commands=["start"])    #definiendo nombre de comando start 
def cmd_start(message):                     #lee el comando y da la bienvenida al usuario
    bot.send_chat_action(message.chat.id, 'typing')         #esto es para que salga escribiendo...
    bot.reply_to(message,'Hola, este es el bot de Blackout, escribe "/" para ver la lista de comandos, para obtener más información escribe el comando "/ayuda"') #reply_to es una funcion del bot
@bot.message_handler(commands=["admin"])  #comando para administradores oculto
def cmd_admin(message):
    markup=ForceReply() 
    if(message.chat.id != chat_id_lorenzo and message.chat.id !=chat_id_arturo and message.chat.id != chat_id_javier):
        bot.send_message(message.chat.id,"No está autorizado para usar el modo administrador")
    elif(message.chat.id==chat_id_lorenzo):
        bot.send_chat_action(message.chat.id, 'typing')
        msg=bot.send_message(message.chat.id,"Hola Lorenzo, escribe 'lista' para recibir la lista de invitados o escribe 'reiniciar' para resetear el bot ",reply_markup=markup)
        bot.register_next_step_handler(msg,cmd_reset)
    elif(message.chat.id==chat_id_arturo):
        bot.send_chat_action(message.chat.id, 'typing')
        msg=bot.send_message(message.chat.id,"Hola Arturo, escribe 'lista' para recibir la lista de invitados o escribe 'reiniciar' para resetear el bot ",reply_markup=markup)
        bot.register_next_step_handler(msg,cmd_reset)
    elif(message.chat.id==chat_id_javier):
        bot.send_chat_action(message.chat.id, 'typing')
        msg=bot.send_message(message.chat.id,"Hola Javier, escribe 'lista' para recibir la lista de invitados o escribe 'reiniciar' para resetear el bot ",reply_markup=markup)
        bot.register_next_step_handler(msg,cmd_reset)
def cmd_reset(message):                       #para reiniciar el bot 
    markup=ForceReply()
    if(message.text=='lista'):
        archivo3=open("datos.txt","rb")
        bot.send_chat_action(message.chat.id,'typing')
        bot.send_document(message.chat.id,archivo3,caption="lista de invitados")
        
            
    elif(message.text=="reiniciar"): 
        bot.send_chat_action(message.chat.id, 'typing')   
        bot.send_message(message.chat.id,"Espere unos segundos...")
        time.sleep(4)
        usuarios.clear()
        with open("informacion.txt",'w',encoding="UTF-8") as info2:
            info2.write("   ")
        with open("datos.txt",'w',encoding="UTF-8") as data2:
            data2.write("   ")
            
        bot.send_message(message.chat.id,"El bot se ha reiniciado correctamente")
    else:
        msg=bot.send_message(message.chat.id,"Escribe correctamente el comando ")
        bot.register_next_step_handler(msg,cmd_reset)    
        
@bot.message_handler(commands=["ayuda"])                     #definiendo el comando help

def cmd_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, "Actualmente este es un bot en desarrollo, en el cuál por ahora podrás gestionar tus invitaciones a los eventos que realiza nuestro proyecto")
    
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Para obtener tu invitación utiliza el comando "/invitacion"')   #send_message es una funcion del bot
    
@bot.message_handler(commands=["invitacion"])                #definiendo el comando invitacion

def preguntar_nombre(message):
    markup=ForceReply()
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1) 
    chat_id =message.chat.id
    msg=bot.send_message(chat_id, "Escribe tu nombre y primer apellido", reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_carnet)
def preguntar_carnet(message):
    
    if(" " not in message.text):
        msg=bot.send_message(message.chat.id, "ERROR: Debes enviar tu nombre y primer apellido\nEscribe tu nombre y primer apellido")
        bot.register_next_step_handler(msg, preguntar_carnet)
    else:
        usuarios[message.chat.id]={}
        usuarios["nombre_y_apellidos"]=message.text
        
        
        bot.send_chat_action(message.chat.id, 'typing')
        chat_id =message.chat.id
        markup=ForceReply()
        msg=bot.send_message(chat_id, "Envía tu numero de Carnet de Identidad",reply_markup=markup)   
        bot.register_next_step_handler(msg,guardar_datos_usuario)

def guardar_datos_usuario(message):
    if not(message.text.isdigit):
        msg=bot.send_message(message.chat.id, "ERROR: Debes indicar un número de 11 dígitos.\nEnvía tu numero de Carnet de Identidad")
        bot.register_next_step_handler(msg,guardar_datos_usuario)
    else:
        usuarios["numero_de_carnet"]= message.text
        bot.send_chat_action(message.chat.id, 'typing')
        time.sleep(1)
        bot.send_message(message.chat.id,"Se han registrado sus datos, espere unos segundos...")
        time.sleep(3)
        
        
        info=open("informacion.txt",encoding="UTF-8")
        invitación=info.readline(3)
        if(invitación=="   "):
            
            info.close()
            invitación="001"
            with open('informacion.txt','w',encoding="UTF-8") as data:
                data.write("001")
    
        elif(invitación!="   "):
            info.close()
            invitación=list(invitación)
            invitación[0]=int(invitación[0])
            invitación[1]=int(invitación[1])
            invitación[2]=int(invitación[2])
            
            if(invitación[2]==9 and invitación[1]==9):
                invitación[0]+=1
                invitación[1]=0
                invitación[2]=0
            elif(invitación[2]==9):
                invitación[1]+=1
                invitación[2]=0
            elif(invitación[2]<9 and invitación[1]<9):
                invitación[2]+=1   
            
            invitación[0]=str(invitación[0])
            invitación[1]=str(invitación[1])
            invitación[2]=str(invitación[2])
        enviar_invitación=invitación[0]+invitación[1]+invitación[2]
        with open("informacion.txt","w",encoding="UTF-8") as info1:
            info1.write(enviar_invitación)
        mensaje_a_enviar="Su invitación es la número: "+enviar_invitación
        bot.send_message(message.chat.id,mensaje_a_enviar)
        
        with open('datos.txt','a',encoding="UTF-8") as archivo1:
            
            escribir_nombre=usuarios.get("nombre_y_apellidos")
            escribir_carnet=usuarios.get("numero_de_carnet")
            escribir_nombre=str(escribir_nombre)
            escribir_carnet=str(escribir_carnet)
        
            archivo1.writelines(["\n",enviar_invitación," ",escribir_nombre," ",escribir_carnet,]) 
        usuarios.pop("nombre_y_apellidos")
        usuarios.pop("numero_de_carnet")
        time.sleep(1)
        bot.send_message(message.chat.id,"Si desea pedir otra invitación escriba el comando /invitacion")
        
        

@bot.message_handler(content_types=["text"])               #respondiendo a texto del usuario

def bot_mensajes_texto(message):
    if message.text and message.text.startswith("/"):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,"Este comando no está disponible")
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id,"No soy para chatear, envía un comando")








def detectar_mensajes():
    bot.infinity_polling()

if __name__=='__main__':
    bot.set_my_commands([
        telebot.types.BotCommand("/start","da la bienvenida al usuario"),
        telebot.types.BotCommand("/ayuda","breve descripción del bot"),
        telebot.types.BotCommand("/invitacion","aquí puedes obtener tu invitación")
    ])
    print('Iniciando el bot')
    hilo_bot=threading.Thread(name="hilo_bot",target=detectar_mensajes)
    hilo_bot.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
