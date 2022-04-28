import sys
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtWidgets import QLabel
#from PyQt5.QtWidgets import QWidget

#Initialise application
app = QApplication(sys.argv)

#Set window size
main_window = QWidget()
main_window.setWindowTitle("F1 Stats")
main_window.setGeometry(200, 150, 1000, 800)

#Header section
title = QLabel("<h1>F1 Stats App</h1>", parent=main_window)
title.move(30, 15)

explanation = QLabel("<p>Lorem ipsum</p>", parent=main_window)
explanation.move(30, 60)

#Driver section
driver_section_title = QLabel("<h3>Driver Stats</h3>", parent=main_window)
driver_section_title.move(30, 110)

driver_dropdown = QComboBox(parent=main_window)
driver_dropdown.addItems(["Lewis Hamilton", "Max Verstappen", "Charles Leclerc"])
driver_dropdown.move(30, 140)

year_dropdown = QComboBox(parent=main_window)
year_dropdown.addItems(["All Time", "2022", "2021"])
year_dropdown.move(170, 140)

#Schedule event
main_window.show()

#Run event
sys.exit(app.exec_())
