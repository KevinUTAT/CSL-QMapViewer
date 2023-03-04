from map_util import MAX_COOR, map_coor_2_normalized

class TransitType(object):
    Other = 0
    Bus = 1
    Tram = 2

class TransitLine(object):
    def __init__(self, line_id, name, t_type, r, g, b):
        self.id = int(line_id)
        self.name = name
        self.type = TransitType.Other
        self.r = r
        self.g = g 
        self.b = b 

        self.__find_transit_type(t_type)
        self.stops = []


    def __find_transit_type(self, type_str):
        if (type_str == "Bus"):
            self.type = TransitType.Bus
        elif (type_str == "Tram"):
            self.type = TransitType.Tram

    
    def add_stop(self, node_id):
        self.stops.append(int(node_id))
