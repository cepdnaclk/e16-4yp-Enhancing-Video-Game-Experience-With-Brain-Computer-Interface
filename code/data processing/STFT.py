from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


def stft(x, fs):
    f, t, Zxx = signal.stft(x, fs, nperseg=256)
    plt.pcolormesh(t, f, np.abs(Zxx),vmax=1000 ,shading='gouraud')
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()



if __name__ == "__main__":

    f = open("../data acquisition gui/data/22_07_2022 11_07_04.csv", "r").read()  # 12_07_2022 02_00_03 #
    print(len(f))
    x = f.split('\n')
    #print(x[1])

    data = []
    for y in range(len(x)):
        tem = x[y][3 : -1: ]
        tem2 = tem.split(',')
        #print(tem2)
        T3 = list(map(int,tem2))
        data.append(T3[2])


    # time stript
    # shifting
    for y in data:
        temp = data

    stft(data,250)

