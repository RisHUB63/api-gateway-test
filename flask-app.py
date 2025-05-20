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
