import pickle
import asyncpg
import asyncio

import numpy as np

dsn = "postgresql://postgres:admin@localhost:5432/accesscontrolsystem" # dsn

async def execute_query(sql, params=None):
    async with asyncpg.create_pool(min_size=4, max_size=20, dsn=dsn) as conn_pool:
        async with conn_pool.acquire() as connection:
            if params:
                return await connection.fetch(sql, *params)
            else:
                return await connection.fetch(sql)

async def add_admin_person(person_id, name, surname, gender, age, phone, position, feature_vector, image):
    sql = "INSERT INTO Person (PersonID, Name, Surname, Gender, Age, PhoneNumber, Position, FeatureVector," \
          " ImageData) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)"
    values = (person_id, name, surname, gender, age, phone, position, feature_vector, image)
    await execute_query(sql, values)

async def add_admin_user(username, password, person_id):
    sql = "INSERT INTO AdminUser (Username, Password, PersonID) VALUES ($1, $2, $3)"
    values = (username, password, person_id)
    await execute_query(sql, values)

async def main():
    with open('Admin/fw.bin', 'rb') as f:
        feature_vector = f.read()

    with open('Admin/img.bin', 'rb') as f:
        image = f.read()

    await add_admin_person(0, 'John', 'Doe', 'Male', 25, '123456789', 'Admin', feature_vector, image)
    await add_admin_user('admin', 'YWRtaW4=', 0) # 'admin' in base64

if __name__ == '__main__':
    asyncio.run(main())