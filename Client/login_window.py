from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
import requests
import base64

from threading import Thread

class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.gate = main_window.gate

        self.setWindowTitle("Login")
        self.setMinimumSize(300, 150)
        self.background_image = self.main_window.background_image
        if self.background_image.isNull():
            print("Failed to load background.png")
        self.layout = QVBoxLayout(self)

        # Styles for labels and buttons
        button_style = "QPushButton { background-color: rgba(32, 29, 41, 255); color: white; font-size: 14px; padding: 5px 10px; }"
        label_style = "color: white; font-size: 14px; background: transparent;"

        # Labels
        username_label = QLabel("Username:")
        password_label = QLabel("Password:")
        username_label.setStyleSheet(label_style)
        password_label.setStyleSheet(label_style)

        # Form elements
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(button_style)
        self.login_button.clicked.connect(self.login_button_clicked)

        form_layout = QVBoxLayout()

        # Layout
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.login_button)

        self.layout.addLayout(form_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.2)  # Set the opacity of the background
        painter.drawImage(self.rect(), self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding))

    def closeEvent(self, event):
        self.main_window.login_window = None

    def login_button_clicked(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        encrypted_password = self.encrypt(password)

        if not username or not password:
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return
        
        response = requests.post(f"{self.gate.url}/login", json={'username': username, 'password': encrypted_password})
        if response.status_code == 200:
            result = response.json()
            result_password = result['password']

            if result_password:
                decrypted_password = self.decrypt(result_password)
                if decrypted_password != password:
                    QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
                    return

                self.main_window.toggle_visibility(True)
                QMessageBox.information(self, "Login Successful", "You have successfully logged in.")
                self.close()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
        else:
            print(f"Failed to fetch records: {response.text}")
        
    def encrypt(self, password):
        encoded_bytes = base64.b64encode(password.encode('utf-8'))
        encoded_password = encoded_bytes.decode('utf-8')
        return encoded_password
    
    def decrypt(self, password):
        decoded_bytes = base64.b64decode(password.encode('utf-8'))
        decoded_password = decoded_bytes.decode('utf-8')
        return decoded_password
