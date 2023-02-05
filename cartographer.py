import PySide6
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPixmap, QImage, QPen, QColor, QPolygonF, QBrush
from PIL import ImageQt

from segment import SegmentType, MAX_COOR
from building import BuildingType

# Cartographer draws map
class Cartographer(object):

    def __init__(self, scene_ref, view_ref, city_ref):
        self.mapScene = scene_ref
        self.mapView = view_ref
        self.city_data = city_ref


    def draw_map(self, size=4096):
        self.backend_size = size
        self.mapScene.clear()
        terrain_background = self.city_data.terrains.get_terrain_img()
        terrain_pixmap = QPixmap.fromImage(ImageQt.ImageQt(terrain_background))
        # w, h = terrain_pixmap.size().toTuple()
        terrain_pixmap = terrain_pixmap.scaled(size, size)
        self.mapScene.addPixmap(terrain_pixmap)
        self.mapView.fitInView(QRectF(0, 0, size, size), Qt.KeepAspectRatio)

        # segments
        self.draw_quays()
        self.draw_pedestrian_path()
        self.draw_pedestrian_streets()
        self.draw_streets()
        self.draw_highways()
        self.draw_train_tracks()
        self.draw_metro_tracks()

        # buildings
        self.draw_other_building()
        self.draw_ind_building()
        self.draw_off_building()
        self.draw_res_building()
        self.draw_com_building()

        self.mapScene.update()



    def draw_streets(self):
        for seg_id in self.city_data.street_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(Qt.white, pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen)


    def draw_pedestrian_streets(self):
        st_colour = QColor(223, 223, 223, 255)
        for seg_id in self.city_data.pedestrian_st_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen)

    
    def draw_highways(self):
        st_colour = QColor(255, 235, 161, 255)
        for seg_id in self.city_data.highway_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen) 


    def draw_quays(self):
        st_colour = QColor(191, 191, 191, 255)
        for seg_id in self.city_data.quay_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 3
            st_pen = QPen(st_colour, pen_width, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen) 


    def draw_train_tracks(self):
        st_colour = Qt.darkGray
        for seg_id in self.city_data.train_track_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen) 


    def draw_metro_tracks(self):
        st_colour = Qt.darkBlue
        for seg_id in self.city_data.metro_track_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen) 


    def draw_pedestrian_path(self):
        st_colour = Qt.darkGreen
        for seg_id in self.city_data.pedestrian_path_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen)

    # draw a single segment 
    def draw_segment(self, seg, pen=QPen()):
        for i, point in enumerate(seg.points):
            if i < (len(seg.points) - 1):
                # draw one sub-segment (invet Y axis)
                self.mapScene.addLine(  \
                            point[0] * self.backend_size,   \
                            -point[2] * self.backend_size,  \
                            seg.points[i+1][0] * self.backend_size, \
                            -seg.points[i+1][2] * self.backend_size,
                            pen)


    def draw_res_building(self):
        b_pen = QPen(QColor(32,96,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(230, 255, 230))
        for b_id in self.city_data.res_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_com_building(self):
        b_pen = QPen(QColor(95,56,96), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(230, 230, 255))
        for b_id in self.city_data.com_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_ind_building(self):
        b_pen = QPen(QColor(128,96,0), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(255, 255, 230))
        for b_id in self.city_data.ind_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_off_building(self):
        b_pen = QPen(QColor(0,96,96), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(220, 255, 255))
        for b_id in self.city_data.off_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_other_building(self):
        b_pen = QPen(QColor(191,191,191), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(255, 255, 255, 0))
        for b_id in self.city_data.other_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)

    # draw a single building
    def draw_building(self, building, pen=QPen(), brush=QBrush()):
        polygon = QPolygonF()
        for point in building.points:
            polygon.append(QPointF(point[0] * self.backend_size, \
                                -point[2] * self.backend_size))
        self.mapScene.addPolygon(polygon, pen, brush)