import xml.etree.ElementTree as ET
from terrains import Terrains
from segment import Segment


# top level data strcture to store all of the city data from the *.cslmap file
class CityData(object):

    def __init__(self, path2xml):
        self.load_xml(path2xml)
        self.get_terrains()
        self.get_networks()

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
        print("Loading segments: ", end='')
        seg_root = self.city_root.find('Segments')
        for seg in seg_root.findall('Seg'):
            new_seg = Segment(seg.attrib['id'], seg.attrib['sn'], seg.attrib['en'], \
                            seg.attrib['icls'], seg.attrib['width'])

            if (new_name := seg.find('CustomName')) is not None:
                new_seg.add_name(new_name)

            for point in seg.find('Points').findall('P'):
                new_seg.add_point(point.attrib['x'], point.attrib['y'], point.attrib['z'])

            self.segs_dict[int(seg.attrib['id'])] = new_seg
        print(len(self.segs_dict), "segments")


# testbench
if __name__ == '__main__':
    test_city = CityData("testmap.cslmap")