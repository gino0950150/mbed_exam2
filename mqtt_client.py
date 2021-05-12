import paho.mqtt.client as paho
import time
import serial
import matplotlib.pyplot as plt
import numpy as np

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
# TODO: revise host to your IP
host = "192.168.43.214"
topic = "Mbed"
angle = 0
count = 0

serdev = '/dev/ttyACM1'                # use the device name you get from `ls /dev/ttyACM*`
s = serial.Serial(serdev, 9600)

Gesture_s = []
arr = []


# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))
    global count
    count = 0


def on_message(mosq, obj, msg):
    global count
    global arr
    global Gesture_s
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    temp = msg.payload.decode("utf-8")
    Gesture_s.append(int(str(temp[0])))
    count += 1
    if(msg.topic == topic):
        temp = msg.payload.decode("utf-8")
        Gesture_s.append(int(temp[0]))
    if(msg.topic == "features"):
        temp = msg.payload.decode("utf-8")
        arr = temp.split(' ')
        arr = arr[0:9]
        for i in arr:
            i = int(i)
        print("arr:", arr)
        Gesture_s = Gesture_s[0:9]
        draw()
    if(count >= 10) :
        s.write(bytes("/GestureUI_STOP/run/\r", 'UTF-8'))
        s.write(bytes("/Return_features/run/\r", 'UTF-8'))
        count = 0
        print("Ges:", Gesture_s)
    #     temp = msg.payload.decode("utf-8")
    #     angle = int(str(temp[0:1]))
    #     time.sleep(1.5)
    #     ret = mqttc.publish(topic, "GestureUI_STOP", qos=0)
    #     print("get angle" + str(s))
    #     if (ret[0] != 0):
    #         print("Publish failed")
    #     s.write(bytes("/Tilt_Angle_Detection_START/run/\r", 'UTF-8'))
    # elif(msg.topic == "over"):
    #     count += 1
    #     print(count)
    #     if(count >= 10):
    #         ret = mqttc.publish(topic, "Tilt_Angle_Detection_STOP", qos=0)
    #         print("Publish Tilt_Angle_Detection_STOP")
    #         if (ret[0] != 0):
    #             print("Publish failed")
    #         count = 0

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

def draw():
    t = np.arange(9)
    fig, ax = plt.subplots(2, 1)
    ax[0].plot(t,Gesture_s)
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Gesture')
    ax[1].plot(t,arr)
    ax[1].set_xlabel('Time')
    ax[1].set_ylabel('Features')
    plt.show()

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)
mqttc.subscribe("confirm_angle", 0)
mqttc.subscribe("features", 0)

s.write(bytes("/GestureUI_START/run/\r", 'UTF-8'))
count = 0
# Publish messages from Python
# num = 0
# while True:
#     # ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
#     # if (ret[0] != 0):
#     #         print("Publish failed")
#     mqttc.loop()
#     # time.sleep(1.5)
    # num += 1
# mqttc.publish(topic, "GestureUI_STOP", qos=0)
# Loop forever, receiving messages
mqttc.loop_forever()