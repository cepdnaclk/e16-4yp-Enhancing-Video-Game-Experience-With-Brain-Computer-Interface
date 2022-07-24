from pyOpenBCI import OpenBCICyton
import os, sys

# error file
fd = os.open('error.txt',os.O_RDWR|os.O_CREAT)

# duplicate sdn ou
std_out = os.dup(sys.stdout.fileno())

# replace stdout
os.dup2(fd=fd, fd2=sys.stdout.fileno())


def print_raw(sample):
    # np array
    value = (str(sample.channels_data[0])+','+
            str(sample.channels_data[1])+','+
            str(sample.channels_data[2])+','+
            str(sample.channels_data[3])+','+
            str(sample.channels_data[4])+','+
            str(sample.channels_data[5])+','+
            str(sample.channels_data[6])+','+
            str(sample.channels_data[7])+','+
            str('\n'))

    os.write(std_out,str.encode(value))


board = OpenBCICyton(port='COM6', daisy=False)
board.start_stream(print_raw)

os.close(fd)
os.close(std_out)
