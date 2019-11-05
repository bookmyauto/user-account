import mysql.connector
import config as c


class Sql:
    
    # returns instance of db and cursor
    @staticmethod
    def get_connection():
        mydb = mysql.connector.connect(host = c.host, user = c.username, passwd = c.password, database = c.database)
        mycursor = mydb.cursor()
        return mydb, mycursor
