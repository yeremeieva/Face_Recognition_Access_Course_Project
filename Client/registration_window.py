# registration_window.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

class RegistrationWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.gate = main_window.gate

        self.setWindowTitle("Register New Face")
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

        # Layout
        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(QLabel("Gender:"))
        form_layout.addWidget(self.gender_combo)
        form_layout.addWidget(QLabel("Age:"))
        form_layout.addWidget(self.age_edit)
        form_layout.addWidget(QLabel("Phone:"))
        form_layout.addWidget(self.phone_edit)
        form_layout.addWidget(QLabel("Position:"))
        form_layout.addWidget(self.position_combo)
        form_layout.addWidget(self.save_button)
        form_layout.addWidget(self.return_button)

        self.layout.addLayout(form_layout)

        self.return_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.register_button_clicked)

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