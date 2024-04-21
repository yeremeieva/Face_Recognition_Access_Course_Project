import asyncio
import asyncpg
import pickle
import json
from flask import Flask, request, jsonify, render_template
import datetime

import _init_paths
from SQL.InsertProcessor import insert_processor
from SQL.QueryProcessor import query_processor
from SQL.AdminProcessor import admin_processor

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
        'direction': record[4],
        'person_id': record[5]}
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

if __name__ == '__main__':
    app.run(debug=True, port=5555)
