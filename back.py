# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler# creating a Flask app
#app = Flask(__name__)
import RPi.GPIO as GPIO
import time
LED_PIN = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
print("prender")
GPIO.output(LED_PIN, GPIO.HIGH)
time.sleep(2)
GPIO.output(LED_PIN, GPIO.LOW)
def sensor():
    """ Function for test purposes. """
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
@app.route('/login', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        data = "hello world"
@@ -28,4 +41,4 @@ def disp(num):
# driver function
if __name__ == '__main__':
    app.run(debug=True) 
 
