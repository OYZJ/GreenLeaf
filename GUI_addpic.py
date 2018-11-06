"""
@author: Zhangjian Ouyang
@date: 10/25/2018
This file is GUI of project of CS501
"""

import binary_image
import cv2
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt


# class DraggableLabel(QLabel):
#     def __init__(self,parent,image):
#         super(QLabel,self).__init__(parent)
#         self.setPixmap(QPixmap(image))
#         self.show()
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drag_start_position = event.pos()
#
#     def mouseMoveEvent(self, event):
#         if not (event.buttons() & Qt.LeftButton):
#             return
#         if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
#             return
#         drag = QDrag(self)
#         mimedata = event.mimeData()
#         mimedata.setText(self.text())
#         mimedata.setImageData(self.pixmap().toImage())
#
#         drag.setMimeData(mimedata)
#         pixmap = QPixmap(self.size())
#         painter = QPainter(pixmap)
#         painter.drawPixmap(self.rect(), self.grab())
#         painter.end()
#         drag.setPixmap(pixmap)
#         drag.setHotSpot(event.pos())
#         drag.exec_(Qt.CopyAction | Qt.MoveAction)

class Label(QLabel):
    """
    Enable the label can be dropped
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.path = ""
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            print("Yes")
        else:
            e.ignore()

    def dropEvent(self, e):
        self.setText(e.mimeData().text())
        temp_path = e.mimeData().text()
        print(temp_path)
        self.path = temp_path[8:]
        print(self.path)

    def get_path(self):
        print("get_path", self.path)
        return self.path


class Figure_Canvas(FigureCanvas):
    """
    Drawing chart with matplt
    """
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
    """
    Main class
    """
    def __init__(self):
        super().__init__()
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture(0)
        # self.filename = "filename"
        self.initUI()
        # self.slot_init()

    def slot_init(self):
        """
        Initialize the slot
        :return:
        """
        self.timer_camera.start(30)
        self.timer_camera.timeout.connect(self.pic_capture)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawBrushes(qp)
        qp.end()

    def drawBrushes(self, qp):
        brush = QBrush(Qt.NoBrush)
        qp.setBrush(brush)
        qp.drawRect(1200, 40, 450, 600)
        qp.drawRect(40, 40, 1120, 600)

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
        self.graphicview.setWindowTitle("Data")
        self.graphicview.setScene(graphicscene)


        # label 1 shows the species
        label1 = QLabel(self)
        label1.setText("Species")
        label1.setFont(QFont("Roman times", 8, QFont.Bold))
        label1.move(60, 660)
        self.qle1 = QLineEdit(self)
        self.qle1.move(60, 710)
        self.qle1.textChanged[str].connect(self.name)

        # label 2 shows the origin image
        self.label2 = Label(self)
        self.label2.resize(480, 480)
        pe = QPalette()
        pe.setColor(QPalette.WindowText, Qt.black)
        self.label2.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.label2.setPalette(pe)
        self.label2.move(60, 100)

        # label 3 shows the processed image
        self.label3 = QLabel(self)
        self.label3.resize(480, 480)
        self.label3.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.gray)
        self.label3.setPalette(pe)
        self.label3.move(650, 100)

        # Orginal image label
        self.label4 = QLabel(self)
        self.label4.setAcceptDrops(True)
        self.label4.setText("Original Image")
        self.label4.setFont(QFont("Roman times", 8, QFont.Bold))
        self.label4.move(60, 60)

        # Process image label
        self.label5 = QLabel(self)
        self.label5.setText("Processed Image")
        self.label5.setFont(QFont("Roman times", 8, QFont.Bold))
        self.label5.move(650, 60)

        # Feature label
        self.label6 = QLabel(self)
        self.label6.setText("Feature")
        self.label6.setFont(QFont("Roman times", 8, QFont.Bold))
        self.label6.move(1250, 60)

        # Perimeter label
        label7 = QLabel(self)
        label7.setText("perimeter")
        label7.move(1250, 100)
        self.qle7 = QLineEdit(self)
        self.qle7.move(1250, 150)

        # Area label
        label8 = QLabel(self)
        label8.setText("Area")
        label8.move(1250, 200)
        self.qle8 = QLineEdit(self)
        self.qle8.move(1250, 250)

        # MinL label
        label9 = QLabel(self)
        label9.setText("MinL")
        label9.move(1250, 300)
        self.qle9 = QLineEdit(self)
        self.qle9.move(1250, 350)

        # MaxL label
        label10 = QLabel(self)
        label10.setText("MaxL")
        label10.move(1250, 400)
        self.qle10 = QLineEdit(self)
        self.qle10.move(1250, 450)

        # Eccentricity label
        label11 = QLabel(self)
        label11.setText("Eccentricity")
        label11.move(1250, 500)
        self.qle11 = QLineEdit(self)
        self.qle11.move(1250, 550)


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

        # Load button
        btn3 = QPushButton('load', self)
        btn3.clicked.connect(self.loadFile)
        btn3.resize(btn3.sizeHint())
        btn3.move(1700, 100)

        # Process button
        btn4 = QPushButton('Process', self)
        btn4.clicked.connect(self.image_process)
        btn4.resize(btn4.sizeHint())
        btn4.move(1700, 200)

        self.setGeometry(600, 600, 2000, 800)
        pe.setBrush(self.backgroundRole(), QBrush(QPixmap('bg.jpg')))
        self.setPalette(pe)
        self.setWindowTitle('CS501: Green Leaf')
        self.show()
        if cv2.waitKey(1) & 0xFF == ord('c'):
            self.cap.release()
            cv2.destroyAllWindows()


    def loadFile(self):
        """
        load image
        :return: image path
        """
        global fname
        print("load--file")
        fname, _ = QFileDialog.getOpenFileName(self, 'choose pic', 'C:\personal files\programming\Python\CS501\project\Project_Code\Project_Code\GreenLeaf', 'Image files(*.jpg *.gif *.png)')
        pic = cv2.imread(fname)
        pic = cv2.resize(pic, (480, 480), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('test.jpg', pic)
        self.label2.setPixmap(QPixmap('test.jpg'))
        self.label4
        return fname


    def name(self):
        """
        Show the species of the image
        :return:
        """
        self.qle1.setText("Cup")

    def image_process(self):
        """
        process image & extract features
        :return:
        """
        print(fname)
        binary_image.binary('test.jpg')
        pic = QtGui.QPixmap('2.jpg')
        self.label3.setPixmap(pic)
        self.qle7.setText("12")
        self.qle8.setText("13213")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())
