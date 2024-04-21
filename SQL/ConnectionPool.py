from psycopg2 import pool


class ConnectionPool:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConnectionPool, cls).__new__(cls, *args, **kwargs)
            cls._instance.conn_pool = pool.ThreadedConnectionPool(
                minconn=4, maxconn=20,
                dbname="accesscontrolsystem",
                user="postgres",
                password="111111",
                host="localhost",
                port="5432")
        return cls._instance

    def __init__(self):
        pass
