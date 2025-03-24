import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
import requests
from PIL import Image
import sys
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QLabel, QSlider
from PyQt6.QtGui import QImage, QColor, QTransform
from PyQt6.QtGui import QPixmap
from qt_form import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
from geocoder import show_map, get_ll, geocoder, get_address_coords


def get_image_and_spn(spn, lat=56.92, lon=60.56, theme='light'):
    # print(spn)

    toponym_to_find = 'pass'
    if toponym_to_find:
        lat, lon = lat, lon
        ll_spn = f'll-{lat},{lon}&spn={spn},{spn}'
        show_map(ll_spn)
        ll, spn = f'{lat},{lon}', f'{spn}'
        ll_spn = f'll={ll}&spn={spn}'
        show_map(ll_spn)
        point_param = f'pt-{ll}'
        show_map(ll_spn, add_params=point_param)
    toponym_longitude, toponym_lattitude = str(lon), str(lat)

    delta = spn
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "apikey": apikey,
        "pt": ",".join([toponym_longitude, toponym_lattitude]),
        'theme':theme
    }
    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    im = BytesIO(response.content)
    opened_image = Image.open(im)
    opened_image.save('map.png')
    return float(spn)


class AlphaManagement(QMainWindow, Ui_MainWindow):
    def __init__(self, spn):
        super().__init__()
        self.setupUi(self)
        self.spn = spn
        self.coords = [56.92, 60.56]
        self.theme = 'light'
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Диалоговое окно')
        self.image = QLabel(self)
        self.image.resize(800, 800)
        self.image.move(0, 10)
        self.curr_image = QImage('map.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.spn += 0.05
        elif event.key() == Qt.Key.Key_PageDown:
            self.spn -= 0.05
        elif event.key() == Qt.Key.Key_Down and self.coords[0] >= 0.1:
            self.coords[0] -= 0.05
        elif event.key() == Qt.Key.Key_Up and self.coords[0] <= 110:
            self.coords[0] += 0.05
        elif event.key() == Qt.Key.Key_Right and self.coords[1] <= 110:
            self.coords[1] += 0.05
        elif event.key() == Qt.Key.Key_Left and self.coords[1] >= 0.1:
            self.coords[1] -= 0.05

        elif event.key() == Qt.Key.Key_B:
            if self.theme == 'dark':
                self.theme = 'light'
            else:
                self.theme = 'dark'

        if 0.05 >= float(self.spn) > 2.5:
            self.spn = '0.5'

        get_image_and_spn(str(self.spn), self.coords[0], self.coords[1], self.theme)
        self.curr_image = QImage('map.png')
        self.pixmap = QPixmap.fromImage(self.curr_image)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    spn = get_image_and_spn(0.1)
    app = QApplication(sys.argv)
    ex = AlphaManagement(spn)
    ex.show()
    sys.exit(app.exec())
