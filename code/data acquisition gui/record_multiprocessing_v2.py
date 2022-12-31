# importing libraries
from multiprocessing.connection import wait
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
import sys
import time
import random
import multiprocessing
from pyOpenBCI_v1 import OpenBCICyton


# cycle time
cycle_time = 7000
white_dot_1 = 0
direction = 500
white_dot_2 = 1000
blue_dot = 3500
rest_time = 4500


class Window(QMainWindow):

    def __init__(self, current_status ,  start_signal : multiprocessing.Event ):
        super().__init__()

        # shared 
        self.start_signal = start_signal
        self.current_status = current_status

        # GUI status 
        self.start_signal.clear()

        # setting title
        self.setWindowTitle("Trial Workflow")

        # setting geometry
        self.setGeometry(600, 100, 800, 800)
        self.setStyleSheet("background-color: gray;")

        # image index
        self.image_name = ['1', '2', 'black', 'down', 'left', 'right', 'up']
        self.image_index = 0

        self.Components()

        # showing all the widgets
        self.show()

    def run(self):
        
        # full time cycle 7seconds
        self.start_signal.set()
        self.button1.setText("STOP")
        self.timer_cycle = QtCore.QTimer()
        self.timer_cycle.timeout.connect(self.cycle)
        self.timer_cycle.start(7000)
        # start cycle zero
        self.cycle()

    
    def stop(self):
        self.current_status.number = -10
        self.current_status.status = -10
        self.current_status.time = -10
        self.button1.setText("START")
        self.timer_cycle.stop()
        self.reset_timer.stop()
        self.dirction_timer.stop()
        self.white_dot_timer.stop()
        self.blue_dot_timer.stop()
        self.start_signal.clear()

    def is_run(self):
        return self.start_signal.is_set() == True

    # method for widgets
    def Components(self):

        # start button
        self.button1 = QPushButton(self)
        self.button1.setText("START")
        self.button1.width = 100
        self.button1.height = 75
        self.button1.setGeometry(250, 675, 300, 75)
        self.button1.clicked.connect(self.button1_clicked)
        self.button1.setStyleSheet("border : 1px solid black;background-color: white;border-radius: 10px;")
        self.button1.setFont(QFont('Arial', 20))

        # image box
        self.image1 = QLabel(self)


    def show_image(self, number, status):
      now = datetime.now()
      timestamp = now.strftime("%M%S%f")
      #TODO
      # set_status(number, str(timestamp))
      self.current_status.number = number
      self.current_status.status = status
      self.current_status.time = str(timestamp)
      #global status_recoding
      # status_recoding = number
      self.pixmap = QPixmap('images/' + self.image_name[status] + '.jpg')
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)

    def cycle(self):

        # 0 = white dot
        # 1 = show direction
        # 2 = black screen
        # 3 - 6 = direction (down, left, right, up)

        # name              number      status
        # const                 0           0   whie dot
        # cue                   1           x   show dire 
        # action                x           0   white dot (down, left, right, up)
        # relax                 2           1   blue dot
        # rest                 -1           2   black

        
        # white dot time  = 0 base
        self.show_image(0,0)

        # random direction time = 0.5s
        x = random.randint(3,6)
        self.dirction_timer = QtCore.QTimer()
        self.dirction_timer.singleShot(direction, lambda: self.show_image(1,x))

        # 2nd white dot time = 1s
        self.white_dot_timer = QtCore.QTimer()
        self.white_dot_timer.singleShot(white_dot_2, lambda: self.show_image(x,0))

        # blue dot time = 3.5 second
        self.blue_dot_timer = QtCore.QTimer()
        self.blue_dot_timer.singleShot(blue_dot, lambda: self.show_image(2,1) )

        # black reset time = 4.5s
        self.reset_timer = QtCore.QTimer()
        self.reset_timer.singleShot(rest_time, lambda: self.show_image(-1,2))
       

    # stop button
    def button1_clicked(self):
        #
        # end_record()
        if self.is_run():
            self.stop()
        else:
            self.run()

  
def GUI_Data_Acquisition(GUI_current_status ,  start_signal : multiprocessing.Event ):
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = Window(GUI_current_status ,  start_signal)
    # start the app
    sys.exit(App.exec())


