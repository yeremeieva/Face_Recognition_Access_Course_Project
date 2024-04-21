import asyncio
import asyncpg
from SQL.config import dsn

class AdminProcessor:
    def __init__(self):
        pass

    async def run_query(self, sql, params=None):
        async with asyncpg.create_pool(min_size=4, max_size=20, dsn=dsn) as conn_pool:
            async with conn_pool.acquire() as connection:
                if params:
                    return await connection.fetch(sql, *params)
                else:
                    return await connection.fetch(sql)

    async def process_query(self, sql, params=None):
        return await self.run_query(sql, params)

    def get_time_spent_by_person(self, person_id):
        sql = """
            WITH first_in_out_times AS (
                SELECT
                    p.Name, p.Surname,
                    MIN(r.RecordTime) FILTER (WHERE r.Direction = 'In') AS first_in_time,
                    MAX(r.RecordTime) FILTER (WHERE r.Direction = 'Out') AS latest_out_time
                FROM
                    Record r
                JOIN
                    Person p ON p.PersonID = r.PersonID
                WHERE
                    p.PersonID = $1 AND
                    recordtime >= CURRENT_DATE AND
                    recordtime < CURRENT_DATE + INTERVAL '1 day'
                GROUP BY
                    p.Name, p.Surname
            )
            SELECT
                Name,
                Surname,
                first_in_time,
                latest_out_time,
                COALESCE(latest_out_time - first_in_time, INTERVAL '0 minutes') AS total_time_spent
            FROM
                first_in_out_times;
        """
        return asyncio.run(self.process_query(sql, (person_id)))

    def get_daily_access_report(self):
        sql = """
            SELECT p.Name, p.Surname, r.RecordTime, d.Location, r.Direction
            FROM Record r
            JOIN Person p ON r.PersonID = p.PersonID
            JOIN Door d ON r.DoorID = d.DoorID AND d.Direction = r.Direction
            WHERE DATE(r.RecordTime) = CURRENT_DATE;
        """
        return asyncio.run(self.process_query(sql))


    def get_denied_access_report(self):
        sql = """
            SELECT p.Name, p.Surname, r.RecordTime, d.Location
            FROM Record r
            JOIN Person p ON r.PersonID = p.PersonID
            JOIN Door d ON r.DoorID = d.DoorID AND d.Direction = r.Direction
            WHERE r.Access = FALSE AND
            DATE(r.RecordTime) = CURRENT_DATE;
        """
        return asyncio.run(self.process_query(sql))

    def update_person_position(self, person_id, new_position):
        sql = "UPDATE Person SET Position = $1 WHERE PersonID = $2;"
        return asyncio.run(self.process_query(sql, (new_position, person_id)))

    def list_people_by_position_and_gender(self, position, gender):
        sql = "SELECT * FROM Person WHERE Position = $1 AND Gender = $2;"
        return asyncio.run(self.process_query(sql, (position, gender)))

# Usage
admin_processor = AdminProcessor()
