import xml.etree.ElementTree as ET
from terrains import Terrains
from segment import Segment, SegmentType, SegmentLane
from building import Building, BuildingType
from node import Node
from transit import TransitLine


# top level data strcture to store all of the city data from the *.cslmap file
class CityData(object):

    def __init__(self, path2xml):
        self.load_xml(path2xml)
        self.get_terrains()
        self.get_networks()
        self.get_buildings()
        self.get_transit()

    # load the xml file (*.cslmap)
    def load_xml(self, path2xml):
        self.city_data_tree = ET.parse(path2xml)
        self.city_root = self.city_data_tree.getroot()
        # print(self.city_data_tree.getroot().findall('Terrains').tag)

    # load terrain data from root
    def get_terrains(self):
        sea_level = int(self.city_root.find('SeaLevel').text)
        self.terrains = Terrains(self.city_root.find('Terrains').   \
                                find('Ter').text, sea_level)

    # load network stuff: nodes and segments
    def get_networks(self):

        self.get_nodes()
        self.get_segment_types()
        
        # load all segments
        self.segs_dict = {}
        self.highway_segs = []
        self.street_segs = []
        self.train_track_segs = []
        self.metro_track_segs = []
        self.pedestrian_path_segs = []
        self.quay_segs = []
        self.pedestrian_st_segs = []
        self.tram_segs = []
        self.other_segs = []

        print("Loading segments: ", end='')
        seg_root = self.city_root.find('Segments')
        for seg in seg_root.findall('Seg'):
            new_seg = Segment(seg.attrib['id'], seg.attrib['sn'], seg.attrib['en'], \
                            seg.attrib['icls'], seg.attrib['width'], seg.find('Name').text)

            if (new_name := seg.find('CustomName')) is not None:
                new_seg.add_name(new_name.text)

            for point in seg.find('Points').findall('P'):
                new_seg.add_point(point.attrib['x'], point.attrib['y'], point.attrib['z'])

            self.segs_dict[int(seg.attrib['id'])] = new_seg

            if (new_seg.seg_type == SegmentType.Street):
                self.street_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.PedestrianStreet):
                self.pedestrian_st_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.PedestrianPath):
                self.pedestrian_path_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.Highway):
                self.highway_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.Quay):
                self.quay_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.TrainTrack):
                self.train_track_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.MetroTrack):
                self.metro_track_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.Tram):
                self.tram_segs.append(int(seg.attrib['id']))
            else:
                self.other_segs.append(int(seg.attrib['id']))

        print(len(self.segs_dict), "segments")


    def get_segment_types(self):
        for seg_type in self.city_root.find('SegmentTypes'):
            is_highway = seg_type.attrib['highway'] == 'true'
            lanes = []
            for lane in seg_type.find('Lanes').findall('Lane'):
                new_lane = SegmentLane(lane.attrib['type'], lane.attrib['vType'], \
                                        lane.attrib['dir'], lane.attrib['pos'], \
                                        lane.attrib['width'], lane.attrib['speed'])
                lanes.append(new_lane)
            SegmentType.seg_name_dict[seg_type.attrib['name']] = [is_highway, lanes]

    
    def get_nodes(self):
        self.node_dict = {}
        print("Loading nodes: ", end='')
        for node in self.city_root.find('Nodes').findall('Node'):
            node_pos = node.find('Pos')
            new_node = Node(node.attrib['id'], node.attrib['ug'], \
                            node.attrib['og'], node.attrib['srv'], \
                            node.attrib['subsrv'], node_pos.attrib['x'], \
                            node_pos.attrib['y'], node_pos.attrib['z'])
            self.node_dict[int(node.attrib['id'])] = new_node
        print(len(self.node_dict), "nodes")
        


    # load buildings
    def get_buildings(self):
        srvs = {}
        self.building_dict = {}
        self.res_buils = []
        self.com_buils = []
        self.ind_buils = []
        self.off_buils = []
        self.beauti_buils = []
        self.edu_buils = []
        self.sport_buils = []
        self.transit_buils = []
        self.police_buils = []
        self.elec_buils = []
        self.fire_buils = []
        self.road_buils = []
        self.serv_buils = []
        self.mont_buils = []
        self.health_buils = []
        self.water_buils = []
        self.garb_buils = []
        self.disaster_buils = []
        self.fish_buils = []
        self.other_buils = []

        print("Loading building: ", end='')
        building_root = self.city_root.find('Buildings')
        for buil in building_root.findall('Buil'):
            new_building = Building(buil.attrib['id'], buil.attrib['name'], buil.attrib['srv'], \
                                    buil.attrib['subsrv'], buil.attrib['icls'])
            if ('subb' in  buil.attrib.keys()):
                new_building.add_child(buil.attrib['subb'])
            if ('prntb' in buil.attrib.keys()):
                new_building.add_parent(buil.attrib['prntb'])
            if ('myname' in buil.attrib.keys()):
                new_building.add_myname(buil.attrib['myname'])

            for point in buil.find('Points').findall('P'):
                new_building.add_point(point.attrib['x'], point.attrib['y'], point.attrib['z'])

            self.building_dict[int(buil.attrib['id'])] = new_building

            if (new_building.btype == BuildingType.Residential):
                self.res_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Commercial): 
                self.com_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Industrial):
                self.ind_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Office):
                self.off_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Beautification):
                self.beauti_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Education):
                self.edu_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.PublicTransport):
                self.transit_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Police):
                self.police_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Electricity):
                self.elec_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Fire):
                self.fire_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Road):
                self.road_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.ServicePoint):
                self.serv_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Monument):
                self.mont_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.HealthCare):
                self.health_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.VarsitySports):
                self.sport_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Water):
                self.water_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Garbage):
                self.garb_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Disaster):
                self.disaster_buils.append(int(buil.attrib['id']))
            elif (new_building.btype == BuildingType.Fishing):
                self.fish_buils.append(int(buil.attrib['id']))
            else:
                self.other_buils.append(int(buil.attrib['id']))

        print(len(self.building_dict), "buildings")
        
            
    def get_transit(self):
        self.transit_dict = {}
        print("Loading transit: ", end='')
        for line in self.city_root.find('Transports').findall('Trans'):
            line_color = line.find('color')
            new_line = TransitLine(line.attrib['id'], line.attrib['name'], \
                            line.attrib['type'], line_color.attrib['r'], \
                            line_color.attrib['g'], line_color.attrib['b'])
            for stop in line.find('Stops').findall('Stop'):
                new_line.add_stop(stop.attrib['node'])
            self.transit_dict[int(line.attrib['id'])] = new_line
        print(len(self.transit_dict), "transits")



# testbench
if __name__ == '__main__':
    test_city = CityData("testmap.cslmap")