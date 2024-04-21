import asyncio
import pickle

from SQL import ConnectionPool

class InsertProcessor:
    def __init__(self):
        self.conn_pool = ConnectionPool().conn_pool

    async def run_insert(self, sql, values):
        conn = self.conn_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        self.conn_pool.putconn(conn)

    def insert_into_person(self, person_id, name, surname, gender, age, phone, position, feature_vector, image):
        sql = "INSERT INTO Person (PersonID, Name, Surname, Gender, Age, PhoneNumber, Position, FeatureVector," \
              " ImageData) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (person_id, name, surname, gender, age, phone, position, pickle.dumps(feature_vector), pickle.dumps(image))

        asyncio.run(self.run_insert(sql, values))

    def insert_into_door(self, door_id, door_access, direction, location):
        sql = "INSERT INTO Door (DoorID, AccessType, Direction, Location) VALUES (%s, %s, %s, %s)"
        values = (door_id, door_access, direction, location)

        asyncio.run(self.run_insert(sql, values))

    def insert_into_record(self, record_id, access, door_id, direction, person_id):
        sql = "INSERT INTO Record (RecordID, RecordTime, Access, DoorID, Direction, PersonID) VALUES (%s, NOW(), %s, %s, %s, %s)"
        values = (record_id, access, door_id, direction, person_id)

        asyncio.run(self.run_insert(sql, values))

insert_processor = InsertProcessor()
