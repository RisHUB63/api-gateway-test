# **1. Flask Dummy Backend (app.py)**

# ```python
from flask import Flask, jsonify
import time
import os
import socket

app = Flask(__name__)
PORT = int(os.environ.get('PORT', 5000))  # Use environment variable for port
HOSTNAME = socket.gethostname()

@app.route('/health')
def health():
    """Health check endpoint for the backend."""
    return jsonify({'status': 'OK', 'port': PORT, 'hostname': HOSTNAME}), 200

@app.route('/create')
def create():
    """Endpoint to simulate data retrieval with a small delay."""
    time.sleep(0.9)  # Simulate a 100ms delay
    return jsonify({'message': f'Data from backend on port {PORT} and hostname {HOSTNAME}', 'port': PORT, 'hostname': HOSTNAME}), 200


@app.route('/update')
def update():
    """Endpoint to simulate data retrieval with a small delay."""
    time.sleep(0.5)  # Simulate a 100ms delay
    return jsonify({'message': f'Data from backend on port {PORT} and hostname {HOSTNAME}', 'port': PORT, 'hostname': HOSTNAME}), 200


@app.route('/delete')
def delete():
    """Endpoint to simulate data retrieval with a small delay."""
    time.sleep(0.3)  # Simulate a 100ms delay
    return jsonify({'message': f'Data from backend on port {PORT} and hostname {HOSTNAME}', 'port': PORT, 'hostname': HOSTNAME}), 200



@app.route('/list')
def list():
    """Endpoint to simulate data retrieval with a small delay."""
    time.sleep(1)  # Simulate a 100ms delay
    return jsonify({'message': f'Data from backend on port {PORT} and hostname {HOSTNAME}', 'port': PORT, 'hostname': HOSTNAME}), 200


@app.route('/format')
def format():
    """Endpoint to simulate data retrieval with a small delay."""
    time.sleep(0.8)  # Simulate a 100ms delay
    return jsonify({'message': f'Data from backend on port {PORT} and hostname {HOSTNAME}', 'port': PORT, 'hostname': HOSTNAME}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=False) #changed to false
# ```

# * This Flask app has two endpoints:
#     * `/health`: Returns a 200 OK status, the port it's running on, and the hostname.
#     * `/data`: Returns a JSON response with a message, the port, and the hostname, and also has a 100ms delay.
# * It uses an environment variable `PORT` to determine the port it runs on, defaulting to 5000. This is important for running multiple instances.
# * The `socket` module is used to get the hostname of the machine.