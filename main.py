# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
# creating a Flask app
app = Flask(__name__)

def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=60)
sched.start()
@app.route('/login', methods=['GET', 'POST'])
def home():
    if (request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})
    if (request.method == 'POST'):
        data = request.get_json()
        return data

@app.route('/home/<int:num>', methods=['GET'])
def disp(num):
    return jsonify({'data': num ** 2})


# driver function
if __name__ == '__main__':
    app.run(debug=True)