class Recording():

    def __init__(self, FIFO: multiprocessing.Queue, start_signal : multiprocessing.Event, terminate_signal:  multiprocessing.Event ):
        # create connection
        port = 'COM3'
        self.board = OpenBCICyton(port=port, daisy=False)
        self.board.write_command('x1040010X')
        self.board.write_command('x2040010X')
        self.board.write_command('x3040010X')
        self.board.write_command('x4040010X')
        self.board.write_command('x5040010X')
        self.board.write_command('x6040010X')
        self.board.write_command('x7040010X')
        self.board.write_command('x8040010X')
        self.FIFO = FIFO  
        self.start_signal = start_signal
        self.terminate_signal = terminate_signal

    def print_raw(self, sample):

        # raw data save
        now = datetime.now()
        time = str(now.strftime("%M%S%f"))
        raw = (time + ',' +  str(sample.channels_data[0])+','+ 
            str(sample.channels_data[1])+','+
            str(sample.channels_data[2])+','+
            str(sample.channels_data[3])+','+
            str(sample.channels_data[4])+','+
            str(sample.channels_data[5])+','+
            str(sample.channels_data[6])+','+
            str(sample.channels_data[7])+ ' '
        )
        
        
        if  self.start_signal.is_set() == True :
            self.FIFO.put(raw)

        if self.terminate_signal.is_set() == True :
            self.FIFO.close()
            self.start_signal.clear()
            self.board.stop_stream()

    def run(self):
        
        # print data
        print('run')
        self.board.start_stream(self.print_raw)

    def stop(self):
        self.board.stop_stream()
        print('stop stream')

def recoding_call(FIFO: multiprocessing.Queue, start_signal : multiprocessing.Event, terminate_signal : multiprocessing.Event):
    recode = Recording(FIFO=FIFO, start_signal=start_signal, terminate_signal= terminate_signal)
    recode.run()



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
        keys = "status, ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7 \n"
        self.file.write(keys)


    def write(self, raw):
        self.file.write(raw)

    def close(self):
        # file close
        self.file.close()

class Sync:
      def __init__(self) -> None:

        # file save
        self.file = Save()
        self.file.open()

        # shared varibale
        self.FIFO = multiprocessing.Queue()
        self.start_signal = multiprocessing.Event()
        self.terminate_signal = multiprocessing.Event()

        mgr = multiprocessing.Manager()
        self.current_status = mgr.Namespace()

        self.current_status.number = -10
        self.current_status.status = -10
        self.current_status.time = -10

        self.gui = multiprocessing.Process(target= GUI_Data_Acquisition, args= (self.current_status, self.start_signal))
        self.gui.start()

        self.recode = multiprocessing.Process(target= recoding_call, args= (self.FIFO, self.start_signal, self.terminate_signal))
        self.recode.start()

      def run(self):

        accual_value = -10
        accual_time = -10
        next_value = -10
        next_time = -10

        while 1:
            if self.FIFO.empty() == 0:

                # print( (self.start_signal.is_set() == True),
                # self.FIFO.get() , self.current_status.status, self.current_status.number , 
                # self.current_status.time  ,"loop")
                data = (str(self.FIFO.get())).split(',')

                accual_time = int(data[0])
                next_time = int(self.current_status.time)
                next_value = self.current_status.number
                if accual_time >= next_time :
                    accual_value = next_value

                #print(accual_value,'/', data ,'/' , self.current_status.status, self.current_status.number , self.current_status.time )
                tem = (str(accual_value) + ',' + 
                    data[1] + ',' +
                    data[2] + ',' +
                    data[3] + ',' +
                    data[4] + ',' +
                    data[5] + ',' +
                    data[6] + ',' +
                    data[7] + ',' +
                    data[8]  + '\n' )
                self.file.write(tem)
                # print('start_signal', self.start_signal.is_set() == False)
                if (self.start_signal.is_set() == False)   :
                    self.file.close()
                    self.file = Save()
                    self.file.open()
                    
                    
            elif self.gui.is_alive() == False :
                self.terminate_signal.set()
                break
            else:
                # time.sleep(1)
                pass

if __name__ == "__main__":
    sync = Sync()
    sync.run() 
