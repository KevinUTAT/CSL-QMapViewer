import xml.etree.ElementTree as ET
from terrains import Terrains
from segment import Segment, SegmentType
from building import Building, BuildingType


# top level data strcture to store all of the city data from the *.cslmap file
class CityData(object):

    def __init__(self, path2xml):
        self.load_xml(path2xml)
        self.get_terrains()
        self.get_networks()
        self.get_buildings()

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
        
        # load all segments
        self.segs_dict = {}
        self.highway_segs = []
        self.street_segs = []
        self.train_track_segs = []
        self.metro_track_segs = []
        self.pedestrian_path_segs = []
        self.quay_segs = []
        self.pedestrian_st_segs = []
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
            else:
                self.other_segs.append(int(seg.attrib['id']))

        print(len(self.segs_dict), "segments")

    # load buildings
    def get_buildings(self):
        srvs = {}
        self.building_dict = {}
        self.res_buils = []
        self.com_buils = []
        self.ind_buils = []
        self.off_buils = []
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
            else:
                self.other_buils.append(int(buil.attrib['id']))

        print(len(self.building_dict), "buildings")
        
            



# testbench
if __name__ == '__main__':
    test_city = CityData("testmap.cslmap")