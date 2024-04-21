import asyncio
import pickle

import asyncpg
from SQL.config import dsn

class InsertProcessor:
    def __init__(self):
        pass

    async def run_insert(self, sql, values):
        async with asyncpg.create_pool(min_size=4, max_size=20, dsn=dsn) as conn_pool:
            async with conn_pool.acquire() as connection:
                return await connection.execute(sql, *values)

    def insert_into_person(self, person_id, name, surname, gender, age, phone, position, feature_vector, image):
        sql = "INSERT INTO Person (PersonID, Name, Surname, Gender, Age, PhoneNumber, Position, FeatureVector," \
              " ImageData) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)"
        values = (person_id, name, surname, gender, age, phone, position, pickle.dumps(feature_vector), pickle.dumps(image))

        asyncio.run(self.run_insert(sql, values))

    def insert_into_door(self, door_id, door_access, direction, location):
        sql = "INSERT INTO Door (DoorID, AccessType, Direction, Location) VALUES ($1, $2, $3, $4)"
        values = (door_id, door_access, direction, location)

        asyncio.run(self.run_insert(sql, values))

    def insert_into_record(self, record_id, access, door_id, direction, person_id):
        sql = "INSERT INTO Record (RecordID, RecordTime, Access, DoorID, Direction, PersonID) VALUES ($1, NOW(), $2, $3, $4, $5)"
        values = (record_id, access, door_id, direction, person_id)

        asyncio.run(self.run_insert(sql, values))

insert_processor = InsertProcessor()
