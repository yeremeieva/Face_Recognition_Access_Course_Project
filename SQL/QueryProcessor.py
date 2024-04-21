import asyncio
import asyncpg
from SQL.config import dsn

class QueryProcessor:
    def __init__(self):
        pass

    async def run_query(self, sql):
        async with asyncpg.create_pool(min_size=4, max_size=20, dsn=dsn) as conn_pool:
            async with conn_pool.acquire() as connection:
                return await connection.fetch(sql)

    async def process_query(self, query):
        return await self.run_query(query)

    def query_records(self):
        sql = "SELECT p.Name, p.Surname, r.RecordTime, r.Access, r.DoorID, r.Direction, d.Location " \
            "FROM Record r " \
            "JOIN Person p ON r.PersonID = p.PersonID " \
            "JOIN Door d ON r.DoorID = d.DoorID AND d.Direction = r.Direction"
        # sql = "SELECT RecordID, RecordTime, Access, DoorID, Direction, PersonID FROM Record"
        return asyncio.run(self.process_query(sql))

    def query_people(self):
        sql = "SELECT PersonID, Name, Gender, Age, PhoneNumber, Position, FeatureVector, ImageData FROM Person"
        return asyncio.run(self.process_query(sql))
    
    def query_login(self, username, password):
        sql = f"SELECT * FROM AdminUser WHERE Username='{username}' AND Password='{password}'"
        return asyncio.run(self.process_query(sql))
    
    def query_person_by_id(self, person_id):
        sql = f"SELECT PersonID, Name, Surname, Position FROM Person WHERE PersonID={person_id}"
        return asyncio.run(self.process_query(sql))
    
    def query_last_record_id(self):
        sql = "SELECT MAX(RecordID) FROM Record"
        return asyncio.run(self.process_query(sql))

query_processor = QueryProcessor()