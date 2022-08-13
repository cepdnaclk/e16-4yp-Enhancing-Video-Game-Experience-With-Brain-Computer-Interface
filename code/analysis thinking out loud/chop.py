import mne
from CoR import Handler
import matplotlib
import matplotlib.pyplot as plt
from access_data import Access_file
from event_tag import Event_tag

matplotlib.use('Qt5Agg')


class Chop(Handler):
    def __init__(self):
        super().__init__()
        self.epochs = ''
        self.action_interval = ''
        self.up = ''
        self.down = ''
        self.right = ''
        self.left = ''
        self.relax_interval = ''
        self.relax_interval: mne.epochs.EpochsFIF

        self.out = ''

    def handle(self, request: [mne.io.edf.edf.RawEDF, mne.epochs.EpochsFIF, str]):
        self.epochs = request[1]
        # “Arriba”    = “up”
        # “Abajo”     = “down”
        # “Derecha”   = “right”
        # “Izquierda” = “lef”

        # action interval 0.5s to 3s
        self.action_interval = self.epochs.copy()
        self.action_interval = self.action_interval.crop(tmin=0.5, tmax=3)

        # relax interval
        # todo relax interval is 1 sec
        self.relax_interval = self.epochs.copy()
        self.relax_interval = self.relax_interval.crop(tmin=3, tmax=4)

        # direction
        self.up = self.action_interval['Arriba'].get_data()
        self.down = self.action_interval['Abajo'].get_data()
        self.right = self.action_interval['Derecha'].get_data()
        self.left = self.action_interval['Izquierda'].get_data()

        self.out = [self.up, self.down, self.right, self.left, self.relax_interval, request[2]]

        if self.nextHandler is None:
            return self.out

        else:
            super(Chop, self).handle(self.out)


if __name__ == "__main__":
    file = Access_file(file_name='sub-03_ses-02')
    tags = Event_tag()
    chop = Chop()

    file.nextHandler = tags
    tags.nextHandler = chop
    file.handle()

    print(chop.relax_interval.get_data().shape)
