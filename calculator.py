import sys
from osrsbox import items_api
from osrsbox import monsters_api
from osrsbox import prayers_api
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QGridLayout, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor
__items = items_api.load()
__equipment = list(filter(lambda item: item.equipable_by_player, __items))
__weapons = list(filter(lambda item: item.equipable_weapon, __items))
__equipmentSlots = {
    "head": list(filter(lambda equipment: equipment.equipment.slot == "head", __equipment)),
    "legs": list(filter(lambda equipment: equipment.equipment.slot == "legs", __equipment)),
    "neck": list(filter(lambda equipment: equipment.equipment.slot == "neck", __equipment)),
    "feet": list(filter(lambda equipment: equipment.equipment.slot == "feet", __equipment)),
    "cape": list(filter(lambda equipment: equipment.equipment.slot == "cape", __equipment)),
    "body": list(filter(lambda equipment: equipment.equipment.slot == "body", __equipment)),
    "shield": list(filter(lambda equipment: equipment.equipment.slot == "shield", __equipment)),
    "ring": list(filter(lambda equipment: equipment.equipment.slot == "ring", __equipment)),
    "ammunition": list(filter(lambda equipment: equipment.equipment.slot == "ammo", __equipment)),
    "shield": list(filter(lambda equipment: equipment.equipment.slot == "shield", __equipment)),
    "2hWeapon": list(filter(lambda weapon: weapon.equipment.slot == "2h", __weapons)),
    "1hWeapon": list(filter(lambda weapon: weapon.equipment.slot == "weapon", __weapons)),
}
__monsters = monsters_api.load()
__prayers = prayers_api.load()
__skills = ["Attack", "Strength", "Defence", "Ranged", "Prayer", "Magic", "Runecraft", "Hitpoints", "Crafting", "Mining",
"Smithing", "Fishing", "Cooking", "Firemaking", "Woodcutting", "Agility", "Herblore", "Thieving", "Fletching", "Slayer",
"Farming", "Construction", "Hunter"]

class Skill():
    __xpLevels = [0, 83, 174, 276, 388, 512, 650, 801, 969, 1154, 1358, 1584, 1833, 2107, 2411, 2746, 3115, 3523, 3973, 4470,
    5018, 5624, 6291, 7028, 7842, 8740, 9730, 10824, 12031, 13363, 14833, 16456, 18247, 20224, 22406, 24815, 27473, 30408, 33648, 37224,
    41171, 45529, 50339, 55649, 61512, 67983, 75127, 83014, 91721, 101333, 111945, 123660, 136594, 150872, 136594, 150872, 166636, 184040, 203254, 224466, 247886, 273742,
    302288, 333804, 368599, 407015, 449428, 496254, 547953, 605032, 668051, 737627, 814445, 899257, 992895, 1096278, 1210421, 1336443, 1475581, 1629200, 1798808, 1986068,
    2192818, 2421087, 2673114, 2951373, 3258594, 3597792, 3972294, 43842295, 5346332, 5902831, 6517253, 7195629, 7944614, 8771558, 9684577, 10692629, 11805606, 13034431]
    def __init__(self, data):
        self.name = data.name
        self.xp = data.xp
        self.level = self.calculateLevel(self)
    def calculateLevel(self):
        for level in range(1, 99):
            if self.xp <= __xpLevels[level-1]:
                return level

class Equipment():
    def __init__(self, data):
        self.name = data.name
        self.slot = data.slot
        self.stats = {
            "attackStab": data.attackStab,
            "attackSlash": data.attackSlash,
            "attackCrush": data.attackCrush,
            "attackMagic": data.attackMagic,
            "attackRanged": data.attackRanged,
            "defenceStab": data.defenceStab,
            "defenceSlash": data.defenceSlash,
            "defenceCrush": data.defenceCrush,
            "defenceMagic": data.defenceMagic,
            "defenceRanged": data.defenceRanged,
            "meleeStrength": data.meleeStrength,
            "rangedStrength": data.rangedStrength,
            "magicDamage": data.magicDamage,
            "prayer": data.prayer,
        }
        self.requirements = data.requirements

class Player():
    def __init__(self, data):
        self.name = data.name
        self.skills = {}
        for skill in data.skills:
            setattr(self.skills, skill.name, Skill({"name": skill.name, "xp": skill.xp}))
        self.gear = {
            "head": None,
            "necklace": None,
            "body": None,
            "legs": None,
            "feet": None,
            "hands": None,
            "cape": None,
            "ammo": None,
            "shield": None,
            "weapon": None,
        }
    def addEquipment(self, equipment):
        setattr(self.gear, equipment.name, equipment)
    def removeEquipment(self, equipment):
        setattr(self.gear, equipment.name, None)

class EquipmentDataModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.load_data(data)

    def load_data(self, data):
        self.input_dates = data[0].values
        self.input_magnitudes = data[1].values

        self.column_count = 2
        self.row_count = len(self.input_magnitudes)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return ("Date", "Magnitude")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            if column == 0:
                date = self.input_dates[row].toPython()
                return str(date)[:-3]
            elif column == 1:
                magnitude = self.input_magnitudes[row]
                return f"{magnitude:.2f}"
        elif role == Qt.BackgroundRole:
            return QColor(Qt.white)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

        return None

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUI__()

    def __initUI__(self):
        self.setWindowTitle('OSRS DPS Calculator')
        self.setGeometry(100, 100, 500, 500)
        geometry = self.frameGeometry()
        geometry.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(geometry.topLeft())
        layout = QGridLayout()
        layout.addWidget(QLabel('<h1>DPS Calculator</h1>'), 0, 1)
        layout.addWidget(QLabel('<h2>Username:</h2>'), 1, 1)
        layout.addWidget(QLineEdit(), 1, 2)

        gearLayout = QGridLayout()
        self.setLayout(layout)

# Initialize app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())