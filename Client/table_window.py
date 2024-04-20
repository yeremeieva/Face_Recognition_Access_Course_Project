from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QPushButton, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt

import requests

class FacesTableWindow(QWidget):
    def __init__(self, main_window):
        self.main_window = main_window
        super().__init__()
        self.setWindowTitle("Access Records")
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # RecordID, RecordTime, Access, DoorID, PersonID
        self.table.setHorizontalHeaderLabels(['RecordID', 'RecordTime', 'Access', 'DoorID', 'PersonID'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.table)

        self.return_button = QPushButton("Return")
        self.return_button.clicked.connect(self.main_window.return_to_main)
        self.layout.addWidget(self.return_button)

        self.populate_table()

    def populate_table(self):
        response = requests.get(f"{self.main_window.gate.url}/get_records")
        if response.status_code == 200:
            records = response.json()

            self.table.setRowCount(len(records))
            for row_index, record in enumerate(records):
                self.table.setItem(row_index, 0, QTableWidgetItem(str(record['recordid'])))
                self.table.setItem(row_index, 1, QTableWidgetItem(record['recordtime']))
                self.table.setItem(row_index, 2, QTableWidgetItem('Yes' if record['access'] else 'No'))
                self.table.setItem(row_index, 3, QTableWidgetItem(str(record['doorid'])))
                self.table.setItem(row_index, 4, QTableWidgetItem(str(record['personid'])))
        else:
            print(f"Failed to fetch records: {response.text}")
