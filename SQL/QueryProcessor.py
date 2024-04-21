import asyncio

from SQL.ConnectionPool import ConnectionPool


class QueryProcessor:
    def __init__(self):
        self.conn_pool = ConnectionPool().conn_pool

    async def run_query(self, sql):
        conn = self.conn_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conn_pool.putconn(conn)
        return result

    async def process_query(self, query):
        return await query_processor.run_query(query)

    def query_records(self):
        sql = "SELECT RecordID, RecordTime, Access, DoorID, Direction, PersonID FROM Record"
        return asyncio.run(self.process_query(sql))

    def query_people(self):
        sql = "SELECT PersonID, Name, Gender, Age, PhoneNumber, Position, FeatureVector, ImageData FROM Person"
        return asyncio.run(self.process_query(sql))

query_processor = QueryProcessor()