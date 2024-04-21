# main_window.py
import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMessageBox
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtCore import QTimer, QDateTime, Qt

from registration_window import RegistrationWindow
from table_window import FacesTableWindow
from login_window import LoginWindow


class MainWindow(QMainWindow):
    def __init__(self, gate):
        super().__init__()
        self.gate = gate

        self.setWindowTitle("Face Detection System")
        self._initUI()

        self.registration_window = None
        self.login_window = None

    def open_registration_window(self):
        if not self.registration_window:
            self.registration_window = RegistrationWindow(self)
        self.registration_window.show()

    def open_login_window(self):
        if not self.login_window:
            self.login_window = LoginWindow(self)
        self.login_window.show()

    def _initUI(self):
        central_widget = QWidget()
        # set background image
        self.background_image = QImage('Client/background.png')
        if self.background_image.isNull():
            print("Failed to load background.png")

        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        top_layout = QHBoxLayout()  # layout for elements above the date-time bar
        # Camera display
        self.image_label = QLabel("Camera feed will appear here")
        self.image_label.setFixedSize(640, 480)
        top_layout.addWidget(self.image_label)

        # Right side panel
        info_panel = QVBoxLayout()
        right_panel_widget = QWidget()
        right_panel_widget.setMaximumWidth(200)
        right_panel_widget.setMaximumHeight(200)
        right_panel_widget.setStyleSheet("""
        background-color: rgba(32, 29, 41, 255);
        border-radius: 15px;
        padding: 10px;
        """)

        right_panel = QVBoxLayout(right_panel_widget)
        self.door_id_label = QLabel(f"Door ID: \t {self.gate.door_id}")
        self.direction_label = QLabel(f"Direction: \t {self.gate.direction}")
        self.face_count_label = QLabel(f"Detected Faces: \t {len(self.gate.facenet.people_database)}")
        self.time_label = QLabel("Time: \t --:--")
        self.update_time()

        # styles for info labels on right side panel
        info_style = "color: white; font-size: 16px; background: transparent;"
        self.direction_label.setStyleSheet(info_style)
        self.door_id_label.setStyleSheet(info_style)
        self.face_count_label.setStyleSheet(info_style)
        self.time_label.setStyleSheet(info_style)

        self.record_button = QPushButton("Record", self)
        self.register_button = QPushButton("Register", self)
        self.login_button = QPushButton("Login", self)
        self.logout_button = QPushButton("Logout", self)
        self.register_button.clicked.connect(self.open_registration_window)
        self.record_button.clicked.connect(self.on_record)
        self.login_button.clicked.connect(self.open_login_window)
        self.logout_button.clicked.connect(self.on_logout)

        self.toggle_visibility(False)

        # styles for buttons
        button_style = ("QPushButton { background-color: rgba(32, 29, 41, 255); color: white; "
                        "font-size: 16px; padding: 10px 20px; }")
        self.record_button.setStyleSheet(button_style)
        self.register_button.setStyleSheet(button_style)
        self.login_button.setStyleSheet(button_style)
        self.logout_button.setStyleSheet(button_style)

        # buttons layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.register_button)

        login_layout = QHBoxLayout()
        login_layout.addWidget(self.login_button)
        login_layout.addWidget(self.logout_button)

        # right panel layout widgets
        right_panel.addWidget(self.door_id_label)
        right_panel.addWidget(self.direction_label)
        right_panel.addWidget(self.face_count_label)
        right_panel.addWidget(self.time_label)
        info_panel.addWidget(right_panel_widget)
        info_panel.addLayout(button_layout)
        info_panel.addLayout(login_layout)

        # bottom bar with date and time
        bottom_bar = QWidget()
        bottom_bar.setStyleSheet("background-color: rgba(128, 0, 128, 102);")

        status_bar = QHBoxLayout(bottom_bar)
        status_bar.setContentsMargins(0, 0, 0, 0)
        status_bar.setSpacing(0)
        self.date_label = QLabel(QDateTime.currentDateTime().toString("yyyy-MM-dd"))
        self.date_label.setStyleSheet("color: white; font-size: 16px; background: transparent;")
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: white; font-size: 16px; background: transparent;")
        status_bar.addWidget(self.date_label, 1, Qt.AlignCenter)
        status_bar.addWidget(self.time_label, 0, Qt.AlignRight)

        layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addLayout(info_panel)

        layout.addWidget(QWidget(), 1)  # Placeholder for other content
        layout.addLayout(top_layout)
        layout.addWidget(bottom_bar)

        # Timer for updating time
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)  # Update every second

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.2)  # Set the opacity of the background
        painter.drawImage(self.rect(), self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding))

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

    def on_logout(self):
        result = QMessageBox.question(self, "Logout", "Are you sure you want to logout?", QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            self.toggle_visibility(False)
            QMessageBox.information(self, "Logout", "You have successfully logged out.")
        else:
            pass
    
    def toggle_visibility(self, visible):
        self.register_button.setVisible(visible)
        self.record_button.setVisible(visible)
        self.login_button.setVisible(not visible)
        self.logout_button.setVisible(visible)