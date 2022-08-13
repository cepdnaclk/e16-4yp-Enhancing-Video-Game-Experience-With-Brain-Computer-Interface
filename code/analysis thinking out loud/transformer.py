from CoR import Handler
import mne
from access_data import Access_file
from event_tag import Event_tag
from chop import Chop
import numpy


class Transformer(Handler):
    def __init__(self):
        super().__init__()
        self.up = ''
        self.down = ''
        self.right = ''
        self.left = ''
        self.relax_interval = ''
        self.file_name = ''

    def pushing(self, value: numpy.ndarray):
        # get shape 50, 128, 641
        value_shape = value.shape

        # loop through epochs
        for epochs in range(value_shape[0]):  # 50
            for electrode in range(value_shape[1]):  # 128
                # todo electrode name should be channel name
                name = self.file_name + '/' + str(epochs) + '/' + str(electrode)
                out = [name, value[epochs][electrode]]
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
        self.pushing(self.up)

        # down
        self.pushing(self.down)

        # left
        self.pushing(self.left)

        # right
        self.pushing(self.right)


if __name__ == "__main__":
    file = Access_file(file_name='sub-03_ses-02')
    tags = Event_tag()
    chop = Chop()
    transformer = Transformer()

    file.nextHandler = tags
    tags.nextHandler = chop
    chop.nextHandler = transformer
    file.handle()
