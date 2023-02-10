from PySide6.QtWidgets import (QGraphicsScene, QGraphicsView)
from PySide6.QtCore import Qt


# MapScene is attached to MapView to provide interations control 
# (mouse, keyboard or even touch)
class MapScene(QGraphicsScene):

    def __init__(self, parent, cursor_pos_callback):
        super().__init__(parent)
        self.cursor_pos_callback = cursor_pos_callback


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
        self.cursor_pos_callback(event.pos(), event.scenePos())
    

class MapView(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)

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
        