# gate.py
import cv2
from threading import Thread
import requests
import time

from main_window import MainWindow
from Facenet import Facenet

class Gate:
    def __init__(self, door_id, direction, positions, door_type, location, url):
        self.door_id = door_id
        self.direction = direction
        self.positions = positions
        self.door_type = door_type
        self.location = location
        self.url = url

        self.cap = cv2.VideoCapture(0)

        self.facenet = Facenet(self)
        self.widget = MainWindow(self)

        door_details = {
            'door_id': self.door_id,
            'direction': self.direction,
            'door_access': self.positions[0],
            'location': self.location
        }
        self.person_id_counter = 0
        self.record_id_counter = requests.get(f"{self.url}/get_last_record_id").json()

        returnData = requests.post(f"{self.url}/add_door", json=door_details)
        
        self.facenet.people_database = self.load_people()
        self.widget.show()

    def run(self):
        last_record_time = 0  # Keep track of the last record time
        last_box_time = 0    # Last time the box was updated
        record_interval = 1  # Interval in seconds for records
        box_interval = 0.1   # Interval in seconds for box updates
        box = None           # Store last box coordinates
        person_details = None # Store last known/unknown person details

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                current_time = time.time()

                # Update face detection at specified interval
                if current_time - last_box_time > box_interval:
                    is_known, person, box, feature_vector = self.facenet.detect_and_compare_faces(frame)
                    last_box_time = current_time  # Update the last box update time
                    if box is not None:
                        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                    person_details = (is_known, person)

                # Draw the last known box and details
                if box is not None:
                    x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                    if person_details[0]:  # is_known is True
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box for known person
                        cv2.putText(frame, person_details[1]['name'], (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                        # Handle recording known person access
                        if current_time - last_record_time > record_interval:
                            t = Thread(target=self.add_record, args=(person_details[1]['person_id'], person_details[1]['position'], frame))
                            t.setDaemon(True)
                            t.start()
                            last_record_time = current_time  # Update the last record time
                    else:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red box for unknown person
                        cv2.putText(frame, "Unknown", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                        if current_time - last_record_time > record_interval:
                            t = Thread(target=self.add_record, args=(-1, '', frame))
                            t.setDaemon(True)
                            t.start()
                            last_record_time = current_time

                self.widget.display_image(frame)
            else:
                print("Failed to capture face from camera.")
                break

        self.cap.release()
        print("Camera feed stopped.")

    def access_logic(self, person_access):
        """
        Determine if the detected person has access based on the door type.
        'Admin' doors allow both 'Admin' and 'Worker' access.
        'Worker' doors only allow 'Worker' access.
        """
        if self.door_type == 'Worker':
            return person_access == 'Worker' or person_access == 'Admin'
        elif self.door_type == 'Admin':
            return person_access == 'Admin'
        return False  # Default to no access if the position does not match

    def add_record(self, person_id, person_access, face):
        bool_access = self.access_logic(person_access)

        self.record_id_counter += 1
        record_details = {
            'record_id': self.record_id_counter,
            'access': bool_access,
            'door_id': self.door_id,
            'direction': self.direction,
            'person_id': person_id
        }
        
        returnData = requests.post(f"{self.url}/add_record", json=record_details)

    def add_person(self, name, surname, gender, age, phone, position, face, feature_vector):

        self.person_id_counter += 1
        person_details = {
            'person_id': self.person_id_counter,
            'name': name,
            'surname': surname,
            'gender': gender,
            'age': int(age),
            'phone': phone,
            'position': position,
            'image': face.tolist(),
            'feature_vector': feature_vector.tolist()
        }
        
        returnData = requests.post(f"{self.url}/add_person", json=person_details)
        self.facenet.people_database.append(person_details)

    def load_people(self):
            response = requests.get(f"{self.url}/get_people")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to load people from the server: {response.text}")
                return []
            
    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
