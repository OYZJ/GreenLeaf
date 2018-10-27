"""
@author: Zhangjian Ouyang
@date: 10/25/2018
This file is GUI of project of CS501
"""

import cv2
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QPushButton, QApplication, QLineEdit)
from PyQt5.QtCore import QCoreApplication, Qt


class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes = fig.add_subplot(121)
        self.axes1 = fig.add_subplot(122)

    def test(self):
        x = ['SVM', 'RR', 'RT', 'Kmeans']
        y = [99, 97, 95, 98]
        width = 0.5
        self.axes.bar([0, 1, 2, 3], y, width, align="center")
        self.axes.set_xticks([0, 1, 2, 3])
        self.axes.set_xticklabels(x)
        self.axes.set_ylabel('accuracy %')
        x1 = ['SVM', 'RR', 'RT', 'Kmeans']
        y1 = [50, 80, 20, 90]
        width = 0.5
        self.axes1.bar([0, 1, 2, 3], y1, width, align="center", color='green')
        self.axes1.set_xticks([0, 1, 2, 3])
        self.axes1.set_xticklabels(x1)
        self.axes1.set_ylabel('possibility %')




class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture(0)
        self.initUI()
        self.slot_init()

    def slot_init(self):
        """
        Initialize the slot
        :return:
        """
        self.timer_camera.start(30)
        self.timer_camera.timeout.connect(self.pic_capture)

    def initUI(self):
        """
        Setup the GUI
        :return:
        """

        # chart
        self.graphicview = QtWidgets.QGraphicsView()
        chart = Figure_Canvas()
        chart.test()
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(chart)
        self.graphicview.setScene(graphicscene)


        # label 1 shows the species
        label1 = QLabel(self)
        label1.setText("Species")
        label1.move(60, 700)
        self.qle1 = QLineEdit(self)
        self.qle1.move(60, 750)
        self.qle1.textChanged[str].connect(self.name)

        # label 2 shows the origin image
        self.label2 = QLabel(self)
        self.label2.resize(640, 480)
        self.label2.move(60, 100)
        self.pic_capture()

        # label 3 shows the processed image
        self.label3 = QLabel(self)
        self.label3.resize(640, 480)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.red)
        self.label3.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.black)
        self.label3.setPalette(pe)
        self.label3.move(800, 100)

        # label 4
        self.label4 = QLabel(self)
        self.label4.setText("Original Image")
        self.label4.move(60, 60)

        # label 5
        self.label5 = QLabel(self)
        self.label5.setText("Processed Image")
        self.label5.move(800, 60)

        # Quit button
        btn1 = QPushButton('Quit', self)
        btn1.clicked.connect(QCoreApplication.instance().quit)
        btn1.resize(btn1.sizeHint())
        btn1.move(1700, 500)

        # Species button
        btn2 = QPushButton('Species', self)
        btn2.clicked.connect(self.name)
        btn2.clicked.connect(self.graphicview.show)
        btn2.resize(btn2.sizeHint())
        btn2.move(1700, 300)

        # Capture button
        btn3 = QPushButton('Capture', self)
        btn3.clicked.connect(self.pic_show)
        btn3.resize(btn3.sizeHint())
        btn3.move(1700, 100)

        # Process button
        btn4 = QPushButton('Process', self)
        btn4.clicked.connect(self.image_process)
        btn4.resize(btn4.sizeHint())
        btn4.move(1700, 200)

        self.setGeometry(600, 600, 2000, 1000)
        self.setWindowTitle('CS501: Green Leaf')
        self.show()
        if cv2.waitKey(1) & 0xFF == ord('c'):
            self.cap.release()
            cv2.destroyAllWindows()

    # def pic_resize(self):
    #     """
    #     resize the picture
    #     :return:
    #     """
    #     pic = cv2.imread('2018-09-10.png')
    #     pic = cv2.resize(pic, (600, 600), interpolation=cv2.INTER_CUBIC)
    #     # cv2.imshow('', pic)
    #     cv2.imwrite('2018-09-10-1.png', pic)

    def name(self):
        """
        Show the species of the image
        :return:
        """
        self.qle1.setText("Cup")

    def pic_show(self):
        """
        Show the captured image
        :return:
        """
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('capture.jpg', frame)
        pic = QtGui.QPixmap('capture.jpg')
        self.label3.setPixmap(pic)

    def image_process(self):
        image = cv2.imread("capture.jpg")
        im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('processed_image.jpg', im_gray)
        pic = QtGui.QPixmap('processed_image.jpg')
        self.label3.setPixmap(pic)

    def pic_capture(self):
        """
        show the video stream
        :return:
        """
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('Capture', frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.label2.setPixmap(QtGui.QPixmap.fromImage(showImage))

        # if cv2.waitKey(1) & 0xFF == ord('c'):
        #     cv2.imwrite('2018-09-10-1.jpg', frame)
        #     break
        # cap.release()
        # cv2.destroyAllWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
