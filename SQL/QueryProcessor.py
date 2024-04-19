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

    def load_face_image_feature_vector(self):
        sql = "SELECT PersonID,Name,FeatureVector FROM  Person"
        return asyncio.run(self.process_query(sql))

    def query_door_record(self, door_id, direction, start_time, end_time):
        sql = "SELECT * FROM DoorRecordView " \
              "WHERE DoorID = %s AND Direction = %s AND RecordTime BETWEEN %s AND %s", \
            (door_id, direction, start_time, end_time)
        return asyncio.run(self.process_query(sql))

    def query_person_face_recognition_record(self, person_id, start_time, end_time):
        sql = "SELECT PersonID,Name, Surname,RecordTime,DoorID,Direction " \
              "FROM Person,DoorRecordView " \
              "WHERE PersonID = %s AND RecordTime BETWEEN %s AND %s " \
              "AND Person.PersonID = DoorRecordView.PersonID", \
            (person_id, start_time, end_time)
        return asyncio.run(self.process_query(sql))



query_processor = QueryProcessor()

# import time
# from timeit import timeit
#
# @timeit
# def test():
#     queries = ["SELECT * FROM course", "SELECT * FROM dept", "SELECT * FROM sc", "SELECT * FROM student"]
#     for query in queries:
#         results = asyncio.run(query_processor.process_query(query))
#         print(f"Query: {query}")
#         print(f"Result: {results}")
#
# if __name__ == '__main__':
#     start = time.time()
#     for i in range(100):
#         test()
#     end = time.time()
#     print(f"Time: {end - start}")
