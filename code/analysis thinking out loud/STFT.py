import sys
import matplotlib.pyplot as plt
from CoR import Handler
from scipy import signal
import mne
from access_data import Access_file
from event_tag import Event_tag
from chop import Chop
from transformer import Transformer
import numpy as np


def encoder():
    pass


def convertor(x: np.ndarray, fs: float, path: str):
    # create 2d matrix
    Z = np.abs(signal.stft(x, fs, nperseg=50)[2]) # 50

    # plt.imshow(Z,aspect='auto')
    # plt.show()
    # print(type(Z))
    # save file
    np.save(path,Z)

    # y = np.load(path+'.npy')
    # plt.imshow(y, aspect='auto')
    # plt.show()
    # print(type(y))
    # print(y)
    # print(value)
    # plt.pcolormesh(t, f, np.abs(zxx), shading='gouraud')
    # plt.title('STFT')
    # plt.ylabel('Frequency [Hz]')
    # plt.xlabel('Time [sec]')
    # print(f, t, zxx)
    print("Saving figure", path)
    # plt.savefig(path, format="png")
    # sys.exit()

class STFT(Handler):
    def __init__(self):
        super().__init__()

    def handle(self, request: [str, np.ndarray]):
        # frequency
        convertor(request[1], 256, request[0])

        if self.nextHandler is None:
            return


if __name__ == "__main__":
    file = Access_file(file_name='sub_01_ses_02_sub_01_ses_02')
    tags = Event_tag()
    chop = Chop()
    transformer = Transformer()
    stft = STFT()

    file.nextHandler = tags
    tags.nextHandler = chop
    chop.nextHandler = transformer
    transformer.nextHandler = stft
    file.handle()
