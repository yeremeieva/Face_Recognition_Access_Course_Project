import asyncio
import asyncpg
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

async def get_db_connection():
    return await asyncpg.connect(
        database="accesscontrolsystem",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

def serialize_vector(feature_vector):
    return pickle.dumps(feature_vector)

@app.route('/add_person', methods=['POST'])
async def add_person():
    data = request.json
    conn = await get_db_connection()
    serialized_feature_vector = serialize_vector(data['feature_vector'])
    serialized_image_vector = serialize_vector(data['image'])

    try:
        await conn.execute('''
            INSERT INTO Person (PersonID, Name, Gender, Age, PhoneNumber, Position, FeatureVector, ImageData)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ''', data['person_id'], data['name'], data['gender'], data['age'], data['phone'], data['position'], serialized_feature_vector, serialized_image_vector)
        await conn.close()
        return jsonify({'message': 'Person added successfully'}), 201
    except Exception as e:
        print(str(e))
        await conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/add_door', methods=['POST'])
async def add_door():
    data = request.json
    conn = await get_db_connection()
    try:
        await conn.execute('''
            INSERT INTO Door (DoorID, AccessType, Direction)
            VALUES ($1, $2, $3)
        ''', data['door_id'], data['door_access'], data['direction'])
        await conn.close()
        return jsonify({'message': 'Door added successfully'}), 201
    except Exception as e:
        print(str(e))        
        await conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/add_record', methods=['POST'])
async def insert_record():
    data = request.json
    conn = await get_db_connection()
    try:
        await conn.execute("""
            INSERT INTO Record (RecordID, RecordTime, Access, DoorID, PersonID)
            VALUES ($1, NOW(), $2, $3, $4)
        """, data['record_id'], data['access'], data['door_id'], data['person_id'])
        await conn.close()
        return jsonify({'message': 'Record added successfully'}), 201
    except Exception as e:
        print(str(e))
        await conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/get_records', methods=['GET'])
async def get_records():
    conn = await get_db_connection()
    try:
        records = await conn.fetch('''
            SELECT RecordID, RecordTime, Access, DoorID, PersonID FROM Record
        ''')
        result = [dict(record) for record in records]
        await conn.close()
        return jsonify(result), 200
    except Exception as e:
        print(str(e))
        await conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/get_people', methods=['GET'])
async def get_people():
    conn = await get_db_connection()
    try:
        people = await conn.fetch('''
            SELECT PersonID, Name, Gender, Age, PhoneNumber, Position, FeatureVector, ImageData FROM Person
        ''')
        result = [{
            'person_id': person['personid'],
            'name': person['name'],
            'gender': person['gender'],
            'age': person['age'],
            'phone': person['phonenumber'],
            'position': person['position'],
            'feature_vector': pickle.loads(person['featurevector']),  # Deserialized
            'image': pickle.loads(person['imagedata'])  # Deserialized
            } for person in people]
        
        await conn.close()
        return jsonify(result), 200
    except Exception as e:
        print(str(e))
        await conn.close()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5555)
