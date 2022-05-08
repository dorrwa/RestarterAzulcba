from multiprocessing import Process
import config
from telegram.ext import (Updater, CommandHandler)
import requests

def turnon(update,context):
    try:
        print(context.args[0])
        mensaje = str(context.args[0])
        response = requests.get("http://127.0.0.1:5000/turnon/"+str(context.args[0]))
        print(response)
        context.bot.send_message(update.message.chat_id, mensaje)
    except:
        context.bot.send_message(update.message.chat_id, "Ingrese un valor")

def turnoff(update,context):
    try:
        print(context.args[0])
        mensaje = str(context.args[0])
        response = requests.get("http://127.0.0.1:5000/turnoff/"+str(context.args[0]))
        print(response)
        context.bot.send_message(update.message.chat_id, mensaje)
    except:
        context.bot.send_message(update.message.chat_id, "Ingrese un valor")

def reset(update,context):
    try:
        print(context.args[0])
        mensaje = str(context.args[0])
        response = requests.get("http://127.0.0.1:5000/reset/"+str(context.args[0]))
        print(response)
        context.bot.send_message(update.message.chat_id, mensaje)
    except:
        context.bot.send_message(update.message.chat_id, "Ingrese un valor")
def help(update, context):
    context.bot.send_message(update.message.chat_id, "Lista de comandos \n /turnon + numero - prender rig numero x \n /turnoff + numero - apagar rig numero x \n /restart numero - restartea el rig")
def tgbot():
    TOKEN = config.TGTOKEN
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Eventos que activarán nuestro bot.
    dp.add_handler(CommandHandler('turnon', turnon))
    dp.add_handler(CommandHandler('turnoff', turnoff))
    dp.add_handler(CommandHandler('reset', reset))
    dp.add_handler(CommandHandler('help', help))
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()

if __name__=='__main__':
    p1 = Process(target = tgbot())
    p1.start()
