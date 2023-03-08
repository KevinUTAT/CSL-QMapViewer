from enum import Enum
import re

MAX_COOR = 8648

class SegmentLane(object):
    lane_type =    {"None"                  : 0,
                    "Pedestrian"            : 1,
                    "Vehicle"               : 2,
                    "Parking"               : 3,
                    "PublicTransport"       : 4,
                    "TransportVehicle"      : 5}
    vehicle_type = {"None"                  : 0,
                    "Car"                   : 1,
                    "Train"                 : 2,
                    "Tram"                  : 3,
                    "Metro"                 : 4,
                    "Bicycle"               : 5,
                    "Car, Tram"             : 6,
                    "Ferry"                 : 7,
                    "Ship"                  : 8,
                    "Monorail"              : 9,
                    "CableCar"              : 10,
                    "Car, Tram, Trolleybus" : 11,
                    "TrolleybusRightPole"   : 13,
                    "TrolleybusLeftPole"    : 14,
                    "Car, Trolleybus"       : 15,
                    "Plane"                 : 16,
                    "1572880"               : 17} # this is also plane
    direction_type={"None"                  : 0,
                    "Backward"              : 1,
                    "Forward"               : 2,
                    "Both"                  : 3,
                    "AvoidForward"          : 4,
                    "AvoidBackward"         : 5,
                    "Avoid"                 : 6,
                    "AvoidBoth"             : 7}
    def __init__(self, ltype, vtype, dir_, pos, width, speed):
        if (ltype in self.lane_type.keys()):
            self.type = self.lane_type[ltype]
        else:
            self.type = 0
        
        if (vtype in self.vehicle_type.keys()):
            self.vtype = self.vehicle_type[vtype]
        else:
            self.vtype = 0

        if (dir_ in self.direction_type.keys()):
            self.dir = self.direction_type[dir_]
        else:
            self.dir = 0

        self.pos = float(pos)
        self.width = float(pos)
        self.speed = float(speed)


class SegmentType(object):
    seg_name_dict = {}
    Other = 0
    TrainTrack = 1
    Street = 2
    MetroTrack = 3
    Highway = 4
    PedestrianPath = 5
    Quay = 6
    PedestrianStreet = 7
    Tram = 8
    Runway = 9
    Taxiway = 10

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        elif other.__class__ is int:
            return self.value < other
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        elif other.__class__ is int:
            return self.value > other
        return NotImplemented

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        elif other.__class__ is int:
            return self.value == other
        return NotImplemented


    def __init__(self, type_name, icls):
        is_highway = self.seg_name_dict[type_name][0]
        lanes = self.seg_name_dict[type_name][1]
        self.has_tram = False
        self.only_tram = False
        self.bike_lane = False
        # is it train track?
        if (re.match("^(?=.*train)(?=.*track).*$", icls.lower())):
            self.value = SegmentType.TrainTrack
        # is it pedestrian street?
        elif(re.match("^(?=.*pedestrian)(?=(.*street)|(.*road)).*$", \
                icls.lower())):
            self.value = SegmentType.PedestrianStreet
            self.find_st_property(lanes)
        # is it pedestrian path?
        elif (re.match("^(.*pedestrian).*$", icls.lower())):
            self.value = SegmentType.PedestrianPath
        # is it highway?
        elif is_highway:
            self.value = SegmentType.Highway
        # is it street (road)?
        elif (re.match("^(.*road)|(.*street)|(.*alley)|(.*highway)|(.*next).*$", \
                icls.lower())):
            self.value = SegmentType.Street
            self.find_st_property(lanes)
        # is it metro track?
        elif (re.match("^(?=.*metro)(?=.*track).*$", icls.lower())):
            self.value = SegmentType.MetroTrack
        # is it quay
        elif (re.match("^(.*quay).*$", icls.lower())):
            self.value = SegmentType.Quay
        # is it tram
        elif (re.match("^(.*tram).*$", icls.lower())):
            self.value = SegmentType.Tram
        # is it runway  ; sorry for the confusing comprehension, its just checking if any lane carrys plane
        elif (len([1 for lane in lanes if lane.vtype == SegmentLane.vehicle_type["Plane"]]) > 0): 
            self.value = SegmentType.Runway
        # is it taxiway
        elif (len([1 for lane in lanes if lane.vtype == SegmentLane.vehicle_type["1572880"]]) > 0):
            self.value = SegmentType.Taxiway
        else:
            self.value = SegmentType.Other

    
    def find_st_property(self, lanes):
        for lane in lanes:
            if (lane.vtype == SegmentLane.vehicle_type["Tram"] \
                or lane.vtype == SegmentLane.vehicle_type["Car, Tram"] \
                or lane.vtype == SegmentLane.vehicle_type["Car, Tram, Trolleybus"]):
                self.has_tram = True
            if (lane.vtype == SegmentLane.vehicle_type["Bicycle"]):
                self.bike_lane = True


class Segment(object):

    def __init__(self, id, sn, en, icls, width, iner_name):
        self.id = int(id)
        self.sn = int(sn)
        self.en = int(en)
        self.icls = icls
        self.width = float(width)
        self.internal_name = iner_name

        self.name = ""
        self.points = []

        self.find_seg_type()
        
    
    def add_name(self, name):
        self.name = name

    
    def add_point(self, x, y, z):
        x_norm, y_norm, z_norm = self.remap_coordinate(float(x), float(y), float(z))
        self.points.append([x_norm, y_norm, z_norm])


    def remap_coordinate(self, x, y, z):
        # How to remap coordnate: ONLY x and z
        # from [-32768, 32768] to [0.0, 1.0]
        x_out = (x + MAX_COOR) / (MAX_COOR * 2)
        z_out = (z - MAX_COOR) / (MAX_COOR * 2)
        y_out = y
        return x_out, y_out, z_out

    # Clasify segment to different type. this is mostly hard coded 
    # and probably needs update frequently
    def find_seg_type(self):
        self.seg_type = SegmentType(self.internal_name, self.icls)

        