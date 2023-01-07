import numpy as np
from scipy import signal
import paho.mqtt.client as mqtt
import json
from json import JSONEncoder


class Transformer:

    def __init__(self):
        self.array = [0]
        self.topic = 'BCI'
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.loop_forever()

    class NumpyArrayEncoder(JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return JSONEncoder.default(self, obj)

    # [{"time": "1455312406", "data": [-2028017, 476640, 1684184, 2621645, 1174151, -180759, 3828692, -10715]}]
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        # print(msg.topic + " " + str(msg.payload))
        # json file read
        # get channel one data
        #
        raw = json.loads(msg.payload)
        # print(type(raw),raw)
        channel = raw['data']
        self.array.append(channel[0])
        if len(self.array) > 700:  # TODO consider window
            out = np.abs(signal.stft(self.array, 250, nperseg=256)[2])
            payload = json.dumps(out, cls=Transformer.NumpyArrayEncoder)
            del self.array[0:]  # TODO every 50 sample
            client.publish("model/predict/request", payload)


STFT = Transformer()

# array.append(x)
# tem = array
# out = np.abs(signal.stft(tem, 250, nperseg=256)[2])
