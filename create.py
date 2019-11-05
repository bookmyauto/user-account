import os
import logging
from bson import ObjectId
import sys
sys.append("../config")
from dbconfig import dbconfig
from otpconfig import otpconfig
sys.append("../../SQL")
from connect import connect
sys.append("../../utilities")
from error import error
from result import result
E       = error()
R       = result()
C       = connect()
dbconf  = dbconfig()
otpconf = otpconfig()

class create:

    def create_user(self, payload):
        mycursor            = None
        try:
            mydb, mycursor  = C.get_connection(host = dbconf.host, user = dbconf.user, passwd = dbconf.password, database = dbconf.database)
            _id_            = str(ObjectId())
            _name_          = str(payload["name"])
            _number_        = str(payload["number"])
            _password_      = str(payload["password"])
            # verify existence of number
            sql             = "select u_id from users where number = " + str(_number_)
            mycursor.execute(sql)
            data            = mycursor.fetchone()
            if(len(data) != 0):
                error       = E.make_error(error = "number alreay exists", code = 406, displayError = "This number already exists.")
                return error
            sql             = "insert into users (u_id, name, number, password) values (%s, %s, %s, %s)"
            val             = (_id_, _name_, _number_, _password_)
            result          = R.make_result(result = "user created", u_id = _id_, code = 201, message = "Congrats, your account has been created.")
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            return result
        except Exception as e:
            log.warning(e)
            if(mycursor != None):
                mycursor.close()
            error = E.make_error(error = "system failure", code = 500, displayError = "Oops something went wrong !")
            return error

