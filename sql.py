import mysql.connector
import config as C
class Sql:

    '''
    returns instance of db and cursor
    '''
    def get_connection():
        mydb        = mysql.connector.connect(host = C.host, user = C.username, passwd = C.password, database = C.database)
        mycursor    = mydb.cursor()
        return mydb, mycursor

