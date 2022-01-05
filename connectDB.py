import psycopg2
import sys
import os
class Databases():
    def __init__(self):


        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWD")
        host_product = os.getenv("DB_HOST")
        dbname = os.getenv("DB_NAME")
        port = os.getenv("DB_PORT")

        product_connection_string = "dbname={dbname} user={user} host={host} password={password} port={port}"\
                                    .format(dbname=dbname,
                                            user=user,
                                            host=host_product,
                                            password=password,
                                            port=port)
        #db 연결
        try:
            self.db = psycopg2.connect(product_connection_string)
            print("connect success!")
        except:
            print("I am unable to connect to the database")

        self.cursor = self.db.cursor()

    def __del__(self):
            self.db.close()
            self.cursor.close()

    def execute(self,query,args={}):
            self.cursor.execute(query,args)
            row = self.cursor.fetchall()
            return row

    def commit(self):
            self.cursor.commit()

    def getColumns(self, table):
        self.cursor.execute("Select * FROM {} LIMIT 0".format(table))
        return [desc[0] for desc in self.cursor.description]

    def insert(self,table,data,*column):
        sql = "INSERT INTO {table} {column} VALUES {data} ;".format(table=table,column=column,data=data)
        try:
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB  ",e)
