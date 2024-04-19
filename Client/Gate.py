import json

import cv2
import requests
from PySide6 import QtGui


class Gate:
    def __init__(self, widget, door_id, direction, url):
        self.widget = widget
        self.door_id = door_id
        self.direction = direction
        self.url = url
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def register(self, frame, id, name):
        res = {
            "rgb_frame": str(frame.tolist()),
            "id": id,
            "name": name,
        }
        returnData = requests.post(f"{self.url}/register", json=res)
        return returnData.text

    def run(self):
        ret = False
        frame = None
        while not ret:
            ret, frame = self.cap.read()
        backGround = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                continue
            change = False

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(backGround, gray)
            diff = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            diff = cv2.dilate(diff, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4)), iterations=2)
            contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            show_img = frame.copy()

            for c in contours:
                if cv2.contourArea(c) < 1500:
                    continue
                change = True
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(show_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if not change:
                backGround = gray
            else:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
                res = {
                    "rgb_frame": str(small_frame.tolist()),
                    "door_id": self.door_id,
                    "direction": self.direction,
                }
                response = requests.post(f"{self.url}/recognize", json=res)
                ids, names, boxes = json.loads(response.text)
                for i in range(len(boxes)):
                    x1 = int(boxes[i][0] * 4)
                    y1 = int(boxes[i][1] * 4)
                    x2 = int(boxes[i][2] * 4)
                    y2 = int(boxes[i][3] * 4)

                    cv2.rectangle(rgb_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(rgb_frame, names[i], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

                height, width, channel = rgb_frame.shape
                bytes_per_line = 3 * width
                q_img = QtGui.QImage(rgb_frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
                self.widget.ui.imgLabel.setPixmap(QtGui.QPixmap(q_img))
                self.widget.ui.namelabel_2.setText(names[0])
                self.widget.ui.idlabel.setText(ids[0])
                self.widget.ui.statuslabel_2.setText(response.headers['direction'])
                self.widget.ui.timelabel_3.setText(response.headers['time'])
