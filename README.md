# Load Testing Environment Setup For API-Gateway

This document outlines the steps to set up and run a load test using Locust, an API gateway (Flask), and dummy backend servers (Flask).

## Components

* **Locust (`locustfile.py`)**: Defines the load test behavior.
    * `wait_time`: Simulates users waiting between 1 and 3 seconds between requests.
    * `on_start`: Registers the dummy servers with the gateway. The server names are hardcoded here.
    * `get_data`: Sends a GET request to the `/api/data` endpoint via the gateway.
* **API Gateway (`gateway.py`)**: A Flask application that acts as a reverse proxy.
* **Dummy Backend Servers (`app.py`)**: Flask applications simulating backend services.

## Running the Load Test

### Prerequisites

* Python 3.x
* pip (Python package installer)

### Installation

1.  **Install Dependencies:**

    ```bash
    pip install -r requirement.txt
    ```

### Setup

1.  **Start the Flask Dummy Backends:**

    Open three terminal windows. In each, run the following, changing the `PORT`:

    **Terminal 1:**

    ```bash
    export PORT=5000
    python app.py
    ```

    **Terminal 2:**

    ```bash
    export PORT=5001
    python app.py
    ```

    **Terminal 3:**

    ```bash
    export PORT=5002
    python app.py
    ```

    This will start three instances of the Flask app on ports 5000, 5001, and 5002.

2.  **Start the API Gateway:**

    Open another terminal and run:

    ```bash
    python gateway.py
    ```

3.  **Start Locust:**

    Open another terminal and run:

    ```bash
    locust -f {locust-file-name}.py -u <number of users to spawn> -r <time interval (sec)>
    ```

    This will start Locust with 10 users and a spawn rate of 2 users per second. Open your browser to `http://localhost:8089` to access the Locust web interface.

### Running the Test

1.  **Run the Load Test:**

    In the Locust web interface, start the load test. Locust will send requests to your API gateway, which will then distribute them to the Flask backend instances.

### Monitoring

1.  **Check the Results:**

    * Locust will show you the RPS, response times, and other statistics.
    * The API gateway's console will show the requests being proxied and any errors.
    * You can use the `/api/stats/1m`, `/api/stats/5m`, and `/api/stats/1h` endpoints on the gateway (e.g., `http://localhost:8000/api/stats/1m`) to see the gateway's statistics.
    * You can use the `/api/servers` endpoints on the gateway (e.g., `http://localhost:8000/api/servers`) to see the registered servers.
