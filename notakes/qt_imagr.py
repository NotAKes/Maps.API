
import sys
from PyQt6.QtCore import QPoint
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QLabel, QSlider
from PyQt6.QtGui import QImage, QColor, QTransform
from PyQt6.QtGui import QPixmap
from qt_form import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
from main import get_image


class AlphaManagement(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Диалоговое окно')
        self.image = QLabel(self)
        self.image.resize(800, 800)
        self.image.move(0, 10)
        self.curr_image = QImage('../map.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    get_image()
    app = QApplication(sys.argv)
    ex = AlphaManagement()
    ex.show()
    sys.exit(app.exec())