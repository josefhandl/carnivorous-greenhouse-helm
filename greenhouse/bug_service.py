# bug_service.py

import os
from flask import Flask, request, jsonify
import random
import requests
import threading
import time
import logging

logging.basicConfig(
    format='ts=%(asctime)s,%(msecs)03d level=%(levelname)s line=%(lineno)d msg="%(message)s"',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bugsarebad1234'

USER_SERVICE_URL       = os.environ.get("USER_SERVICE_URL",       'http://user_service:5001')
PLANT_SERVICE_URL      = os.environ.get("PLANT_SERVICE_URL",      'http://plant_service:5002')
SIMULATION_SERVICE_URL = os.environ.get("SIMULATION_SERVICE_URL", 'http://simulation_service:5003')
WEBSOCKET_SERVICE_URL  = os.environ.get("WEBSOCKET_SERVICE_URL",  'http://websocket_service:5004')

SERVICES = [
    USER_SERVICE_URL,
    PLANT_SERVICE_URL,
    SIMULATION_SERVICE_URL,
    WEBSOCKET_SERVICE_URL
]

bug_mode = False

def bug_mode_worker():
    while True:
        if bug_mode:
            service_url = random.choice(SERVICES)
            try:
                response = requests.get(f'{service_url}/trigger_bug')
                if response.status_code == 200:
                    logging.info(f"Bug triggered in {service_url}")
                else:
                    logging.error(f"Failed to trigger bug in {service_url}")
            except Exception as e:
                logging.error(f"Error triggering bug in {service_url}: {str(e)}")
        time.sleep(10)  # Trigger a bug every 10 seconds

@app.route('/toggle_bug_mode', methods=['POST'])
def toggle_bug_mode():
    global bug_mode
    bug_mode = not bug_mode
    logging.info(f"Bug mode toggled: {bug_mode}")
    return jsonify({"message": "Bug mode toggled", "bug_mode": bug_mode}), 200


@app.route('/bug_mode_status', methods=['GET'])
def bug_mode_status():
    return jsonify({"bug_mode": bug_mode}), 200

if __name__ == '__main__':
    threading.Thread(target=bug_mode_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=5010)
