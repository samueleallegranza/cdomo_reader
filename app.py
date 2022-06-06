from lib.RelayBoard import RL_Board
import time
from datetime import datetime
import paho.mqtt.client as mqtt
import json 
import random

# [MQTT Functions]

def on_pub(client,userdata,result):
    print("Published.")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")


# # [Load config files]
# with open("config/mqtt.json") as _MQTT_CFG_FILE:
#     MQTT_CFG = json.loads(_MQTT_CFG_FILE)
# print(MQTT_CFG)

try:
    board = RL_Board("/dev/ttyUSB0", 115200)
    board.open()
except Exception as e:
    print("Error - Connection to the board: {}".format(e))
    exit()

client_id = "rpi-{}".format(random.randint(0, 1000))
mqtt_client = mqtt.Client(client_id)

mqtt_client.username_pw_set("rpi", "raspberry")
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_pub

mqtt_client.connect("78.47.121.248", port=1883)

screenshot = None

mqtt_client.loop_start()
while True:
    (resp, err) = board.read_inputs()

    if(err >= 0):
        # Check if at least one input has changed value
        if(screenshot):
            equal = True
            for inp, screen in zip(resp, screenshot):
                equal = (inp["counter"]==0) and (inp["status"]==screen["status"])
                if(not equal): break;
        else:
            equal = False

        screenshot = resp

        time_now = datetime.now().time()
        time_epoch = int(time.time())

        # Send updated status via MQTT if any change occurred
        if(not equal):
            message = {
                "time": time_epoch,
                "payload": resp
            }
            mqtt_client.publish(topic="test", payload=json.dumps(message), qos=0)
            print("{} [{}]".format(time_now, time_epoch))
            print(json.dumps(message, indent=4, sort_keys=True))


    else:
        print("{} [{}] [!] Error while reading inputs".format(time_now, time_epoch))

    # Wait N seconds before checking again
    time.sleep(1)