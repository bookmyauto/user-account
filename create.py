import os
import logging
from bson import ObjectId
from sql import Sql
from response import Response


class Create:

    @staticmethod
    def check_user_repetition(payload):
        mydb, mycursor  = Sql.get_connection()

        # get data from payload
        number          = str(payload["number"])

        # check from db
        sql_query       = "select u_id from users where number = \'" + str(number) + "\'"
        mycursor.execute(sql_query)
        data            = mycursor.fetchone()
        if len(data) == 0:
            return 0
        return 1

    @staticmethod
    def create_user(payload):
        mycursor            = None
        try:
            mydb, mycursor  = Sql.get_connection()
            # get data from payload
            u_id            = str(ObjectId())
            name            = str(payload["name"])
            number          = str(payload["number"])
            password        = str(payload["password"])

            # insert in db
            sql_query       = "insert into users (u_id, name, number, password) values (%s, %s, %s, %s)"
            val             = (u_id, name, number, password)
            mycursor.execute(sql_query, val)
            mydb.commit()
            result          = Response.make_result(result_code = 201, result_message = "Account created",
                                                   display_message = "Your account has been created",
                                                   u_id = u_id)
            mycursor.close()
            return result
        except Exception as e:
            logging.warning(e)
            if mycursor is not None:
                mycursor.close()
            error = Response.make_error(error_message = "system failure", error_code = 500, display_message = "Oops something went wrong !")
            return error

