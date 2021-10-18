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

    def insertDB(self,table,data,*column):
        sql = " INSERT INTO {table} {column} VALUES {data} ;".format(table=table,column=column,data=data)
        try:
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB  ",e)

    def readDB(self):
        sql = " SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_CATALOG = " + self.dbname + " and TABLE_NAME = 'restaurant'"
        try:
            print(sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        return result

    def getRestaurants1(self, limit, offset):
        sql = "SELECT * FROM restaurant where content_id IS NULL and muslim_friendly IS NULL LIMIT {} OFFSET {} ".format(limit, offset)
        try:
            print(sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = "get info err: " + str(e)
            sys.exit()

        print(result)
        return result

    def getTourRestaurants(self):
        sql = "SELECT * FROM restaurant where content_id IS NOT NULL AND images IS NULL"
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            result = "getTourRestaurants err: " + str(e)
        
        return result

    def updateImgUrl(self, table, id, imgs):
        sql = "UPDATE {} SET images=array{}::text[] WHERE id='{}'".format(table, imgs, id)
        
        try:
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
            result = "success to update!"
        except Exception as e:
            result = "update err: " + str(e)
            self.db.commit()

        return result

    def updateContentId(self, id, contentid):
        sql = "UPDATE restaurant SET content_id={} WHERE id={}".format(contentid, id)
        try:
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
            result = "success to update!"
        except Exception as e:
            result = "update err: " + str(e)

        return result

    def insertFoodtruckData(self, data):
        sql = " INSERT INTO foodtruck(no, total_count, instt_cdnm, lcns_no, prms_dt, induty_cdnm, bssh_nm, upso_addr, name, telno) VALUES {} ;".format(tuple(data.values()))
        try:
            print(sql)
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB  ",e)
