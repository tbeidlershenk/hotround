import logging
import os
from flask import Flask, jsonify
from pyngrok import ngrok
from pyngrok import conf

uptime_app = Flask(__name__)

@uptime_app.route('/')
def home():
    return jsonify(message="Online", status=200)

def configure_logging():
    uptime_app.logger.setLevel(logging.CRITICAL+1)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL+1)

def run_server():
    ngrok_config = os.getenv("ngrok_config")
    if ngrok_config is None:
        return
    configure_logging()
    port = int(os.getenv("flask_port"))
    conf.get_default().config_path = ngrok_config
    ngrok.connect(addr=port, name="caddiebot")
    uptime_app.run(port=port)
