import PySide6
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPixmap, QImage, QPen, QColor, QPolygonF, QBrush
from PySide6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from PIL import ImageQt

from segment import SegmentType, MAX_COOR
from building import BuildingType

# Cartographer draws map
class Cartographer(object):

    def __init__(self, scene_ref, view_ref, city_ref, status_bar_ref):
        self.mapScene = scene_ref
        self.mapView = view_ref
        self.city_data = city_ref
        self.status_bar = status_bar_ref


    def draw_map(self, size=4096):
        self.backend_size = size
        self.mapScene.clear()
        terrain_background = self.city_data.terrains.get_terrain_img()
        terrain_pixmap = QPixmap.fromImage(ImageQt.ImageQt(terrain_background))
        # w, h = terrain_pixmap.size().toTuple()
        terrain_pixmap = terrain_pixmap.scaled(size, size)
        self.mapScene.addPixmap(terrain_pixmap)
        self.mapView.fitInView(QRectF(0, 0, size, size), Qt.KeepAspectRatio)

        self.draw_quays()
        self.draw_pedestrian_streets()
        self.draw_streets()
        self.draw_highways()
        self.draw_transit_building()
        self.draw_tram_tracks()
        self.draw_train_tracks()
        self.draw_metro_tracks()
        self.draw_other_building()
        self.draw_beauti_building()
        self.draw_pedestrian_path()
        self.draw_garb_building()
        self.draw_ind_building()
        self.draw_off_building()
        self.draw_res_building()
        self.draw_com_building()
        self.draw_fish_building()
        self.draw_police_building()
        self.draw_elec_building()
        self.draw_fire_building()
        self.draw_road_building()
        self.draw_serv_building()
        self.draw_disaster_building()
        self.draw_water_building()
        self.draw_mont_building()
        self.draw_edu_building()
        self.draw_sport_building()
        self.draw_health_building()
        self.draw_tram()
        

        self.mapScene.update()



    def draw_streets(self):
        for seg_id in self.city_data.street_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(QColor(248, 249, 250), pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen)
        
        for seg_id in self.city_data.street_segs:
            seg = self.city_data.segs_dict[seg_id]
            if (seg.seg_type.has_tram):
                track_pen = QPen(Qt.gray, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                self.draw_segment(seg, track_pen)


    def draw_pedestrian_streets(self):
        st_colour = QColor(223, 223, 223, 255)
        for seg_id in self.city_data.pedestrian_st_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            self.draw_segment(seg, st_pen)
        
        for seg_id in self.city_data.pedestrian_st_segs:
            seg = self.city_data.segs_dict[seg_id]
            if (seg.seg_type.has_tram):
                track_pen = QPen(Qt.gray, 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
                self.draw_segment(seg, track_pen)

    
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
            st_pen = QPen(st_colour, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            st_pen.setCosmetic(True)
            self.draw_segment(seg, st_pen) 


    def draw_metro_tracks(self):
        st_colour = Qt.darkBlue
        for seg_id in self.city_data.metro_track_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            st_pen.setCosmetic(True)
            self.draw_segment(seg, st_pen) 


    def draw_tram_tracks(self):
        st_colour = Qt.red
        for seg_id in self.city_data.tram_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            st_pen.setCosmetic(True)
            self.draw_segment(seg, st_pen) 


    def draw_pedestrian_path(self):
        st_colour = QColor(63,129,0)
        for seg_id in self.city_data.pedestrian_path_segs:
            seg = self.city_data.segs_dict[seg_id]
            pen_width = seg.width * (self.backend_size / MAX_COOR) / 2
            st_pen = QPen(st_colour, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            st_pen.setCosmetic(True)
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
        b_pen = QPen(QColor(32,128,0), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(220, 255, 255))
        for b_id in self.city_data.off_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)
    

    def draw_beauti_building(self):
        b_pen = QPen(QColor(0,96,96), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(180, 255, 180))
        for b_id in self.city_data.beauti_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_edu_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.edu_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_sport_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.sport_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_transit_building(self):
        b_pen = QPen(QColor(95,56,96), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(230, 200, 255))
        for b_id in self.city_data.transit_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_police_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.police_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_elec_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.elec_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_fire_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.fire_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_road_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.road_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_serv_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.serv_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_disaster_building(self):
        b_pen = QPen(QColor(96,32,32), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(224,198,204))
        for b_id in self.city_data.disaster_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_water_building(self):
        b_pen = QPen(QColor(32,32,95), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(135,191,191))
        for b_id in self.city_data.water_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_garb_building(self):
        b_pen = QPen(QColor(123, 85, 0), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(204,171,62))
        for b_id in self.city_data.garb_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_mont_building(self):
        b_pen = QPen(QColor(96,96,96), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(184,192,201))
        for b_id in self.city_data.mont_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)
    

    def draw_health_building(self):
        b_pen = QPen(QColor(127,0,0), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(255, 255, 255))
        for b_id in self.city_data.health_buils:
            building = self.city_data.building_dict[b_id]
            poly = self.draw_building(building, b_pen, b_brush)
            icon = QGraphicsPixmapItem(QPixmap("icon/health.png"), poly)
            # print(icon.scenePos())


    def draw_fish_building(self):
        b_pen = QPen(QColor(128,96,0), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        b_brush = QBrush(QColor(255, 255, 230))
        for b_id in self.city_data.fish_buils:
            building = self.city_data.building_dict[b_id]
            self.draw_building(building, b_pen, b_brush)


    def draw_other_building(self):
        b_pen = QPen(QColor(95,56,96), 0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
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
        return self.mapScene.addPolygon(polygon, pen, brush)


    def draw_tram(self):
        for node in self.city_data.node_dict.values():
            if (node.subsrv == "PublicTransportTram"):
                self.draw_dot(node, 2, Qt.red)


    def draw_dot(self, node, r, color):
        dot_pen = QPen(color, r, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        dot_pen.setCosmetic(True)
        rec_x = node.x * self.backend_size - r
        rec_y = -node.z * self.backend_size - r
        self.mapScene.addEllipse(rec_x, rec_y, 2*r, 2*r, dot_pen)