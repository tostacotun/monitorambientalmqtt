import os
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from datetime import datetime
from ast import literal_eval
#Variables
load_dotenv()
MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT"))
MQTT_BROKER_KEEPALIVE = int(os.getenv("MQTT_BROKER_KEEPALIVE"))
DATABASE_URL= os.getenv("DATABASE_URL")
DATABASE_USER= os.getenv("DATABASE_USER")
DATABASE_PASS= os.getenv("DATABASE_PASS")
DATABASE_AUTHSRC= os.getenv("DATABASE_AUTHSRC")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_COLLECTION = os.getenv("DATABASE_COLLECTION")
#MONGO
cliente = MongoClient(DATABASE_URL,
                      username=DATABASE_USER,
                      password=DATABASE_PASS,
                      authSource=DATABASE_AUTHSRC
                      )
base = cliente[DATABASE_DB]
colleccion = base[DATABASE_COLLECTION]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/cuartomax/#")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    lectura = literal_eval(msg.payload.decode())
    resultado = colleccion.insert_one(
        {
            "fecha": datetime.utcnow(),
            "temperatura": lectura["temperatura"],
            "humedad": lectura["humedad"],
            "origen":msg.topic

        }
    )
    if resultado.acknowledged:
        time.sleep(15 * 60)


def mqttcon():
    load_dotenv()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, MQTT_BROKER_KEEPALIVE)
    client.loop_forever()
