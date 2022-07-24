# importing libraries
from multiprocessing.connection import wait
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import time
import random
from recording import *

# cycle time
cycle_time = 7000
white_dot_1 = 0
direction = 500
white_dot_2 = 1000
blue_dot = 3500
rest_time = 4500


class SecondWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Trial Workflow")

        # setting geometry
        self.setGeometry(600, 100, 800, 800)
        self.setStyleSheet("background-color: gray;")

        # image index
        self.image_name = ['1', '2', 'black', 'down', 'left', 'right', 'up']
        self.image_index = 0

        self.Components()

        # full time cycle 7seconds
        self.timer_cycle = QtCore.QTimer()
        self.timer_cycle.timeout.connect(self.cycle)
        self.timer_cycle.start(7000)

        # showing all the widgets
        self.show()

    # method for widgets
    def Components(self):

        # start button
        self.button1 = QPushButton(self)
        self.button1.setText("STOP")
        self.button1.width = 100
        self.button1.height = 75
        self.button1.setGeometry(250, 675, 300, 75)
        self.button1.clicked.connect(self.button1_clicked)
        self.button1.setStyleSheet("border : 1px solid black;background-color: white;border-radius: 10px;")
        self.button1.setFont(QFont('Arial', 20))

        # image box
        self.image1 = QLabel(self)

        # start cycle zero
        self.cycle()


    def show_image(self, number):

        set_status(number)
        self.pixmap = QPixmap('images/' + self.image_name[number] + '.jpg')
        self.pixmap = self.pixmap.scaled(575, 575)
        self.image1.setPixmap(self.pixmap)
        self.image1.setGeometry(100, 75, 575, 575)

    def cycle(self):

        # 0 = white dot
        # 1 = blue dot
        # 2 = black screen
        # 3 - 6 = direction (down, left, right, up)

        # white dot time  = 0 base
        self.show_image(0)

        # random direction time = 0.5s
        x = random.randint(3,6)
        self.dirction_timer = QtCore.QTimer()
        self.dirction_timer.singleShot(direction, lambda: self.show_image(x))

        # 2nd white dot time = 1s
        self.white_dot_timer = QtCore.QTimer()
        self.white_dot_timer.singleShot(white_dot_2, lambda: self.show_image(0))

        # blue dot time = 3.5 second
        self.blue_dot_timer = QtCore.QTimer()
        self.blue_dot_timer.singleShot(blue_dot, lambda: self.show_image(1) )

        # black reset time = 4.5s
        self.reset_timer = QtCore.QTimer()
        self.reset_timer.singleShot(rest_time, lambda: self.show_image(2))


    # start and stop button
    def button1_clicked(self):

        end_record()

        self.w = Window()
        self.hide()
        self.w.show()


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Trial Workflow")

        # setting geometry
        self.setGeometry(600, 100, 800, 800)
        self.setStyleSheet("background-color: gray;")

        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()

    # method for widgets
    def UiComponents(self):
        # start button
        self.button1 = QPushButton(self)
        self.button1.setText("START")
        self.button1.width = 100
        self.button1.height = 75
        self.button1.setGeometry(250, 675, 300, 75)
        self.button1.clicked.connect(self.button1_clicked)
        self.button1.setStyleSheet("border : 1px solid black;background-color: white;border-radius: 10px;")
        self.button1.setFont(QFont('Arial', 20))

        # showing an image initially
        self.image1 = QLabel(self)
        self.pixmap = QPixmap('images/black.jpg')
        self.pixmap = self.pixmap.scaled(575, 575)
        self.image1.setPixmap(self.pixmap)
        self.image1.setGeometry(100, 75, 575, 575)

    # start and stop button
    def button1_clicked(self):
        # start recode
        worker_Recored()
        start_record()

        self.w1 = SecondWindow()
        self.w1.show()
        self.hide()


# create pyqt5 app
App = QApplication(sys.argv)
# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())
