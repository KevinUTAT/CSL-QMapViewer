from enum import Enum

MAX_COOR = 8648

class SegmentType(Enum):
    Other = 0
    TrainTrack = 1
    Street = 2
    MetroTrack = 3
    Highway = 4
    PedestrianPath = 5
    Quay = 6

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


class Segment(object):

    def __init__(self, id, sn, en, icls, width):
        self.id = int(id)
        self.sn = int(sn)
        self.en = int(en)
        self.icls = icls
        self.width = float(width)

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

    def find_seg_type(self):
        # is it train track?
        if ('train' in self.icls.lower()) \
            and ('track' in self.icls.lower()):
            self.seg_type = SegmentType.TrainTrack
        # is it street (road)?
        elif ('road' in self.icls.lower()) \
            or ('street' in self.icls.lower()):
            self.seg_type = SegmentType.Street
        # is it metro track?
        elif ('metro' in self.icls.lower()) \
            and ('track' in self.icls.lower()):
            self.seg_type = SegmentType.MetroTrack
        # is it highway?
        elif ('highway' in self.icls.lower()):
            self.seg_type = SegmentType.Highway
        else:
            self.seg_type = SegmentType.Other
        
        