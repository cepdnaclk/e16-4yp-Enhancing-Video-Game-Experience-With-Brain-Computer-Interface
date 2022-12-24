# importing libraries
from multiprocessing.connection import wait
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import random

import signal

from PyQt5.QtCore import *
import time
import threading
from pyOpenBCI import OpenBCICyton
from datetime import datetime
import multiprocessing

# end of recording action
def end_record(event, event_bci):
    print("clear")
    event.clear()
    event_bci.set()

# trigger start of recording action
# do recording
def start_record(event):
    print("set")
    event.set()

# ---------------------------- data recording ------------------------------

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

    def __init__(self, start_signal_rec,stop_bci_signal, status_record_val, board_val):
        super(Recording, self).__init__()
        self.file = Save()
        self.start_signal = start_signal_rec
        self.stop_bci = stop_bci_signal
        self.status_record = status_record_val
        self.board = board_val

    def print_raw(self, sample):
        
        raw = str(self.status_record)+',' + str(sample.channels_data) + '\n'
        self.file.write(raw)
        #print(raw)

        if self.stop_bci.is_set():
          # terminated connection
          self.board.stop_stream()
          print("stop stream")
          self.file.close()
              

    def start_file_write(self):
        # raw data save
        self.file.open()

        # print data
        print("start stream")
        self.board.start_stream(self.print_raw)
        
  
        

# ---------------------------- GUI ------------------------------

class SecondWindow(QMainWindow):

  def __init__(self, event_signal, bci_signal, status_record_val, curr_dir_val):
    super().__init__()
    self.start_signal_secw = event_signal
    self.bci_signal_secw = bci_signal
    self.status_record = status_record_val
    self.current_direction = curr_dir_val

    # setting title
    self.setWindowTitle("Trial Workflow")

    # setting geometry
    self.setGeometry(600,100,800,800)
    self.setStyleSheet("background-color: gray;")

    # calling method
    self.Components()
    # showing all the widgets
    self.show()

  # method for widgets
  def Components(self):

     #start button
   self.button1 = QPushButton(self)
   self.button1.setText("STOP")
   self.button1.width = 100
   self.button1.height = 75
   self.button1.setGeometry(250, 675, 300, 75)
   self.button1.clicked.connect(self.button1_clicked)
   self.button1.setStyleSheet("border : 1px solid black;background-color: white;border-radius: 10px;")
   self.button1.setFont(QFont('Arial', 20))


   self.image1 = QLabel(self)
   self.pixmap = QPixmap('images/1.jpg')
   self.pixmap = self.pixmap.scaled(575, 575)
   self.image1.setPixmap(self.pixmap)
   self.image1.setGeometry(100, 75, 575, 575)
   
   self.one()
    

   
  def one(self):
    self.counter1 = 0
    self.counter2_1 = 0
    self.counter2_2 = 0
    self.counter2_3 = 0
    self.counter3 = 0
    self.counter4 = 0
    self.counter5 = 0

    self.timer1 = QtCore.QTimer()
    self.timer1.timeout.connect(self.show_cue)
    self.timer1.start(500)

    # Action
    self.timer2_1 = QtCore.QTimer()
    self.timer2_1.timeout.connect(self.show_action_1)
    self.timer2_1.start(1000)

    self.timer2_2 = QtCore.QTimer()
    self.timer2_2.timeout.connect(self.show_action_2)
    self.timer2_2.start(2000)

    self.timer2_3 = QtCore.QTimer()
    self.timer2_3.timeout.connect(self.show_action_3)
    self.timer2_3.start(3000)

    self.timer3 = QtCore.QTimer()
    self.timer3.timeout.connect(self.show_relax)
    self.timer3.start(3500)

    self.timer4 = QtCore.QTimer()
    self.timer4.timeout.connect(self.show_rest)
    self.timer4.start(4500)

    self.timer5 = QtCore.QTimer()
    self.timer5.timeout.connect(self.show_start)
    self.timer5.start(7000)
   
  

  def show_cue(self):
    if self.counter1 == 0:

      num = [1,2,3,4]
      x = random.choice(num)
      

      if x == 1:
        self.status_record.value = 1
        self.pixmap = QPixmap('images/up.jpg')
        self.current_direction.value = 6

      elif x == 2:
        self.status_record.value = 1
        self.pixmap = QPixmap('images/down.jpg')
        self.current_direction.value = 3

      elif x == 3:
        self.status_record.value = 1
        self.pixmap = QPixmap('images/left.jpg')
        self.current_direction.value = 4

      else:
        self.status_record.value = 1
        self.pixmap = QPixmap('images/right.jpg')
        self.current_direction.value = 5
 
      
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)
      
    
    self.counter1 = self.counter1 + 1
    if self.counter1 > 0:
      self.timer1.stop()


  #action
  def show_action_1(self):

    if self.counter2_1 == 0:
      self.status_record.value = self.current_direction.value
      self.pixmap = QPixmap('images/1.jpg')
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)
      
    
    self.counter2_1 = self.counter2_1 + 1
    if self.counter2_1 > 0:
      self.timer2_1.stop()
  
  def show_action_2(self):

    if self.counter2_2 == 0:
      self.status_record.value = self.current_direction.value
      self.pixmap = QPixmap('images/1.jpg')
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)
      
    
    self.counter2_2 = self.counter2_2 + 1
    if self.counter2_2 > 0:
      self.timer2_2.stop()

  def show_action_3(self):

    if self.counter2_3 == 0:
      self.status_record.value = self.current_direction.value
      self.pixmap = QPixmap('images/1.jpg')
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)
      
    
    self.counter2_3 = self.counter2_3 + 1
    if self.counter2_3 > 0:
      self.timer2_3.stop()
  

  def show_relax(self):

    if self.counter3 == 0:
      self.status_record.value = 2
      self.pixmap = QPixmap('images/2.jpg')
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)
      
    
    self.counter3 = self.counter3 + 1
    if self.counter3 > 0:
      self.timer3.stop()
      
  
  def show_rest(self):

    if self.counter4 == 0:
      self.status_record.value = -1
      self.pixmap = QPixmap('images/black.jpg')
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)
      
    
    self.counter4 = self.counter4 + 1
    if self.counter4 > 0:
      self.timer4.stop()
     
  

  def show_start(self):

    if self.counter5 == 0:
      self.status_record.value = 0
      self.pixmap = QPixmap('images/1.jpg')
      self.pixmap = self.pixmap.scaled(575, 575)
      self.image1.setPixmap(self.pixmap)
      self.image1.setGeometry(100, 75, 575, 575)
      
    
    self.counter5 = self.counter5 + 1
    if self.counter5 > 0:
      self.timer5.stop()
      self.one()
  


  # start and stop button
  def button1_clicked(self):
    end_record(self.start_signal_secw, self.bci_signal_secw)
    self.w = Window(self.start_signal_secw, self.bci_signal_secw, self.status_record, self.current_direction)
    self.hide()
    self.w.show()
    


