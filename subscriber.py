import paho.mqtt.client as mqtt
import json
import time
from collections import deque

# MQTT broker settings
BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC = "hotel/temperature"

# Threshold settings-(Temperature - in celsius, Duration- 5 data points each in 1 minute, total duration 5 minutes)
TEMPERATURE_THRESHOLD = 18  
DURATION_THRESHOLD = 5  

# Data storage
temperature_data = []
recent_temperatures = deque(maxlen=DURATION_THRESHOLD)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    temperature = payload['temperature']
    timestamp = payload['timestamp']
    
    # Save data locally
    temperature_data.append(payload)
    
    # Check for threshold 
    recent_temperatures.append(temperature)
    if len(recent_temperatures) == DURATION_THRESHOLD and all(t > TEMPERATURE_THRESHOLD for t in recent_temperatures):
        raise_alarm(temperature)
    
    print(f"Received: Temperature: {temperature}°C, Timestamp: {timestamp}")

def raise_alarm(temperature):
    print(f"ALARM: Temperature has been above {TEMPERATURE_THRESHOLD}°C for {DURATION_THRESHOLD} consecutive readings!")
    print(f"Current temperature: {temperature}°C")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# Start the loop
client.loop_forever()
