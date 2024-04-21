import asyncio
import asyncpg
import pickle
import json
from flask import Flask, request, jsonify
import datetime

import _init_paths
from SQL.InsertProcessor import insert_processor
from SQL.QueryProcessor import query_processor
# from SQL.AdminProcessor import admin_processor

app = Flask(__name__)

@app.route('/add_person', methods=['POST'])
def add_person():
    data = request.json
    response = insert_processor.insert_into_person(**data)
    return json.dumps(response)

@app.route('/add_door', methods=['POST'])
def add_door():
    data = request.json
    response = insert_processor.insert_into_door(**data)
    return json.dumps(response)

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    response = insert_processor.insert_into_record(**data)
    return json.dumps(response)

@app.route('/get_records', methods=['GET'])
def get_records():
    records = query_processor.query_records()

    result = [{
        'record_id': record[0],
        'record_time': str(record[1].utcnow()),
        'access': record[2],
        'door_id': record[3],
        'person_id': record[4]}
        for record in records]

    return result

@app.route('/get_people', methods=['GET'])
def get_people():
    people = query_processor.query_people()

    result = [{
        'person_id': person[0],
        'name': person[1],
        'gender': person[2],
        'age': person[3],
        'phone': person[4],
        'position': person[5],
        'feature_vector': pickle.loads(person[6]),  # Deserialized
        'image': pickle.loads(person[7])  # Deserialized
        } for person in people]

    return result

if __name__ == '__main__':
    app.run(debug=True, port=5555)
