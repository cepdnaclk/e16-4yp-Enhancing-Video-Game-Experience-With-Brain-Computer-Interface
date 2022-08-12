import mne
from CoR import Handler
import matplotlib
import matplotlib.pyplot as plt
from access_data import Access_file

matplotlib.use('Qt5Agg')


class Event_tag(Handler):
    def __init__(self):
        super().__init__()
        self.file_name = ''
        self.epochs = ''

    def handle(self, request):
        # load the event fill
        # file = 'sub-03_ses-02'
        name = request[1] + '_eeg-epo.fif'
        self.epochs = mne.read_epochs(name, verbose='WARNING')

        # loop through epochs
        out = [request, self.epochs]

        if self.nextHandler is None:  # no next element
            return out
            # print(request)
            # request.plot()
            # plt.show()
        else:  # next element
            super(Event_tag, self).handle(out)


if __name__ == "__main__":
    file = Access_file(file_name='sub-03_ses-02')
    tags = Event_tag()

    file.nextHandler = tags
    data = file.handle()

    epochs = tags.epochs
    print(epochs['Arriba'].get_data().shape)
