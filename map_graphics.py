import PySide6
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPen, QColor, QPolygonF, QBrush
from PySide6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem


class TransitStopMark(QGraphicsEllipseItem):

    def __init__(self, x, y, h, w, parent=None):
        super().__init__(parent)
        self.setRect(x, y, w, h)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

    
    def itemChange(self, change, value):
        # super().itemChange(change, value)
        # print(change)
        if (change == QGraphicsItem.ItemScaleChange):
            print(value)
        return QGraphicsItem.itemChange(self, change, value)
        