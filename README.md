The repository contains three code files:

1. Publisher Program: This publisher program simulates a temperature sensor and publishes temperature readings to an MQTT broker every 60 seconds.
2. Subscriber Program: This subscriber program listens for temperature data, saves it locally, and raises an alarm if the temperature threshold is crossed for 5 consecutive readings over 5 minutes.
3. Server Program: This server program uses Flask to create a simple API that returns the last temperature reading when a GET request is made to the /temperature endpoint.

Also, there is a requirements.txt file. You may install the required dependencies by running following command in the terminal: 

pip install -r requirements.txt

Run Publisher, Subscriber, Server program in different terminals respectively.

Note that you'll need to replace "broker.hivemq.com" with the address of your actual MQTT broker in both the publisher and subscriber programs. Here, the MQTT brker used is HiveMQ.

