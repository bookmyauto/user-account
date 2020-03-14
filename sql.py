"""
                Description : contains code for database handling
                Author      : Rahul Tudu
"""
import pymysql
import config


class Sql:
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                   RETURNS INSTANCE OF CURSOR                                                                                              #
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def get_connection():
        conn = pymysql.connect(host=config.host, user=config.user, passwd=config.password, db=config.database)
        cur = conn.cursor()
        return conn, cur
