import logging
import os
import random

from flask import Flask
from flask_mqtt import Mqtt


# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'  # MQTT Broker URL
app.config['MQTT_BROKER_PORT'] = 1883  # MQTT Broker Port
app.config['MQTT_USERNAME'] = 'emqx'  # MQTT Username
app.config['MQTT_PASSWORD'] = 'public'  # MQTT Password
app.config['MQTT_TOPIC'] = 'emqx/flask'  # MQTT Topic
app.config['MQTT_KEEPALIVE'] = 60  # MQTT KeepAlive Interval
app.config['MQTT_RECONNECT_DELAY'] = 3  # MQTT Reconnect Interval
app.config['MQTT_CLIENT_ID'] = f'flask-mqtt-{random.randint(1000, 9999)}'

mqtt = Mqtt()


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc: int) -> None:
    logging.info(f'Connected with result code {rc}')
    topic = app.config['MQTT_TOPIC']
    mqtt.subscribe(topic)  # Replace with your MQTT topic


@mqtt.on_message()
def handle_message(client, userdata, message) -> None:
    logging.info(f'Received message: {message.payload.decode()} on topic {message.topic}')
    # Here you can add logic to handle the message


@app.route('/')
def index():
    topic = app.config['MQTT_TOPIC']
    mqtt.publish(topic, b'Hello from Flask via MQTT over TCP')
    return 'Flask MQTT Client is running'


if __name__ == '__main__':
    debug = True
    if debug and os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        # In debug mode, prevent multiple threads from starting the MQTT client
        mqtt.init_app(app)
    app.run(debug=debug)
