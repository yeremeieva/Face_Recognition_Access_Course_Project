# main.py
import sys
from PySide6.QtWidgets import QApplication

from Gate import Gate
from threading import Thread

if __name__ == "__main__":
    app = QApplication(sys.argv)
    door_id = 0
    direction = 'Out'
    location = 'Entrance'
    positions = ["Admin", "Worker"]
    door_type = positions[1]

    gate = Gate(door_id, direction, positions, door_type, location, url='http://localhost:5555')
    Thread(target=gate.run).start()

    sys.exit(app.exec())
