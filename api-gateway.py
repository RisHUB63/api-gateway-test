# **2. API Gateway (gateway.py)**

# ```python
from flask import Flask, request, jsonify
import http.client
import threading
import time
from urllib.parse import urlparse
from collections import deque

app = Flask(__name__)

PORT = 8000
registered_servers = {'server-1': {'url': 'http://127.0.0.1:5000', 'healthy': True, 'request_count': 0},
                      'server-2': {'url': 'http://127.0.0.1:5001', 'healthy': True, 'request_count': 0},
                      'server-3': {'url': 'http://127.0.0.1:5002', 'healthy': True, 'request_count': 0}}

request_logs = deque(maxlen=10000)
API_PREFIX = '/api'
HEALTH_CHECK_PATH = '/health'
MAX_REQUESTS_PER_SECOND = 100


def check_server_health(server_name):
    """Checks the health of a registered server."""
    server = registered_servers.get(server_name)
    if not server:
        return

    try:
        parsed_url = urlparse(server['url'])
        conn = http.client.HTTPConnection(parsed_url.netloc) if parsed_url.scheme == 'http' else http.client.HTTPSConnection(parsed_url.netloc)
        conn.request("GET", HEALTH_CHECK_PATH, timeout=5)
        response = conn.getresponse()

        if response.status == 200:
            server['healthy'] = True
        else:
            server['healthy'] = False
            print(f"Server {server_name} is unhealthy: {response.status} - {response.reason}")
        conn.close()
    except Exception as e:
        server['healthy'] = False
        print(f"Error checking health of {server_name}: {e}")


@app.route(f'{API_PREFIX}/servers', methods=['GET'])
def get_servers():
    """Returns a list of registered servers."""
    server_list = [{'name': name, 'url': server['url'], 'healthy': server['healthy']}
                   for name, server in registered_servers.items()]
    return jsonify(server_list)



def calculate_stats(period):
    """Calculates statistics based on request logs."""
    now = time.time()
    filtered_logs = [log for log in request_logs if now - log['timestamp'] <= period]

    if not filtered_logs:
        return {
            'rpm': 0,
            'rps': 0,
            'p99': 0,
            'p95': 0,
            'endpoints': {},
            'hosts': {},
        }

    total_requests = len(filtered_logs)
    duration_in_seconds = now - filtered_logs[0]['timestamp']
    rpm = (total_requests / (duration_in_seconds / 60)) if duration_in_seconds else 0
    rps = (total_requests / duration_in_seconds) if duration_in_seconds else 0

    response_times = sorted([log['response_time'] for log in filtered_logs])
    p99_index = int(len(response_times) * 0.99) - 1
    p95_index = int(len(response_times) * 0.95) - 1
    p99 = response_times[p99_index] if response_times else 0
    p95 = response_times[p95_index] if response_times else 0

    endpoints = {}
    hosts = {}
    for log in filtered_logs:
        endpoints[log['path']] = endpoints.get(log['path'], 0) + 1
        hosts[log['target_host']] = hosts.get(log['target_host'], 0) + 1

    return {
        'rpm': round(rpm, 2),
        'rps': round(rps, 2),
        'p99': round(p99, 2),
        'p95': round(p95, 2),
        'endpoints': endpoints,
        'hosts': hosts,
    }


def get_least_loaded_server(servers) -> str:

    if not servers:
        return None  # Handle the case of an empty dictionary

    min_requests = float('inf')  # Start with infinity to find the true minimum
    least_loaded_server = None

    for server_name, request_data in servers.items():
        if request_data.get('request_count') < min_requests:
            min_requests = request_data.get('request_count')
            least_loaded_server = servers[server_name]

    return least_loaded_server



@app.route(f'{API_PREFIX}/stats/<period>', methods=['GET'])
def get_stats(period):
    """Returns statistics for a specified time period."""
    if period not in ['1m', '5m', '1h']:
        return jsonify({'error': 'Invalid period. Use 1m, 5m, or 1h.'}), 400
    stats = calculate_stats({
        '1m': 60,
        '5m': 5 * 60,
        '1h': 60 * 60
    }[period])
    return jsonify(stats)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    """Proxies requests to registered servers with load balancing and error handling."""    

    # Not implemenent the health check here

    # Load balancing
    server = get_least_loaded_server(servers=registered_servers)
    
    target_url = server['url'] + path.replace('api', '')
    start_time = time.time()
    try:
        parsed_url = urlparse(target_url)
        conn = http.client.HTTPConnection(parsed_url.netloc) if parsed_url.scheme == 'http' else http.client.HTTPSConnection(parsed_url.netloc)

        # Forward headers
        headers = dict(request.headers)
        if 'Host' in headers:
            del headers['Host']
        conn.request(request.method, parsed_url.path, body=request.get_data(), headers=headers)
        proxy_response = conn.getresponse()
        end_time = time.time()
        response_time = (end_time - start_time) * 1000

        # Log the request
        request_logs.append({
            'timestamp': time.time(),
            'method': request.method,
            'path': path,
            'target_host': server['url'],
            'status_code': proxy_response.status,
            'response_time': response_time,
        })
        server['request_count'] += 1

        # Copy headers
        response_headers = dict(proxy_response.getheaders())
        # Change Here
        response_body = proxy_response.read().decode() # Read response
        flask_response = jsonify(response_body) # jsonify
        flask_response.status_code = proxy_response.status
        for k, v in response_headers.items():
            flask_response.headers[k] = v
        conn.close()
        return flask_response

    except Exception as e:
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        print(f'Error proxying to {server["url"]}: {e}')
        request_logs.append({
            'timestamp': time.time(),
            'method': request.method,
            'path': path,
            'target_host': server['url'],
            'status_code': 500,
            'response_time': response_time,
            'error': str(e),
        })
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)