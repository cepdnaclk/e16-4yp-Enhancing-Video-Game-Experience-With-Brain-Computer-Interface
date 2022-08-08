import mne

#.git/annex/objects/26/kG/MD5E-s673838592--47da206a83bfb09136d2b1cd86c0a608.bdf
# data/ds003626/sub-01/ses-01/eeg/sub-01_ses-01_task-innerspeech_eeg.bdf

raw = mne.io.read_raw_bdf('sub-01_ses-01_task-innerspeech_eeg.bdf', preload=True)

raw.plot()

print('Keys in info dictionary:\n', raw.keys())
#ica = mne.preprocessing.ICA(n_components=4, random_state=0)

#ica.fit(raw.copy().filter(8,35))

#ica.plot_components(outlines="skirt")
print(type(raw))
#fft = mne.time_frequency.stft(raw['A1'],wsize=20)
