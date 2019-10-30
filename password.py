import os
import mysql.connector
import sys
sys.append("../config")
import config as C
sys.append("../utilities")
from error import error
from result import result

E   = error()
R   = result

class password:
    def change_password(self, payload):
        mycursor    = None
        try:
            mydb        = mysql.connector.connect(host = C.host, user = C.user, passwd = C.password, database = C.database)
            mycursor    = mydb.cursor()
            _old_       = str(payload["old_password"])
            _new_       = str(payload["new_password"])
            _number_    = str(payload["number"])
            sql         = "select password from users where number = %s"
            val         = (_number_)
            mycursor.execute(sql, val)
            data        = mycursor.fetchone()
            if(len(data) > 0):
                old     = str(data[0])
                if(_old_ == old):
                    sql = "update users set password = %s where number = %s"
                    val = (_new_, _number_)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    result  = R.make_result(result = "password updated", code = "201", message = "Password updated")
                    return result
                else:
                    error   = E.make_error(error = "password mismatch", code = 200, displayError = "Oops something went wrong !")
                    return error
            else:
                error   = E.make_error(error = "account does not exist", code = 405, displayError = "Account does not exist")
                return error
        except Exception as e:
            log.warning(e)
            if(mycursor != None):
                mycursor.close()
            error = E.make_error(error = "system failure", code = 500, displayError = "Oops something went wrong !")
            return error
    def forgot_password_get_otp(self, payload):
        mycursor    = None
        try:
            mydb        = mysql.connector.connect(host = C.host, user = C.user, passwd = C.password, database = C.database)
            mycursor    = mydb.cursor()
            _number_    = str(payload["number"])
            response    = requests.get("https://2factor.in/API/V1/" + str(C.2factor_api_key) + "/SMS/+91" + str(_number_)[-10:]+ "/AUTOGEN")
            response    = dict(response)
            if(response["Status"] == "Success"):
                _session_id_    = response["Details"]
                sql             = "update users set session_id = %s, otp_verified = 0 where number = %s"
                val             = (_session_id_, _number_)
                mycursor.execute(sql, val)
                db.commit()
                result          = R.make_result(result = "OTP sent", code = 201, message = "Please enter otp")
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                return result
            else:
                mycursor.close()
                error = E.make_error(error = "otp system failure", code = 500, displayError = "Oops something went wrong !")
        except Exception as e:
            log.warning(e)
            if(mycursor != None):
                mycursor.close()
            error = E.make_error(error = "system failure", code = 500, displayError = "Oops something went wrong !")
            return error
    def forgot_password_change(self, payload):
        mycursor    = None
        try:
            mydb        = mysql.connector.connect(host = C.host, user = C.user, passwd = C.password, database = C.database)
            mycursor    = mydb.cursor()
            _new_       = str(payload["new_password"])
            _number_    = str(payload["number"])
            sql = "update users set password = %s where number = %s"
            val = (_new_, _number_)
            mycursor.execute(sql, val)
            mydb.commit()
            result  = R.make_result(result = "password updated", code = "201", message = "Password updated")
            return result
        except Exception as e:
            log.warning(e)
            if(mycursor != None):
                mycursor.close()
            error = E.make_error(error = "system failure", code = 500, displayError = "Oops something went wrong !")
            return error
