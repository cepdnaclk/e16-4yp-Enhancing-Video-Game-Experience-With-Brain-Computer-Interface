from pyOpenBCI import OpenBCICyton
import random
import time
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'
count = 0

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def print_raw(sample):
  
    print(sample.channels_data)
    
    data = sample.channels_data
    
    msg  = ','.join(map(str,data))
    
    
    
    global count
    count = count + 1
    
    msg = "Number:"+str(count)+": " + msg
    
    
    
    result = client.publish(topic, msg)
        # result: [0, 1]
    status = result[0]
    if status == 0:
      print(f"Number `{count}`Send `{msg}` to topic `{topic}`")
    else:
      print(f"Failed to send message to topic {topic}")
       
    
   
if __name__ == '__main__':
  
  client = connect_mqtt()
  client.loop_start()
  
  board = OpenBCICyton(port='COM6', daisy=False)

  board.start_stream(print_raw)
  