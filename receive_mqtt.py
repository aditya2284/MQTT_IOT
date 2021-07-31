import paho.mqtt.client as mqtt
import time
import grpc
import Temperature_pb2
import Temperature_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

message = ""

#step1:create a channel
channel=grpc.insecure_channel('192.168.1.13:30051')

#Step2: create a stub
stub=Temperature_pb2_grpc.TemperatureSensingStub(channel)

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))
    temporary=message.split(',')
    date_time_str=temporary[0]
    #2021-07-23 21:48:33.284263
    date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")

    timestamp = Timestamp()
    timestamp.FromDatetime(date_time_obj)
    tosend=Temperature_pb2.TemperatureData(device_ID="1",date_time=timestamp,temperature=float(temporary[1]),unit="degree C")
    response=stub.AddTemperatureData(tosend)
    print("message received ", message)
    #print("message topic=", message.topic)
    message_received = True
    
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        global connected
        connected = True
        print("Connected")
        print("..........")
    else:
        print("Unable To Connect")
        
connected = False
message_received = False
broker_address = "192.168.1.10"

print("creating new instance")
client = mqtt.Client("MQTT")

client.on_message = on_message
client.on_connect = on_connect

print("connecting to broker")
client.connect(broker_address,port=1883)

client.loop_start()

print("Subscribing to topic", "time")
client.subscribe("time")

while connected != True or message_received != True:
    time.sleep(0.2)

client.loop_forever()