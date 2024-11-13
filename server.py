import logging
import os
from flask import Flask, jsonify
from pyngrok import ngrok
from pyngrok import conf
import dotenv

uptime_app = Flask(__name__)

@uptime_app.route('/')
def home():
    return jsonify(message="Online", status=200)

def configure_logging():
    uptime_app.logger.setLevel(logging.CRITICAL+1)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL+1)

def run_server():
    dotenv.load_dotenv()
    configure_logging()
    port = int(os.getenv("PORT"))
    conf.get_default().config_path = "ngrok_config.yml"
    ngrok.connect(addr=port, name="caddiebot")
    uptime_app.run(port=port)
