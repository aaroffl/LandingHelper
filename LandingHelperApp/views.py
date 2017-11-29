import sys
sys.path.append('C:\\Users\\Aaron\\Source\\Repos\\LandingHelper')
sys.path.append('C:\\Users\\Aaron\\Source\\Repos\\LandingHelper\LandingHelper')
from flask import Flask, render_template
#from LandingHelper import *
from LandingHelper import core
from flask_socketio import SocketIO
import threading
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
    app = core.coreApp()
    t = threading.Thread(target=app.run)
    t.start()
    #t.join()
    return render_template('main.html')

@app.route('/distance')
def generate():

    distance = str(random.randint(1,100))
    return json.dumps({'distance': core.dataProviderData})
    

if __name__ == '__main__':
    socketio.run(app)

