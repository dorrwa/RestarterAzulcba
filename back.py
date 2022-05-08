# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler# creating a Flask app
app = Flask(__name__)
import RPi.GPIO as GPIO
import time
import os

hostnames = ["google.com","192.168.0.1"]
pins=[20,30]

def ping(num):
    response = os.system("ping -c 1 " + hostnames[num])
    if response == 0:
        print(hostnames[num], 'is up!')
        return False
    else:
        print(hostnames[num], 'is down!')
        return True
def enviarPulsoDe(segs,rignum):
    GPIO.output(pins[rignum], GPIO.HIGH)
    time.sleep(segs)
    GPIO.output(pins[rignum], GPIO.LOW)

def checkSensors():
    for i in range(len(hostnames)):
        if ping(i):
            enviarPulsoDe(5,i)

sched = BackgroundScheduler(daemon=True)
sched.add_job(checkSensors(),'interval',seconds=300)
sched.start()
"""
LED_PIN = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
print("prender")
GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(2)
GPIO.output(LED_PIN, GPIO.LOW)
def sensor():
    GPIO.setup(LED_PIN, GPIO.OUT)
    print("prender")
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(3)
    print("apagar")
    GPIO.output(LED_PIN, GPIO.LOW)
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',seconds=5)
sched.start()
"""
@app.route('/turnon/<int:num>', methods=['GET'])
def turnon(num):
    if (request.method == 'GET'):
        data = "Recibido"
        print(data)
        enviarPulsoDe(1,num)
        return jsonify({'data': data})
    if (request.method == 'POST'):
        data = request.get_json()
        return data
@app.route('/turnoff/<int:num>', methods=['GET'])
def turnoff(num):
    if (request.method == 'GET'):
        data = "Recibido"
        enviarPulsoDe(5, num)
        return jsonify({'data': data})
    if (request.method == 'POST'):
        data = request.get_json()
    return data
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
# driver function
if __name__ == '__main__':
    app.run(debug=True)
