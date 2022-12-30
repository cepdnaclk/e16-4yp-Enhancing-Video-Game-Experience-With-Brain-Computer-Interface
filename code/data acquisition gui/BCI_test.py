
from pyOpenBCI_v1 import OpenBCICyton
import time

import serial
from serial import Serial

def my_write_command(board, command):
    """Sends string command to the Cyton board"""
    if command == '?':
        board.ser.write(command.encode())
        if board.ser.inWaiting():
            line = ''
            while '$$$' not in line:
                line += board.ser.read().decode('utf-8', errors='replace')
            print(line)
    else:
        board.ser.write(command.encode())
        if board.ser.inWaiting():
            line = ''
            while '$$$' not in line:
                line += board.ser.read().decode('utf-8', errors='replace')
            print(line)
        time.sleep(0.5)

def print_raw(sample):
    print(sample.channels_data)

def test(serial ,command):
    
    s.write(command)
    line = ''
    time.sleep(2)
    if s.inWaiting():
        line = ''
        c = ''
        while '$$$' not in line:
            c = s.read().decode('utf-8', errors='replace')
            line += c
        print(line)
        if 'OpenBCI' in line:
            print('work')


board = OpenBCICyton()
#s = Serial(port='COM3', baudrate=115200, timeout=None)
#test(serial = s, command = b'v')
#test(serial = s, command = b'x1020000X')
#test(serial = s, command = b'x2020000X')
#test(serial = s, command = b'b')
board.write_command('x1020000X')
board.write_command('x2020000X')
board.write_command('x3020000X')
#board.start_stream(print_raw)

#time.sleep(1)
#print('write command',my_write_command(board,"?"))


#time.sleep(5)
#board.ser.write(b'v')
#if board.ser.inWaiting():
#    print("bv",board.ser.read().decode('utf-8', errors='replace'))

#print(board.ser.read().decode('utf-8', errors='replace'))
# print(board.parse_board_data())
#print('write command',board.write_command('OpenBCI V3 16 channel\nADS1299 Device ID: 0x3E\nLIS3DH Device ID: 0x33\n$$$') )

#time.sleep(1)
#print('write command',board.write_command('x1040010X'))