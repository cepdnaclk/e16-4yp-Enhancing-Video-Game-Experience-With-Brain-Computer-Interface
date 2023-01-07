import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.layers import Dense, Conv2D, Flatten, MaxPool2D
from tensorflow.keras.models import Sequential
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

model = tf.keras.models.load_model('external_model')


# TODO
# stochastic gradient descent -> batch gradient descent
def retrain(x, y):
    # model.fit(x, y, batch_size=32, epochs=1)
    # print("retrain", str(message.payload))
    model.fit(x, y)


def prediction(x):
    # print("prediction", str(x))
    return model.predict(x)


def on_connect(client, userdata, flags, rc):
    # print("Connected with result code " + str(rc))
    client.subscribe(topic)


def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))
    # json file read
    # get channel one data
    if msg.topic == 'model/predict/request':
        prediction(msg.payload)

    elif msg.topic == 'model/retrain':
        retrain(msg.payload)


topic = 'model/#'
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
