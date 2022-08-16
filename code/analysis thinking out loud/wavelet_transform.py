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


def convertor(x: np.ndarray, fs: float, name: str):
    widths = np.arange(1,20)
    cwtmatr = signal.cwt(x, signal.ricker, widths )

    plt.imshow(cwtmatr, cmap='PRGn', aspect='auto',
           vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())

    plt.title('CWT')
    plt.ylabel('Scale')
    plt.xlabel('Time [sec]')
    
    plt.show()

    # todo remove this ans add file save
    sys.exit()


class WT(Handler):
    def __init__(self):
        super().__init__()

    def handle(self, request: [str, np.ndarray]):
        # frequency
        convertor(request[1], 256, request[0])
        
        if self.nextHandler is None:
            return


if __name__ == "__main__":
    file = Access_file(file_name='sub-03_ses-02')
    tags = Event_tag()
    chop = Chop()
    transformer = Transformer()
    wt = WT()

    file.nextHandler = tags
    tags.nextHandler = chop
    chop.nextHandler = transformer
    transformer.nextHandler = wt
    file.handle()
