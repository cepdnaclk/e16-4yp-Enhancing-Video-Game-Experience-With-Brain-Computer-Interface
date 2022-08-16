import signal

from PyQt5.QtCore import *
import time
import threading
from pyOpenBCI import OpenBCICyton
from datetime import datetime

# create connection
board = OpenBCICyton(port='COM4', daisy=False)

# recoding termination signal
end_signal = threading.Event()

# state recoding
status_recoding = 0


def set_status(number):
    global status_recoding
    status_recoding = number


def end_record():
    end_signal.set()


def start_record():
    end_signal.clear()


class Save:

    def __init__(self):
        # create file recording
        # file name
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
        self.file_name = 'data/' +str(dt_string) + '.csv'

    def open(self):
        # open file
        self.file = open(self.file_name, "w")

    def write(self, raw):
        self.file.write(raw)

    def close(self):
        # file close
        self.file.close()


class Recording(QRunnable):

    def __init__(self):
        super(Recording, self).__init__()
        self.file = Save()

    def print_raw(self, sample):
        global status_recoding
        # raw data save
        raw = str(status_recoding)+',' + str(sample.channels_data) + '\n'
        self.file.write(raw)
        #print(raw)

        if end_signal.is_set():
            # terminated connection
            board.stop_stream()
            self.file.close()

    def run(self):
        self.file.open()

        # print data
        board.start_stream(self.print_raw)




def worker_Recored():
    threadpool = QThreadPool().globalInstance()

    worker = Recording()
    threadpool.start(worker)


if __name__ == "__main__":
    # worker_Recored()

    worker_Recored()
    start_record()

    while 1 :
        time.sleep(1)
