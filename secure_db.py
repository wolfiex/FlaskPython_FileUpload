
from pysqlcipher3 import dbapi2 as sqlite3
from config import app_key, db_loc
from datetime import datetime

class Database(object):
    def __init__(self, dbname,appkey):
        self.dbname = dbname
        self.apkey  = appkey

    def conndb(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA key='%s'"%self.apkey)

    def close(self):
        self.conn.close()
    
    def createDB(self):
        self.conndb()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS upload (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dir TEXT NOT NULL,
            uploadcode TEXT UNIQUE
            );
            '''
        )
        
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS log (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            uploadcode TEXT NOT NULL,
            file TEXT NOT NULL,
            time TEXT NOT NULL
            );
            '''
        )

        self.conn.commit()
        self.conn.close()


    def add_user(self, user, dir, keycode):
        self.conndb()
        self.cursor.execute(
            '''
            INSERT INTO upload (name, dir, uploadcode)
            VALUES ("%s", "%s", "%s")
            '''%(user,dir,keycode)
        )
        self.conn.commit()
        self.conn.close()        



    def queryDB(self, sql):
        self.conndb()
        self.cursor.execute(sql)

        if sql[0:6].lower() == 'select':
            result = self.cursor.fetchall()
            self.conn.close()
            return result
        else:
            self.conn.commit()
            self.conn.close()


    def writefile(self, user_code, file=False):
        self.conndb()
        self.cursor.execute('select * from upload where uploadcode="%s"'%user_code)

        result = self.cursor.fetchall()
        
        
        
        if len(result)<0: 
            passed = False
        elif not file:
            ## just getting directory
            passed = result[0][2]
        else:
            self.cursor.execute(
                '''
                INSERT INTO log (uploadcode,file,time)
                VALUES ("%s", "%s", "%s")
                '''%(user_code,file,datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            )
            passed = result[0][2]##'directory'
            
        self.conn.commit()
        self.conn.close()

        return passed
        
    def printlog(self):
        self.conndb()
        self.cursor.execute('select * from log'%user_code)

        for i in self.cursor.fetchall(): 
            print (i)
        
        self.conn.commit()
        self.conn.close()

        return passed



            
if __name__ == '__main__':
    import sys,os
    ## you can use arg parse if you want a neater interface
    if '--wipe' in sys.argv:
        os.system('rm '+db_loc)
        sqlc = Database(db_loc,app_key)
        sqlc.createDB()
        
    
        
        