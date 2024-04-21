import json

import numpy as np
from PIL import Image
from flask import Flask
from flask import render_template, jsonify, request

import _init_paths
from FacenetModel import Facenet
from SQL.InsertProcessor import insert_processor
from SQL.QueryProcessor import query_processor
from SQL.AdminProcessor import admin_processor

facenet = Facenet()
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'time_spent':
            person_id = request.form['person_id']
            result = admin_processor.get_time_spent_by_person(person_id)
            formatted_result = format_time_spent_result(result)
            return jsonify(formatted_result)
        
        elif action == 'daily_access_report':
            result = admin_processor.get_daily_access_report()
            return jsonify([{
                "Name": row[0],
                "Surname": row[1],
                "RecordTime": str(row[2]),
                "Location": row[3],
                "Direction": row[4]
            } for row in result])

        elif action == 'denied_access_report':
            result = admin_processor.get_denied_access_report()
            return jsonify([{
                "Name": row[0],
                "Surname": row[1],
                "RecordTime": str(row[2]),
                "Location": row[3]
            } for row in result])

        if action == 'update_person_position':
            person_id = request.form['person_id']
            new_position = request.form['new_position']
            rows_affected = admin_processor.update_person_position(person_id, new_position)
            if rows_affected > 0:
                return jsonify({"success": "Position updated successfully."})
            else:
                return jsonify({"error": "No position updated, check the person ID."})

        elif action == 'list_by_position_gender':
            position = request.form['position']
            gender = request.form['gender']
            result = admin_processor.list_people_by_position_and_gender(position, gender)
            return jsonify([{
                "PersonID": row[0],
                "Name": row[1],
                "Surname": row[2],
                "Age": row[3],
                "PhoneNumber": row[4],
                "Position": row[5],
                "Gender": row[6]
            } for row in result])

    else:
        return render_template('admin.html')

def format_time_spent_result(result):
    if result:
        return [{
            "Name": row[0],
            "Surname": row[1],
            "FirstInTime": str(row[2]),
            "LatestOutTime": str(row[3]),
            "TotalTimeSpent": str(row[4])
        } for row in result]
    else:
        return {"error": "No data found"}

@app.route("/recognize", methods=['POST'])
def recognize():
    response = request.json
    rgb_frame = response["rgb_frame"]
    rgb_frame = json.loads(rgb_frame)
    rbg_image = Image.fromarray(np.uint8(rgb_frame))
    boxes, probs = facenet.face_detect(rbg_image)
    boxes = [box for box, prob in zip(boxes, probs) if prob > 0.5]
    if boxes:
        images = facenet.boxes_to_images(rbg_image, boxes)
        embeddings_features = facenet.face_recognize(images)
        ids, names = facenet.face_features_compare(embeddings_features)
        if ids:
            for id, name, image in zip(ids, names, images):
                insert_processor.store_face_recognized_record(
                    door_id=response["door_id"], direction=response["direction"],
                    result_id=id, image_data=np.uint8(image))
        return json.dumps([ids, names, boxes])


@app.route("/register", methods=['POST'])
def register():
    response = request.json
    rgb_frame = response["rgb_frame"]
    rgb_frame = json.loads(rgb_frame)
    rbg_image = Image.fromarray(np.uint8(rgb_frame))
    boxes, probs = facenet.face_detect(rbg_image)
    boxes = [box for box, prob in zip(boxes, probs) if prob > 0.5]
    boxes.sort()
    images = facenet.boxes_to_images(rbg_image, boxes[-1:])
    embeddings_features = facenet.face_recognize(images)
    feature = embeddings_features[0]
    facenet.register_new_face(response["id"], response["name"], images[0], feature)
    return "register success"


@app.route("/door_record", methods=['POST'])
def door_record():
    response = request.json
    records = query_processor.query_door_record(**response)
    return json.dumps(records)


@app.route("/student_record", methods=['POST'])
def student_record():
    response = request.json
    records = query_processor.query_student_face_recognition_record(**response)
    return json.dumps(records)


@app.route("/teacher_record", methods=['POST'])
def teacher_record():
    response = request.json
    records = query_processor.query_teacher_face_recognition_record(**response)
    return json.dumps(records)


@app.route("/class_record", methods=['POST'])
def class_record():
    response = request.json
    records = query_processor.query_class_face_recognition_record(**response)
    return json.dumps(records)


@app.route("/major_record", methods=['POST'])
def major_record():
    response = request.json
    records = query_processor.query_major_face_recognition_record(**response)
    return json.dumps(records)


@app.route("/faculty_record", methods=['POST'])
def faculty_record():
    response = request.json
    records = query_processor.query_faculty_face_recognition_record(**response)
    return json.dumps(records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
