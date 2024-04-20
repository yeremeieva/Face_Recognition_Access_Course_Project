# main_window.py
import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QTimer, QDateTime, Qt

from registration_window import RegistrationWindow
from table_window import FacesTableWindow

class MainWindow(QMainWindow):
    def __init__(self, gate):
        super().__init__()
        self.gate = gate

        self.setWindowTitle("Face Detection System")
        self._initUI()

        self.registration_window = None  

    def open_registration_window(self):
        if not self.registration_window:
            self.registration_window = RegistrationWindow(self)
        self.registration_window.show()

    def _initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Camera display
        self.image_label = QLabel("Camera feed will appear here")
        self.image_label.setFixedSize(640, 480)
        layout.addWidget(self.image_label)

        # Right side panel
        right_panel = QVBoxLayout()
        self.door_id_label = QLabel(f"Door ID: {self.gate.door_id}")
        self.direction_label = QLabel(f"Direction: {self.gate.direction}")
        self.face_count_label = QLabel(f"Saved Faces: {len(self.gate.facenet.people_database)}")
        self.time_label = QLabel("Time: --:--")
        self.update_time()
        
        self.record_button = QPushButton("Record", self)
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.open_registration_window)
        self.record_button.clicked.connect(self.on_record)

        right_panel.addWidget(self.door_id_label)
        right_panel.addWidget(self.direction_label)
        right_panel.addWidget(self.face_count_label)
        right_panel.addWidget(self.time_label)
        right_panel.addWidget(self.record_button)
        right_panel.addWidget(self.register_button)
        layout.addLayout(right_panel)

        # Timer for updating time
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # Update every second

    def on_record(self):
            self.hide()  # Hide the main window
            self.faces_table_window = FacesTableWindow(self)
            self.faces_table_window.show()

    def return_to_main(self):
            self.faces_table_window.close()
            self.show()

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.time_label.setText(f"Time: {current_time}")

    def update_face_count(self):
        self.face_count_label.setText(f"Saved Faces: {len(self.gate.facenet.people_database)}")

    def display_image(self, frame):
        # Convert image to QPixmap and display it
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qt_image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
