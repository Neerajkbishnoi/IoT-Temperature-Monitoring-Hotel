import paho.mqtt.client as mqtt
import time
import random
import json

# MQTT BROKER settings(configurations)
BROKER_ADDRESS = "broker.hivemq.com" #you may add the ip address of your preferred MQTT Broker
BROKER_PORT = 1883
TOPIC = "hotel/temperature"

# Simulating temperature 
class TemperatureSensor:
    def __init__(self, min_temp=18, max_temp=30):
        self.min_temp = min_temp
        self.max_temp = max_temp

    def read_temperature(self):
        return round(random.uniform(self.min_temp, self.max_temp), 2)

# client setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

client.on_connect = on_connect


client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# temperature sensor
sensor = TemperatureSensor()

# Main loop
try:
    while True:
        temperature = sensor.read_temperature()
        timestamp = int(time.time())
        
        payload = json.dumps({
            "temperature": temperature,
            "timestamp": timestamp
        })
        
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        
        time.sleep(60)  # each reading at interval of 60 seconds

except KeyboardInterrupt:
    print("Publisher stopped")
    client.disconnect()