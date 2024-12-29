from enum import Enum
import re
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui import QPen
from mapTableModel import BuildingTableModel

MAX_COOR = 8648

class BuildingType(Enum):
    Other = 0
    Residential = 1
    Commercial = 2
    Industrial = 3
    Office = 4
    Beautification = 5
    Education = 6
    PublicTransport = 7
    Police = 8
    Electricity = 9
    Monument = 10
    HealthCare = 11
    Fire = 12
    Road = 13
    VarsitySports = 14
    Water = 15
    Garbage = 16
    Disaster = 17
    ServicePoint = 18
    Fishing = 19


class Building(object):

    def __init__(self, id, name, srv, subsrv, icls):
        self.id = int(id)
        self.internal_name = name
        self.srv = srv
        self.subsrv = subsrv
        self.icls = icls

        self.name = ""
        self.points = []
        self.subb = None
        self.prntb = None

        # the BuildingPolygon object being drawn on the scene
        self.polygon = None

        self.find_building_type()


    def add_myname(self, myname):
        self.myname = myname
    
    # add a sub-building
    def add_child(self, subb):
        self.subb = int(subb)

    # add a parent building
    def add_parent(self, prntb):
        self.prntb = int(prntb)

    
    def add_point(self, x, y, z):
        x_norm, y_norm, z_norm = self.remap_coordinate(float(x), float(y), float(z))
        self.points.append([x_norm, y_norm, z_norm])


    def set_polygon(self, polygon_ref):
        self.polygon = polygon_ref
        self.polygon.set_building(self)

    def remap_coordinate(self, x, y, z):
        # How to remap coordnate: ONLY x and z
        # from [-32768, 32768] to [0.0, 1.0]
        x_out = (x + MAX_COOR) / (MAX_COOR * 2)
        z_out = (z - MAX_COOR) / (MAX_COOR * 2)
        y_out = y
        return x_out, y_out, z_out


    def find_building_type(self):
        # much simpler then segments
        if (re.match("^(.*residential).*$", self.srv.lower())):
            self.btype = BuildingType.Residential
        elif (re.match("^(.*commercial).*$", self.srv.lower())):
            self.btype = BuildingType.Commercial
        elif (re.match("^(.*industr).*$", self.srv.lower())):
            self.btype = BuildingType.Industrial
        elif (re.match("^(.*office).*$", self.srv.lower())):
            self.btype = BuildingType.Office
        elif (re.match("^(.*beautification).*$", self.srv.lower())):
            self.btype = BuildingType.Beautification
        elif (re.match("^(.*education).*$", self.srv.lower())):
            self.btype = BuildingType.Education
        elif (re.match("^(.*publictransport).*$", self.srv.lower())):
            self.btype = BuildingType.PublicTransport
        elif (re.match("^(.*police).*$", self.srv.lower())):
            self.btype = BuildingType.Police
        elif (re.match("^(.*electricity).*$", self.srv.lower())):
            self.btype = BuildingType.Electricity
        elif (re.match("^(.*monument).*$", self.srv.lower())):
            self.btype = BuildingType.Monument
        elif (re.match("^(.*healthcare).*$", self.srv.lower())):
            self.btype = BuildingType.HealthCare
        elif (re.match("^(.*fire).*$", self.srv.lower())):
            self.btype = BuildingType.Fire
        elif (re.match("^(.*road).*$", self.srv.lower())):
            self.btype = BuildingType.Road
        elif (re.match("^(.*sports).*$", self.srv.lower())):
            self.btype = BuildingType.VarsitySports
        elif (re.match("^(.*water).*$", self.srv.lower())):
            self.btype = BuildingType.Water
        elif (re.match("^(.*garbage).*$", self.srv.lower())):
            self.btype = BuildingType.Garbage
        elif (re.match("^(.*disaster).*$", self.srv.lower())):
            self.btype = BuildingType.Disaster
        elif (re.match("^(.*servicepoint).*$", self.srv.lower())):
            self.btype = BuildingType.ServicePoint
        elif (re.match("^(.*fishing).*$", self.srv.lower())):
            self.btype = BuildingType.Fishing
        else:
            self.btype = BuildingType.Other


class BuildingPolygon(QGraphicsPolygonItem):

    def __init__(self, polygon, pen, brush, detail_table_callback=None, parent=None):
        super().__init__(polygon, parent)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        self.defult_brush = brush
        self.defult_pen = pen
        self.setBrush(brush)
        self.setPen(pen)
        # set up the highlight pen
        self.highlight_pen = QPen(pen.color(), pen.widthF() + 0.5, pen.style(), pen.capStyle(), pen.joinStyle())

        self.detail_table_callback = detail_table_callback

    def set_building(self, building_ref):
        self.building = building_ref

    def hoverEnterEvent(self, event):
        self.setPen(self.highlight_pen)
        self.update()
        # print("Hovering enter at buliding: ", self.building.internal_name)
    
    def hoverLeaveEvent(self, event):
        self.setPen(self.defult_pen)
        self.update()
        # print("Hovering leave at buliding: ", self.building.internal_name)

    
    def mousePressEvent(self, event):
        # Handle the left-click event (check if it was the left button)
        if event.button() == Qt.LeftButton:
            if (self.detail_table_callback is not None):
                detail_model = BuildingTableModel(self.building)
                self.detail_table_callback(detail_model)
            else:
                print("Click at buliding: ", self.building.internal_name)
        
        # super().mousePressEvent(event)