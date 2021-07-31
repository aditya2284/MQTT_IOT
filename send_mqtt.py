import paho.mqtt.client as mqtt
import time
from datetime import datetime
import os
import glob

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
    
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


connected = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        connected = True
        print("Connected")
    else:
        print("Not Able To Connect")

broker_address = "192.168.1.10"


client = mqtt.Client("P1") 
client.on_connect = on_connect

client.connect(broker_address,port=1883)
time.sleep(0.4)
client.loop_start()
while True:
    now=datetime.now()
    temperature=read_temp()
    client.publish("time", str(now)+","+str(temperature))
    print("Publishing... " + str(now)+","+str(temperature))
    time.sleep(4)
    
client.loop_stop()