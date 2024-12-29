from PySide6.QtWidgets import (QGraphicsScene, QGraphicsView)
from PySide6.QtCore import Qt, Signal


# MapScene is attached to MapView to provide interations control 
# (mouse, keyboard or even touch)
class MapScene(QGraphicsScene):

    def __init__(self, parent, cursor_pos_callback, detail_table_callback):
        super().__init__(parent)
        self.cursor_pos_callback = cursor_pos_callback
        self.detail_table_callback = detail_table_callback


    def set_view_ref(self, view):
        self.view_ref = view

    # mouse wheel to zoom
    # def wheelEvent(self, event):
    #     wheel_setp = event.delta() / 120
    #     self.view_ref.scale(1 + wheel_setp/10, 1 + wheel_setp/10)
    #     super().wheelEvent(event)

    # keyboard + and - to zoom
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Plus):
            self.view_ref.scale(1.1, 1.1)
        elif (event.key() == Qt.Key_Minus):
            self.view_ref.scale(0.9, 0.9)

    # get the location of the current cursor
    def mouseMoveEvent(self, event):
        # call the callback function to update the location display
        self.cursor_pos_callback(event.pos(), event.scenePos())
        # then sent the event down to any items expecting it (such as hover)
        super().mouseMoveEvent(event)
    

class MapView(QGraphicsView):

    droppedFiles = Signal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    # mouse wheel to zoom 
    # has to implement here to disable scolling?
    def wheelEvent(self, event):
        if (abs(event.angleDelta().x()) > abs(event.angleDelta().y())):
            wheel_move = event.angleDelta().x()
        else:
            wheel_move = event.angleDelta().y()
        wheel_setp = wheel_move / 120
        self.scale(1 + wheel_setp/10, 1 + wheel_setp/10)
        # super().wheelEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            print(links)
            self.droppedFiles.emit(links)
        else:
            event.ignore()
