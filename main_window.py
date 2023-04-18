import sys
import os
from PIL import ImageQt
from pathlib import Path

# Get Qt components
import PySide6
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QWidget, QGraphicsView,
                               QStatusBar, QFileDialog, QProgressDialog)
from PySide6.QtCore import QFile, QObject, QRectF, Qt, Slot
from PySide6.QtGui import QPixmap, QImage, QPen, QColor, QAction

# Get local sources
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

        # Only get the first argument, which should be the file path
        if (len(sys.argv) > 1):
            self.load_city(sys.argv[1])

    # initialize all the GUI elements
    def __init_frontend_elements(self):
        # === Status Bar ===============================================
        self.status_bar = self.window.findChild(QStatusBar, 'statusbar')

        # === Menu actions =============================================
        self.window.findChild(QAction, 'actionOpen'). \
            triggered.connect(self.__open_new_city)

        # === Map viewer ===============================================
        self.mapScene = MapScene(self, self.show_cursor_pos)
        self.mapView = self.window.findChild(MapView, 'mapView')
        self.mapView.setScene(self.mapScene)
        self.mapScene.set_view_ref(self.mapView)
        self.mapView.setDragMode(QGraphicsView.ScrollHandDrag)  # enable panning
        self.mapView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.mapView.droppedFiles.connect(self.onDropped)

    def onDropped(self, links):
        for link in links:
            if Path(link).suffix == ".cslmap":
                self.load_city(links[-1])

    def __open_new_city(self):
        self.load_city()

    # load and draw a new city from file
    def load_city(self, clsmap_path=None):  # passed sys.argv earlier to clsmap_path
        if clsmap_path is None:  # if sys.argv is empty (None), get path from dropped in *.cslmap file
            (clsmap_path, ext) = QFileDialog.getOpenFileName( \
                filter="CSLMAP files (*.cslmap)")

        self.__load_city_elements(clsmap_path)  # loads terrain, networks, buildings, transit
        self.backend_size = 4096
        self.cartographer = Cartographer(self.mapScene, self.mapView, self.city_data, self.status_bar)
        self.cartographer.draw_map(self.backend_size)
        self.city_loaded = True

    # load backend city data elements
    def __load_city_elements(self, clsmap_path):
        #  adds a progress bar with 5 steps, at each element loaded get_*****(), set bar 1 higher
        progress_bar = QProgressDialog("Loading data...", "Abort", \
                                       0, 5, self.window)
        progress_bar.setWindowModality(Qt.WindowModal)

        self.city_data = CityData(clsmap_path)
        progress_bar.setValue(1)

        self.city_data.get_terrains()
        progress_bar.setValue(2)

        self.city_data.get_networks()
        progress_bar.setValue(3)

        self.city_data.get_buildings()
        progress_bar.setValue(4)

        self.city_data.get_transit()
        progress_bar.setValue(5)

    def show_cursor_pos(self, cursor_pos, cursor_scene_pos):
        pos_x = cursor_scene_pos.x() / self.backend_size * (2 * MAX_COOR) - MAX_COOR
        pos_y = -cursor_scene_pos.y() / self.backend_size * (2 * MAX_COOR) - MAX_COOR
        msg = f"X={pos_x:.4f},\tY={pos_y:.4f}"
        self.status_bar.showMessage(msg)


if __name__ == "__main__":
    app = QApplication(
        sys.argv)  # sys.argv gets the specified path when running "python main_window.py <path_to_cslmap>"
    main_window = MainWindow('csl_mapper.ui')
    sys.exit(app.exec())
