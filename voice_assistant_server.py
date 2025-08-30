from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import subprocess
import signal
import time
import os

app = Flask(__name__)
CORS(app)

echo_process = None
vision_process = None

def run_echo():
    global echo_process
    echo_process = subprocess.Popen(['python', 'voice_assistant.py'])

def run_vision():
    global vision_process
    vision_process = subprocess.Popen(['python', 'camera.py'])

@app.route('/start_walle', methods=['POST'])
def start_echo():
    global echo_process
    if echo_process is None or echo_process.poll() is not None:
        threading.Thread(target=run_echo).start()
        return jsonify({"status": "walle started"})
    return jsonify({"status": "walle already running"})

@app.route('/stop_walle', methods=['POST'])
def stop_echo():
    global echo_process
    if echo_process and echo_process.poll() is None:
        echo_process.terminate()
        echo_process = None
        return jsonify({"status": "walle stopped"})
    return jsonify({"status": "walle not running"})

@app.route('/start_vision', methods=['POST'])
def start_vision():
    global vision_process
    if vision_process is None or vision_process.poll() is not None:
        threading.Thread(target=run_vision).start()
        return jsonify({"status": "Vision started"})
    return jsonify({"status": "Vision already running"})

@app.route('/stop_vision', methods=['POST'])
def stop_vision():
    global vision_process
    if vision_process and vision_process.poll() is None:
        vision_process.terminate()
        vision_process = None
        return jsonify({"status": "Vision stopped"})
    return jsonify({"status": "Vision not running"})

if __name__ == '__main__':
    app.run(debug=True)