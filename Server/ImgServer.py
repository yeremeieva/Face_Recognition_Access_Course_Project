import json

import numpy as np
from PIL import Image
from flask import Flask
from flask import request

import _init_paths
from FacenetModel import Facenet
from SQL.InsertProcessor import insert_processor
from SQL.QueryProcessor import query_processor

facenet = Facenet()
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"

# todo update file
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
                    person_id=id, image_data=np.uint8(image))
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
    facenet.register_new_person(person_id=response["id"], name=response["name"], image_data=images[0], new_feature_vector=feature)
    return "registration succeeded"


@app.route("/door_record", methods=['POST'])
def door_record():
    response = request.json
    records = query_processor.query_door_record(**response)
    return json.dumps(records)


@app.route("/person_record", methods=['POST'])
def person_record():
    response = request.json
    records = query_processor.query_person_face_recognition_record(**response)
    return json.dumps(records)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
