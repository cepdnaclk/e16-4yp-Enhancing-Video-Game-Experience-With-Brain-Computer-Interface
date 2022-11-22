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
from STFT import *

if __name__ == "__main__":

    for i in range(1,11):
        if i != 10:
            name = 'sub_0' + str(i) + '_ses_02_sub_0' + str(i) + '_ses_02'
        else:
            name = 'sub_10_ses_02_sub_10_ses_02'
        file = Access_file(file_name=name)
        tags = Event_tag()
        chop = Chop()
        transformer = Transformer()
        stft = STFT()

        file.nextHandler = tags
        tags.nextHandler = chop
        chop.nextHandler = transformer
        transformer.nextHandler = stft
        file.handle()
