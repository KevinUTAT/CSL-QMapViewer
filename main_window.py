import sys
import os
from PIL import ImageQt
# Get Qt components
import PySide6
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsView
from PySide6.QtCore import QFile, QObject, QRectF, Qt, Slot
from PySide6.QtGui import QPixmap, QImage, QPen, QColor
# get local sources
from mapScene import MapScene, MapView

from city_data import CityData
from segment import SegmentType, MAX_COOR
from cartographer import Cartographer


class MainWindow(QObject):
    def __init__(self, ui_file, parent=None):
        super(MainWindow, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)
        
        loader = QUiLoader()
        loader.registerCustomWidget(MapView)
        self.window = loader.load(ui_file)
        ui_file.close()

        # "Global" flags
        self.city_loaded = False

        self.__init_frontend_elements()

        self.window.show()

        self.__load_city_elements(sys.argv[1])

        self.cartographer = Cartographer(self.mapScene, self.mapView, self.city_data)
        self.cartographer.draw_map()


    # initialize all the GUI elements
    def __init_frontend_elements(self):

        # === Map viewer ===============================================
        self.mapScene = MapScene(self)
        self.mapView = self.window.findChild(MapView, 'mapView')
        self.mapView.setScene(self.mapScene)
        self.mapScene.set_view_ref(self.mapView)
        self.mapView.setDragMode(QGraphicsView.ScrollHandDrag)  # enable panning
        self.mapView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    # load backend city data elements
    def __load_city_elements(self, clsmap_path):
        self.city_data = CityData(clsmap_path)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow('csl_mapper.ui')
    sys.exit(app.exec())