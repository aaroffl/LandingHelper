#!/usr/bin/env python
import sys
sys.path.append('C:\\Users\\Aaron\\Source\\Repos\\LandingHelper')
sys.path.append('C:\\Users\\Aaron\\Source\\Repos\\LandingHelper\LandingHelper')
from flask import Flask, render_template, session,request
#from LandingHelper import *
from LandingHelper import core
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import threading
from threading import Thread, Lock
from math import sqrt
import json
import random
import time
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

@app.route('/')
def mainpage():
    #app = core.coreApp()
    #t = threading.Thread(target=app.run)
    #t.start()


    #t.join()
    return render_template('main.html', async_mode=socketio.async_mode)

#@app.route('/distance')
#def generate():

#    distance = str(random.randint(1,100))
#    return json.dumps({'distance': core.dataProviderData})
    
#@socketio.on('my event')
def distance():
    while True:
        socketio.sleep(.5)
        distance = str(random.randint(1,100))
        socketio.emit('my_response', {'data':distance})

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

