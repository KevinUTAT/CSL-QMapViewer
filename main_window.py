import sys
import os
from PIL import ImageQt
# Get Qt components
import PySide6
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsView
from PySide6.QtCore import QFile, QObject, QRectF, Qt, Slot
from PySide6.QtGui import QPixmap, QImage
# get local sources
from mapScene import MapScene, MapView

from city_data import CityData


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
        self.draw_map()


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


    def draw_map(self, size=4096):
        self.backend_size = size
        self.mapScene.clear()
        terrain_background = self.city_data.terrains.get_terrain_img()
        terrain_pixmap = QPixmap.fromImage(ImageQt.ImageQt(terrain_background))
        # w, h = terrain_pixmap.size().toTuple()
        terrain_pixmap = terrain_pixmap.scaled(size, size)
        self.mapScene.addPixmap(terrain_pixmap)
        self.mapView.fitInView(QRectF(0, 0, size, size), Qt.KeepAspectRatio)

        self.draw_networks()

        self.mapScene.update()

    
    def draw_networks(self):

        for seg in self.city_data.segs_dict.values():
            if (seg.seg_type > 0):
                self.draw_segment(seg)

    # draw a single segment 
    def draw_segment(self, seg):
        for i, point in enumerate(seg.points):
            if i < (len(seg.points) - 1):
                # draw one sub-segment (invet Y axis)
                self.mapScene.addLine(  \
                            point[0] * self.backend_size,   \
                            -point[2] * self.backend_size,  \
                            seg.points[i+1][0] * self.backend_size, \
                            -seg.points[i+1][2] * self.backend_size)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow('csl_mapper.ui')
    sys.exit(app.exec())