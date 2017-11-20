from flask import Flask, render_template
from LandingHelper import core
from flask_socketio import SocketIO
from threading import Thread
from math import sqrt
import json
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
socketio = SocketIO(app)
thread = None

@app.route('/')
def mainpage():
    return render_template('main.html')

@app.route('/distance')
def generate():
    distance = str(random.randint(1,100))
    return json.dumps({'distance': distance})

if __name__ == '__main__':
    socketio.run(app)

