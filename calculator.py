import sys
from osrsbox import items_api
from osrsbox import monsters_api
from osrsbox import prayers_api
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
__items = items_api.load()
__monsters = monsters_api.load()
__prayers = prayers_api.load()

# Initialize app
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(100, 100, 280, 80)
window.move(60, 15)

title = QLabel('<h1>Hello World!</h1>', parent=window)
title.move(60, 15)
window.show()

sys.exit(app.exec_())