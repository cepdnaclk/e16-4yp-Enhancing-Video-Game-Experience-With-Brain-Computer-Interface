import os
from CoR import Handler
import mne
from access_data import Access_file
from event_tag import Event_tag
from chop import Chop
import numpy

ROOT_DIR = "."

# change according to the applying transformer
PLOT_TYPE = "STFT"

class Transformer(Handler):
    def __init__(self):
        super().__init__()
        self.up = ''
        self.down = ''
        self.right = ''
        self.left = ''
        self.relax_interval = ''
        self.file_name = ''

    def pushing(self, value: numpy.ndarray, task:str):
        # get shape 50, 128, 641
        value_shape = value.shape

        images_path = os.path.join(ROOT_DIR, PLOT_TYPE, task)
        os.makedirs(images_path, exist_ok = True)

        # loop through epochs
        for epochs in range(value_shape[0]):  # 50
            for channel in range(value_shape[1]):  # 128
                name = PLOT_TYPE+'_'+self.file_name + '_epoch-' + str(epochs) + '_channel-' + str(channel)

                # path to save the plots
                path = os.path.join(images_path, name + "." + "png")
                out = [path, value[epochs][channel]]
                super(Transformer, self).handle(out)              

    def handle(self, request: [numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray,
                               numpy.ndarray, str]):
        # received data
        self.up = request[0]
        self.down = request[1]
        self.right = request[2]
        self.left = request[3]
        self.relax_interval = request[4]
        self.file_name = request[5]

        # push into convertor
        # up
        self.pushing(self.up,"Up")

        # down
        self.pushing(self.down, "Down")

        # left
        self.pushing(self.left, "Left")

        # right
        self.pushing(self.right, "Right")

        # relax period
        self.pushing(self.relax_interval, "Relax")


if __name__ == "__main__":
    file = Access_file(file_name='sub-03_ses-02')
    tags = Event_tag()
    chop = Chop()
    transformer = Transformer()

    file.nextHandler = tags
    tags.nextHandler = chop
    chop.nextHandler = transformer
    file.handle()
