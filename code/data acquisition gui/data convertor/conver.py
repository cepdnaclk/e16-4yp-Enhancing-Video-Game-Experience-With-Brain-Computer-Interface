import mne
from pyedflib import highlevel
import os
import pyedflib
import numpy as np
import matplotlib.pyplot as plt


class Conver:
    # .bdf convertor

    def __init__(self, file_name, CSV_name) -> None:
        # board parameters
        self.sample_rate = 250
        self.channel_name = ['C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'T3', 'T4']

        # file_name = save file name

        self.file_name = '../data/bdf/' + file_name + '.edf'
        test_data_file = os.path.join('.', self.file_name)
        self.file = pyedflib.EdfWriter(test_data_file, 8,
                                       file_type=pyedflib.FILETYPE_EDFPLUS)

        # load csv and conver into .bdf
        self.CSV_name = '../data/csv/' + CSV_name

        self.channel_info = []
        self.data_list = []

    def CSV(self, ):

        file_csv = open(self.CSV_name, "r").read()

        x = file_csv.split('\n')
        # file duration
        # todo
        # try actual time size
        self.file_duration = len(x)
        time = np.linspace(0, self.file_duration)

        data = []
        for y in range(len(x)):
            tem = x[y][3: -1:]
            tem2 = tem.split(',')

            tem3 = np.array(list(map(int, tem2)))/10000000
            data.append(tem3)

        data = np.array(data)

        for ch in range(8):
            ch_dict = {'label': self.channel_name[ch], 'dimension': 'uV', 'sample_frequency': self.sample_rate,
                       'transducer': 'openBCI',
                       'prefilter': ''}
            self.channel_info.append(ch_dict)
            # print((data[1,:]))
            # print((data[:,1]))
            # print((data[:, ch]))
            channel_raw = np.array(data[:, ch])
            print(channel_raw)
            self.data_list.append(channel_raw)
            # time = np.linspace(0, self.file_duration)
            # print(self.file_duration)
            # self.data_list.append(np.sin(2*np.pi*time/250))

        print(self.data_list)

        self.file.setSignalHeaders(self.channel_info)
        self.file.writeSamples(self.data_list)
        self.file.writeAnnotation(0, -1, "Recording starts")
        self.file.writeAnnotation(298, -1, "Test 1")
        self.file.writeAnnotation(294.99, -1, "pulse 1")
        self.file.writeAnnotation(295.9921875, -1, "pulse 2")
        self.file.writeAnnotation(296.99078341013825, -1, "pulse 3")
        self.file.writeAnnotation(600, -1, "Recording ends")
        self.file.close()


if __name__ == "__main__":
    testing = Conver(file_name="test", CSV_name="22_07_2022 12_12_28.csv")
    testing.CSV()
