import xml.etree.ElementTree as ET
from terrains import Terrains
from segment import Segment, SegmentType, SegmentLane
from building import Building, BuildingType
from node import Node
from transit import TransitLine


# top level data strcture to store all the city data from the *.cslmap file
class CityData(object):

    def __init__(self, path2xml):
        self.load_xml(path2xml)

    # load the xml file (*.cslmap)
    def load_xml(self, path2xml):
        self.city_data_tree = ET.parse(path2xml)
        self.city_root = self.city_data_tree.getroot()
        # print(self.city_data_tree.getroot().findall('Terrains').tag)

    # load terrain data from root
    def get_terrains(self):
        # apparently the SeaLevel is sometimes not a natural number, e.g. "207.328",
        # so it needs to be split after the dot for int() to work
        sea_level = int(self.city_root.find('SeaLevel').text.split('.')[0])
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
        self.monorail_track_segs = []
        self.metro_track_segs = []
        self.pedestrian_path_segs = []
        self.quay_segs = []
        self.pedestrian_st_segs = []
        self.tram_segs = []
        self.airport_segs = []
        self.concourse_segs= []
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
            elif (new_seg.seg_type == SegmentType.MonorailTrack):
                self.monorail_track_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.MetroTrack):
                self.metro_track_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.Tram):
                self.tram_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.Runway \
                    or new_seg.seg_type == SegmentType.Taxiway):
                self.airport_segs.append(int(seg.attrib['id']))
            elif (new_seg.seg_type == SegmentType.Concourse):
                self.concourse_segs.append(int(seg.attrib['id']))
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
            # id = id (unique Number),
            # name = name (e.g. "H3 4x4 Office07"),
            # srv = category (e.g. "Office", "Residential", "PlayerEducation", etc.),
            # subsrv = subcategory (e.g. "ResidentialHigh", "OfficeGeneric", "PlayerEducationLiberalArts"),
            # icls = category (e.g. "Office - Level 3", "High Residential - Level5")
            new_building = Building(buil.attrib['id'], buil.attrib['name'], buil.attrib['srv'], \
                                    buil.attrib['subsrv'], buil.attrib['icls'])
            if ('subb' in  buil.attrib.keys()):  # sub-building
                new_building.add_child(buil.attrib['subb'])
            if ('prntb' in buil.attrib.keys()):  # parent-building
                new_building.add_parent(buil.attrib['prntb'])
            if ('myname' in buil.attrib.keys()):  # custom name by player
                new_building.add_myname(buil.attrib['myname'])

            for point in buil.find('Points').findall('P'):  # location of building
                new_building.add_point(point.attrib['x'], point.attrib['y'], point.attrib['z'])

            self.building_dict[int(buil.attrib['id'])] = new_building

            # simplified via ChatGPT
            # maps BuildingType to the list attribute
            building_type_map = {
                BuildingType.Residential: self.res_buils,
                BuildingType.Commercial: self.com_buils,
                BuildingType.Industrial: self.ind_buils,
                BuildingType.Office: self.off_buils,
                BuildingType.Beautification: self.beauti_buils,
                BuildingType.Education: self.edu_buils,
                BuildingType.PublicTransport: self.transit_buils,
                BuildingType.Police: self.police_buils,
                BuildingType.Electricity: self.elec_buils,
                BuildingType.Fire: self.fire_buils,
                BuildingType.Road: self.road_buils,
                BuildingType.ServicePoint: self.serv_buils,
                BuildingType.Monument: self.mont_buils,
                BuildingType.HealthCare: self.health_buils,
                BuildingType.VarsitySports: self.sport_buils,
                BuildingType.Water: self.water_buils,
                BuildingType.Garbage: self.garb_buils,
                BuildingType.Disaster: self.disaster_buils,
                BuildingType.Fishing: self.fish_buils
            }

            # get the appropriate list attribute based on the new_building.btype, then append the id to selected list
            building_type_map.get(new_building.btype, self.other_buils).append(int(buil.attrib['id']))

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