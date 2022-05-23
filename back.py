from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)
import RPi.GPIO as GPIO
import time
import os
import sqlite3 as sql
import config

def createDB():
    con = sql.connect("dbRigs.db")
    con.commit()
    con.close()

def createTable():
    con = sql.connect("dbRigs.db")
    cursor= con.cursor()
    cursor.execute(
        """CREATE TABLE rigs(
            id integer,
            estado integer
        )"""
    )
    con.commit()
    con.close()

def hostnamesSetup():
    con= sql.connect(db)
    cursor = con.cursor()
    for i in range(len(hostnames)):
        instr = f"INSERT INTO rigs VALUES ('{i}','{1}')"
        cursor.execute(instr)
        con.commit()
    con.close()
def updateField(id,estado):
    con = sql.connect(db)
    cursor = con.cursor()
    instr = f"UPDATE rigs SET estado='{estado}' WHERE id = '{id}'"
    cursor.execute(instr)
    con.commit()
    con.close()

def checkFieldStatus(id):
    con = sql.connect(db)
    cursor = con.cursor()
    instr = f"SELECT * FROM rigs WHERE id = '{id}'"
    cursor.execute(instr)
    datos = cursor.fetchall()
    con.commit()
    con.close()
    return datos

def ping(num):
    response = os.system("ping -c 1 " + hostnames[num])
    if response == 0:
        print(hostnames[num], 'is up!')
        return False
    else:
        print(hostnames[num], 'is down!')
        return True

def enviarPulsoDe(segs,rignum):
    GPIO.output(pins[rignum], 0)
    time.sleep(segs)
    GPIO.output(pins[rignum], 1)

def checkSensors():
    for i in range(len(hostnames)):
        d = checkFieldStatus(i)
        if ping(i) and d[0][1] == 1:
            enviarPulsoDe(5,i)
            time.sleep(3)
            enviarPulsoDe(2,i)


#completar los hostnames con las ips
hostnames = config.HOSTNAMES
#completar los PINS con los GPIO acordes a cada hostname
pins=config.PINS
db= "dbRigs.db"
GPIO.setmode(GPIO.BOARD)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT, initial = 1)
    
if os.path.isfile(db) == False:
    createDB()
    createTable()
    hostnamesSetup()

sched = BackgroundScheduler(daemon=True)
sched.add_job(checkSensors,'interval',seconds=300)
sched.start()
@app.route('/turnon/<int:num>', methods=['GET'])
def turnon(num):
    if (request.method == 'GET'):
        data = "Recibido"
        print(data)
        enviarPulsoDe(1,num)
        updateField(num,1)
        return jsonify({'data': data})
    if (request.method == 'POST'):
        data = request.get_json()
        return data
@app.route('/turnoff/<int:num>', methods=['GET'])
def turnoff(num):
    if (request.method == 'GET'):

        data = "Recibido"
        enviarPulsoDe(5, num)
        updateField(num,0)
        return jsonify({'data': data})

@app.route('/reset/<int:num>', methods=['GET'])
def reset(num):
    if (request.method == 'GET'):
        data = "Recibido"
        enviarPulsoDe(5, num)
        time.sleep(1)
        enviarPulsoDe(1,num)
        return jsonify({'data': data})

def disp(num):
    return jsonify({'data': num ** 2})

if __name__ == '__main__':
    app.run(debug=True)