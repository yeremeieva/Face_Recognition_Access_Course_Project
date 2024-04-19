import asyncio

import psycopg2

from SQL import ConnectionPool


class InsertProcessor:
    def __init__(self):
        self.conn_pool = ConnectionPool().conn_pool

    async def run_insert(self, sql):
        conn = self.conn_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        self.conn_pool.putconn(conn)

    def insert_into_person(self, person_id, name, surname, gender, age, phone, position, feature_vector, image_data):
        sql = "INSERT INTO Person (PersonID, Name,Surname, Gender, Age, PhoneNumber, Position, FeatureVector," \
              " ImageData) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
              (person_id, name, surname, gender, age, phone, position,
               psycopg2.Binary(feature_vector), psycopg2.Binary(image_data))
        asyncio.run(self.run_insert(sql))

    def insert_into_door(self, door_id, door_location):
        sql = "INSERT INTO Door (DoorID, Location) " \
              "VALUES (%s, %s)", (door_id, door_location)
        asyncio.run(self.run_insert(sql))

    def store_face_recognized_record(self, record_id, access, image_data, door_id, person_id, direction):
        sql = "INSERT INTO Record (RecordID, Access, ImageData, DoorID, PersonID, Direction) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s)", \
            (record_id, access, psycopg2.Binary(image_data), door_id, person_id, direction)
        asyncio.run(self.run_insert(sql))

insert_processor = InsertProcessor()