class Window(QMainWindow):

  def __init__(self, event_signal, bci_signal, status_record_val, curr_dir_val):
    super().__init__()
    self.start_signal_w = event_signal
    self.bci_signal_w = bci_signal
    self.status_record = status_record_val
    self.current_direction = curr_dir_val

    # setting title
    self.setWindowTitle("Trial Workflow")

    # setting geometry
    self.setGeometry(600,100,800,800)
    self.setStyleSheet("background-color: gray;")

    # calling method
    self.UiComponents()
    # showing all the widgets
    self.show()

  # method for widgets
  def UiComponents(self):

     #start button
   self.button1 = QPushButton(self)
   self.button1.setText("START")
   self.button1.width = 100
   self.button1.height = 75
   self.button1.setGeometry(250, 675, 300, 75)
   self.button1.clicked.connect(self.button1_clicked)
   self.button1.setStyleSheet("border : 1px solid black;background-color: white;border-radius: 10px;")
   self.button1.setFont(QFont('Arial', 20))

   #showing an image initially
   self.image1 = QLabel(self)
   self.pixmap = QPixmap('images/black.jpg')
   self.pixmap = self.pixmap.scaled(575, 575)
   self.image1.setPixmap(self.pixmap)
   self.image1.setGeometry(100, 75, 575, 575)

   
  

  # start and stop button
  def button1_clicked(self):

    start_record(self.start_signal_w)

    self.w1 = SecondWindow(self.start_signal_w, self.bci_signal_w, self.status_record, self.current_direction)
    self.w1.show()
    self.hide()

 



def gui(event, event_bci, status_record, current_dir):

    # time.sleep(3)
    # end_record(event)
    # t = threading.Timer(4, start_record, args = (event,))
    # t.start()

    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = Window(event,event_bci, status_record, current_dir)
    # start the app
    sys.exit(App.exec())


def record(event_button, event_bci, status_record, board):
    print("process2")
    event_button.wait()
    record_obj = Recording(event_button, event_bci, status_record, board)
    
    if event_button.is_set():
        # print("status rec", status_record.value)
        # print("curr_dir", current_dir.value)
        record_obj.start_file_write()


if __name__ == '__main__':

    # create connection
    board = OpenBCICyton(port='COM6', daisy=False)

    # event shared by both processes
    start_signal = multiprocessing.Event()
    stop_bci = multiprocessing.Event()

    status_recording = multiprocessing.Value('i', 0)
    current_direction = multiprocessing.Value('i', 3)

    process1 = multiprocessing.Process(target=gui, args=[start_signal,stop_bci, status_recording, current_direction])
    process1.start()

    process2 = multiprocessing.Process(target=record, args=[start_signal, stop_bci, status_recording, board])
    process2.start()