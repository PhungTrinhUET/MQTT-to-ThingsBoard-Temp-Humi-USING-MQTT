import paho.mqtt.client as mqtt
import json  

# THINGSBOARD SETUP-----------------------------------------------------------------------
THINGSBOARD_HOST = "localhost"  
THINGSBOARD_PORT = 1883  
ACCESS_TOKEN = "6OSgcOCEIWMT07HpD0Ri"  # Sensor Xuan Thuy


# DINH NGHIA HAM SU LY SU KIEN KHI KET NOI TOI MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    
    # SUBCRIBE MQTT
    client.subscribe("esp32/temperature")
    client.subscribe("esp32/humidity")

# DINH NGHIA HAM ON_MESSAGE
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    topic = msg.topic # LAY CHU DE TU DEVICE GUI TOI BROKER 

    if topic == "esp32/temperature":
        temperature = payload.get("temperature")
        if temperature is not None:
            send_to_thingsboard("temperature", temperature)
    
    elif topic == "esp32/humidity":
        humidity = payload.get("humidity")
        if humidity is not None:
            send_to_thingsboard("humidity", humidity)

def send_to_thingsboard(sensor_type, value):
    # Send data to ThingsBoard using MQTT
    thingsboard_topic = f"v1/devices/me/telemetry"
    data = {sensor_type: value}
    client.publish(thingsboard_topic, json.dumps(data), qos=1)
    print(f"Data sent to ThingsBoard via MQTT: {sensor_type} -{value}")

#Create and setup Client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, THINGSBOARD_PORT, 60)

# LISTEN AND DUY TRI KET NOI
client.loop_start()

# Giu chuong trinh chay vo han
while True:
    pass







