import paho.mqtt.client as mqtt
import json
import time
from collections import deque

# MQTT broker settings(configurations)
BROKER_ADDRESS = "broker.hivemq.com" #you may add the ip address of your preferred MQTT Broker
BROKER_PORT = 1883
TOPIC = "hotel/temperature"

# Threshold configurations (celsius, time- 5 minutes in seconds)
TEMPERATURE_THRESHOLD = 28  
TIME_THRESHOLD = 5 * 60  

# Data storage-store last 5 readings
temperature_data = []
recent_readings = deque(maxlen=5)  

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    temperature = payload["temperature"]
    timestamp = payload["timestamp"]
    
    # data saved locally
    temperature_data.append(payload)
    
    # recent readings added
    recent_readings.append((temperature, timestamp))
    
    # Checking if crossed 5 consecutive readings
    if len(recent_readings) == 5:
        if all(temp >= TEMPERATURE_THRESHOLD for temp, _ in recent_readings):
            if recent_readings[-1][1] - recent_readings[0][1] >= TIME_THRESHOLD:
                print("ALARM: Temperature threshold crossed for 5 minutes!")

    print(f"Received: Temperature: {temperature}°C, Timestamp: {timestamp}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Subscriber stopped")
    client.disconnect()
