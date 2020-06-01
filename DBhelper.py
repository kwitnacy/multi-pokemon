import pymysql
class DBHelper:

    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = ""
        self.db = "test"

    def __connect__(self):
        self.con = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.con.commit()
        self.__disconnect__()

    def fetch_otherdb(self, sql, db_name):
        self.__connect__()
        self.cur.execute("USE "+ db_name)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute_otherdb(self, sql, db_name):
        self.__connect__()
        self.cur.execute("USE "+ db_name)
        self.cur.execute(sql)
        self.con.commit()
        self.__disconnect__()       
              
    def delete_db(self,db_name):
        self.__connect__()
        self.cur.execute("DROP DATABASE "+db_name)
        self.__disconnect__()
    def change_db(self,db_name):
        self.db=db_name


