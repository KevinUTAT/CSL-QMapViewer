import xml.etree.ElementTree as ET
from terrains import Terrains


# top level data strcture to store all of the city data from the *.cslmap file
class CityData(object):

    def __init__(self, path2xml):
        self.load_xml(path2xml)
        self.get_terrains()

    # load the xml file (*.cslmap)
    def load_xml(self, path2xml):
        self.city_data_tree = ET.parse(path2xml)
        self.city_root = self.city_data_tree.getroot()
        # print(self.city_data_tree.getroot().findall('Terrains').tag)

    # load terrain data from root
    def get_terrains(self):
        sea_level = int(self.city_root.find('SeaLevel').text)
        self.terrains = Terrains(self.city_root.find('Terrains').find('Ter').text, sea_level)


# testbench
if __name__ == '__main__':
    test_city = CityData("testmap.cslmap")