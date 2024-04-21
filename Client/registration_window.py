# registration_window.py
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from PySide6.QtCore import Qt


class RegistrationWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.gate = main_window.gate

        self.setWindowTitle("Register New Face")
        self.setMinimumSize(300, 300)
        self.background_image = QImage('background.png')
        if self.background_image.isNull():
            print("Failed to load background.png")
        self.layout = QVBoxLayout(self)

        self.name_edit = QLineEdit()
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        self.age_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.position_combo = QComboBox()
        self.position_combo.addItems(self.main_window.gate.positions)
        self.save_button = QPushButton("Save")
        self.return_button = QPushButton("Return to Main Window")
        # styles for buttons
        button_style = ("QPushButton { background-color: rgba(32, 29, 41, 255); color: white; "
                        "font-size: 14px; padding: 5px 10px; }")
        self.save_button.setStyleSheet(button_style)
        self.return_button.setStyleSheet(button_style)

        # Labels
        form_layout = QVBoxLayout()
        name_label = QLabel("Name:")
        gender_label = QLabel("Gender:")
        age_label = QLabel("Age:")
        phone_label = QLabel("Phone:")
        position_label = QLabel("Position:")

        # label style
        label_style = "color: white; font-size: 14px; background: transparent;"
        name_label.setStyleSheet(label_style)
        gender_label.setStyleSheet(label_style)
        age_label.setStyleSheet(label_style)
        phone_label.setStyleSheet(label_style)
        position_label.setStyleSheet(label_style)

        combo_box_style = "QComboBox { font-family: 'Calibri'; font-size: 12pt; }"
        self.gender_combo.setStyleSheet(combo_box_style)
        self.position_combo.setStyleSheet(combo_box_style)

        # Layout
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(gender_label)
        form_layout.addWidget(self.gender_combo)
        form_layout.addWidget(age_label)
        form_layout.addWidget(self.age_edit)
        form_layout.addWidget(phone_label)
        form_layout.addWidget(self.phone_edit)
        form_layout.addWidget(position_label)
        form_layout.addWidget(self.position_combo)
        form_layout.addWidget(self.save_button)
        form_layout.addWidget(self.return_button)

        self.layout.addLayout(form_layout)

        self.return_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.register_button_clicked)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.2)  # Set the opacity of the background
        painter.drawImage(self.rect(), self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding))

    def register_button_clicked(self):
        ret, current_frame = self.gate.cap.read()
        is_known, person, box, feature_vector = self.gate.facenet.detect_and_compare_faces(current_frame)
        if is_known:
            QMessageBox.warning(self, "Error", "This face is already registered!")
        else:
            if box is not None:
                name = self.name_edit.text()
                gender = self.gender_combo.currentText()
                age = self.age_edit.text()
                phone = self.phone_edit.text()
                position = self.position_combo.currentText()

                face = current_frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

                self.gate.add_person(name, gender, age, phone, position, face, feature_vector)
                self.main_window.update_face_count()
                QMessageBox.information(self, "Success", "New face registered successfully!")
            else:
                QMessageBox.warning(self, "Failed", "No face detected. Try again.")