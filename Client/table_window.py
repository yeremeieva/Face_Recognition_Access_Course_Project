from PySide6.QtCore import QUrl
from PySide6.QtGui import QImage, QPainter, QFont
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QPushButton, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
import requests


class FacesTableWindow(QWidget):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.setWindowTitle("Access Records")
        # set background image
        self.background_image = QImage('background.png')
        if self.background_image.isNull():
            print("Failed to load background.png")
        self.setMinimumSize(400, 400)
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # RecordID, RecordTime, Access, DoorID, PersonID
        self.table.setHorizontalHeaderLabels(['RecordID', 'RecordTime', 'Access', 'DoorID', 'PersonID'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Set slightly transparent background and font for the table
        self.table.setStyleSheet("background: transparent;")
        font = QFont("Times New Roman", 12)
        self.table.setFont(font)
        # layout
        self.layout.addWidget(self.table)
        self.return_button = QPushButton("Return")

        # styles for buttons
        button_style = ("QPushButton { background-color: rgba(32, 29, 41, 255); color: white; "
                        "font-size: 14px; padding: 5px 10px; }")
        self.return_button.setStyleSheet(button_style)

        self.return_button.clicked.connect(self.main_window.return_to_main)
        self.layout.addWidget(self.return_button)

        self.populate_table()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.2)  # Set the opacity of the background
        painter.drawImage(self.rect(), self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding))

    def populate_table(self):
        response = requests.get(f"{self.main_window.gate.url}/get_records")
        if response.status_code == 200:
            records = response.json()

            self.table.setRowCount(len(records))
            for row_index, record in enumerate(records):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(record['record_id'])))
                self.table.setItem(row_index, 1, QTableWidgetItem(record['record_time']))
                self.table.setItem(row_index, 2, QTableWidgetItem('Yes' if record['access'] else 'No'))
                self.table.setItem(row_index, 3, QTableWidgetItem(str(record['door_id'])))
                self.table.setItem(row_index, 4, QTableWidgetItem(str(record['person_id'])))
        else:
            print(f"Failed to fetch records: {response.text}")
