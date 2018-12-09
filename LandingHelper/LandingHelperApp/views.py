import sys
sys.path.append('C:\\Users\\Aaron\\Source\\Repos\\LandingHelper')
sys.path.append('C:\\Users\\Aaron\\Source\\Repos\\LandingHelper\\LandingHelper')
import core
from flask import Flask, render_template, session,request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import threading
from threading import Thread, Lock
from math import sqrt
import json
import random
import time
async_mode = 'threading'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode=async_mode)
connected = False
thread = None
thread_lock = Lock()
@app.route('/')
def mainpage():
    
    return render_template('main.html', async_mode=socketio.async_mode)

#@app.route('/distance')
#def generate():

#    distance = str(random.randint(1,100))
#    return json.dumps({'distance': core.dataProviderData})
    
#@socketio.on('my event')
def distance():
    config = 'C:/Users/Aaron/Source/Repos/LandingHelper/LandingHelper/config.json'
    coreapp = core.coreApp(config)
    t = threading.Thread(target=coreapp.run)
    t.start()
    while True:
        socketio.sleep(.01)
        #distance = str(random.randint(1,100))+'ft'
        socketio.emit('my_response', {'data': core.dataProviderData})
@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = threading.Thread(target=distance)
            thread.start()
    emit('my_response', {'data': 'Connected', 'count': 1})
if __name__ == '__main__':
    socketio.run(app, debug = True)
