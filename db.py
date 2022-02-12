import psycopg2
import logging
import os
class Databases():
    def __init__(self):
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWD")
        host_product = os.getenv("DB_HOST")
        dbname = os.getenv("DB_NAME")
        port = os.getenv("DB_PORT")

        connection_info = "dbname={dbname} user={user} host={host} password={password} port={port}".format(
            dbname=dbname,
            user=user,
            host=host_product,
            password=password,
            port=port
            )

        # Connect
        try:
            self.db = psycopg2.connect(connection_info)
            logging.info("DB connection was successful!")
        except:
            logging.error("DB connection failed!")

        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self,query,args={}):
        self.cursor.execute(query,args)

    def commit(self):
        self.db.commit()

    def getColumns(self, table):
        self.execute("SELECT * FROM {} LIMIT 0".format(table))
        return [desc[0] for desc in self.cursor.description]

    def read(self, table, columns):
        try:
            self.execute("SELECT {} FROM {}".format(columns, table))
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(e)

    def insert(self,table,column,data):
        try:
            sql = "INSERT INTO {table} ({column}) VALUES ({data})".format(table=table,column=column,data=data)
            print(sql)
            self.execute(sql)
            self.commit()
        except Exception as e :
            print("insert errir")
            logging.error(e)

    def update(self,table, column, value):
        try:
            self.execute("UPDATE {table} SET {column}={value}".format(table=table,column=column,value=value))
        except Exception as e :
            logging.error(e)