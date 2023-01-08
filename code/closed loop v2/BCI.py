from pyOpenBCI_v1 import OpenBCICyton
import os, sys, time
import paho.mqtt.client as mqtt
from datetime import datetime
import json

client = mqtt.Client()
client.connect("localhost", 1883, 60)


def print_raw(sample):
    # np array
    now = datetime.now()
    current_time = str(now.strftime("%M%S%f"))
    tem = {'time': current_time, 'data': sample.channels_data}
    jsonStr = json.dumps(tem)
    client.publish("BCI", jsonStr)

    # client.publish("BCI/time", time)
    # client.publish("BCI/channel0", sample.channels_data[0])
    # client.publish("BCI/channel1", sample.channels_data[1])
    # client.publish("BCI/channel2", sample.channels_data[2])
    # client.publish("BCI/channel3", sample.channels_data[3])
    # client.publish("BCI/channel4", sample.channels_data[4])
    # client.publish("BCI/channel5", sample.channels_data[5])
    # client.publish("BCI/channel6", sample.channels_data[6])
    # client.publish("BCI/channel7", sample.channels_data[0])


board = OpenBCICyton()
board.write_command('x1040010X')
board.write_command('x2040010X')
board.write_command('x3040010X')
board.write_command('x4040010X')
board.write_command('x5040010X')
board.write_command('x6040010X')
board.write_command('x7040010X')
board.write_command('x8040010X')

board.start_stream(print_raw)


# os.close(fd)
# os.close(std_out)
