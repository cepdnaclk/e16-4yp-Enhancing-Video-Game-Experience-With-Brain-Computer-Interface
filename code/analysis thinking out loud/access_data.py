import mne
from CoR import Handler
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')


# .git/annex/objects/26/kG/MD5E-s673838592--47da206a83bfb09136d2b1cd86c0a608.bdf
# data/ds003626/sub-01/ses-01/eeg/sub-01_ses-01_task-innerspeech_eeg.bdf

class Access_file(Handler):
    def __init__(self, file_name='sub-03_ses-02_task-innerspeech_eeg.bdf'):
        super().__init__()
        self.raw = mne.io.read_raw_bdf(file_name, preload=True)  # file load
        self.raw.info['bads']  # todo bad channel detector
        self.raw.drop_channels(['EXG1', 'EXG2', 'EXG3', 'EXG4', 'EXG5', 'EXG6', 'EXG7', 'EXG8'])  # drop extra

        # montage
        # assign the board
        montage = mne.channels.make_standard_montage("biosemi128")
        self.raw.set_montage(montage, match_case=False)

    def handle(self):
        if self.nextHandler is None:  # no next element
            return self.raw
        else:  # next element
            super(Access_file, self).handle(self.raw)


if __name__ == "__main__":
    file = Access_file()
    raw = file.handle()
    raw.plot()
    #
    fig = raw.plot_sensors(show_names=True)
    fig = raw.plot_sensors('3d')
    plt.show()

# raw.plot()
# data, time = raw[:, :10]
# print(type(data))
# fft = mne.time_frequency.stft(raw[:,:],wsize=100)
# print(time)
