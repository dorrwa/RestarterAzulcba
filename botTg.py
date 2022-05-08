from multiprocessing import Process
import time
import config
from telegram.ext import (Updater, CommandHandler)
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
from datetime import datetime
import requests
"""def mesAnterior(update, context):
    client = Client(config.API_KEY, config.API_SECRET)
    total = 0
    dphistory = client.get_deposit_history(coin="ETH")
    df = pd.DataFrame(dphistory,
                      columns=['amount', 'coin', 'network', 'status', 'address', 'addressTag', 'txId', 'insertTime',
                               'transferType', 'unlockConfirm'])
    df.insertTime = df.insertTime.apply(lambda x: pd.to_datetime(x, utc=True, unit='ms'))
    for index, row in df.iterrows():
        amount = row["amount"]
        fecha = row["insertTime"]
        coin = row["coin"]
        address = row["address"]
        if fecha.month == (datetime.now().month - 1)  and coin == 'ETH':
            total += float(amount)
    mensaje= "En el mes "+str(datetime.now().month-1)+ " acumulamos un total de: " + str(total) + " ETH"
    context.bot.send_message(update.message.chat_id, mensaje)
"""
def turnon(update,context):
    try:
        print(context.args[0])
        mensaje = str(context.args[0])
        response = requests.get("http://127.0.0.1:5000/turnon/"+str(context.args[0]))
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
    #dp.add_handler(CommandHandler('mesAnterior', mesAnterior))
    dp.add_handler(CommandHandler('turnon', turnon))
    dp.add_handler(CommandHandler('help', help))
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()

if __name__=='__main__':
    p1 = Process(target = tgbot())
    p1.start()
