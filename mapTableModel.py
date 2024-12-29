from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QFont, QColor
from collections import OrderedDict

# Base class for all table model use in detail table
# The detail table only have 1 colum dispaly name and data
class MapTableModel(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_dict = OrderedDict()
        self.header_str = "Detail"


    def rowCount(self, parent=QModelIndex()):
        # Return the number of rows in the data
        return len(self.data_dict) * 2

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()

        if role == Qt.DisplayRole:
            # odd, display data
            if (row % 2 == 1):
                return str(list(self.data_dict.items())[int(row / 2)][1])
            # even, display lable name
            else:
                return str(list(self.data_dict.items())[int(row / 2)][0])
        elif role == Qt.FontRole:
            if row % 2 == 0:  # Bold text for lable rows
                font = QFont()
                font.setBold(True)
                return font
        elif role == Qt.BackgroundRole:
            if row % 2 == 0:  # Background color for lable rows
                return QColor("#999999")  # Light gray color
            

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header_str
            

class BuildingTableModel(MapTableModel):

    def __init__(self, building, parent=None):
        super().__init__(parent)

        self.header_str = "Building Details"

        self.data_dict["Name"]          = building.name
        self.data_dict["Asset Name"]    = building.internal_name
        self.data_dict["Type"]          = str(building.btype)
        self.data_dict["ID"]            = building.id
        self.data_dict["SRV"]           = building.srv
        self.data_dict["subSRV"]        = building.subsrv
        self.data_dict["ICLS"]          = building.icls