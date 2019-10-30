import logging
import sql


# contains all code related to otp
class Otp:
    def create_otp(self, payload):
        mycursor            = None
        try:
            mydb, mycursor  = C.get_connection(host = dbconf.host, user = dbconf.user, passwd = dbconf.password, database = dbconf.database)
            _number_        = str(payload["number"])
            response        = dict(requests.get("https://2factor.in/API/V1/" + str(otpconf.2factor_api_key) + "/SMS/+91" + str(_number_)[-10:]+ "/AUTOGEN"))
            if(response["Status"] == "Success"):
                _session_id_    = response["Details"]
                sql             = "insert into user_otp (number, session_id) values (%s, %s)"
                val             = (_number_, _session_id_)
                result          = R.make_result(result = "OTP sent", code = 201, message = "Please enter otp")
                mycursor.execute(sql, val)
                mydb.commit()
                mycursor.close()
                return result
            else:
                mycursor.close()
                error = E.make_error(error = "otp system failure", code = 500, displayError = "Oops something went wrong !")
                return error
        except Exception as e:
            log.warning(e)
            if(mycursor != None):
                mycursor.close()
            error = E.make_error(error = "system failure", code = 500, displayError = "Oops something went wrong !")
            return error
    def verify_otp():