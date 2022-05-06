from multiprocessing import Process
import time
import config
from telegram.ext import (Updater, CommandHandler)
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
from datetime import datetime

def mesActual(update, context):
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
        if fecha.month == (datetime.now().month )  and coin=='ETH':
            total += float(amount)

    mensaje = "En el mes " + str(datetime.now().month) + " vamos acumulando un total de: " + str(total) + " ETH"
    context.bot.send_message(update.message.chat_id, mensaje)
def zil(update, context):
    client = Client(config.API_KEY, config.API_SECRET)
    total = 0
    dphistory = client.get_deposit_history(coin="ZIL")
    df = pd.DataFrame(dphistory,
                      columns=['amount', 'coin', 'network', 'status', 'address', 'addressTag', 'txId', 'insertTime',
                               'transferType', 'unlockConfirm'])
    df.insertTime = df.insertTime.apply(lambda x: pd.to_datetime(x, utc=True, unit='ms'))
    for index, row in df.iterrows():
        amount = row["amount"]
        fecha = row["insertTime"]
        coin = row["coin"]
        address = row["address"]
        if coin=='ZIL':
            total += float(amount)

    mensaje = " vamos acumulando un total de: " + str(total) + " ZIL"
    context.bot.send_message(update.message.chat_id, mensaje)

def mesAnterior(update, context):
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
def help(update, context):
    context.bot.send_message(update.message.chat_id, "Lista de comandos \n /mesActual - Total ETH en el mes \n /mesAnterior - Total ETH en el mes anterior")
def tgbot():
    TOKEN = config.TGTOKEN
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Eventos que activarán nuestro bot.
    dp.add_handler(CommandHandler('mesActual', mesActual))
    dp.add_handler(CommandHandler('mesAnterior', mesAnterior))
    dp.add_handler(CommandHandler('zil', zil))
    dp.add_handler(CommandHandler('help', help))
    # Comienza el bot
    updater.start_polling()
    # Lo deja a la escucha. Evita que se detenga.
    updater.idle()

if __name__=='__main__':
    p1 = Process(target = tgbot())
    p1.start()
