import logging
import requests
import config
import sql
import response

# contains all code related to otp

SQL     = Sql()
Resp    = Response()
class Otp:

    '''
    code to create otp
    '''
    def create_otp(self, payload):
        mycursor            = None
        try:
            mydb, mycursor  = SQL.get_connection()
            number          = str(payload["number"])
            response        = dict(requests.get("https://2factor.in/API/V1/" + str(config.api_key_2factor) + "/SMS/+91" + str(number)[-10:]+ "/AUTOGEN"))
            if(response["Status"] == "Success"):
                session_id      = response["Details"]
                sql_query       = "insert into user_otp (number, session_id) values (%s, %s)"
                values          = (_number_, _session_id_)
                result          = Resp.make_result(result_code = 201, result_message = "OTP sent", display_message = "Please enter otp")
                mycursor.execute(sql_query, values)
                mydb.commit()
                mycursor.close()
                return result
            else:
                mycursor.close()
                error           = Resp.make_error(error_code = 500, error_message = "Otp system failure", display_message = "Oops something went wrong !")
                return error
        except Exception as e:
            log.warning(e)
            if(mycursor != None):
                mycursor.close()
            error = Resp.make_error(error_code = 500, error_message = "System failure", display_message = "Oops something went wrong !")
            return error

    '''
    code to verify otp
    '''
    def verify_otp(self, payload):
        mycursor            = None
        try:
            mydb, mycursor  = SQL.get_connection()
            number          = str(payload["number"])
            otp             = str(payload["otp"])
            sql_query       = "select session_id from user_otp where number = " + str(number)
            mycursor.execute(sql_query)
            data            = mycursor.fetchone(sql)
            session_id      = str(data[0])
            response        = requests.get("https://2factor.in/API/V1/" + str(config.api_key_2factor) + "/SMS/VERIFY/" + str(session_id)+ "/" + str(otp))
            response        = dict(response)
            if(response["Status"] == "Success" and response["Details"] == "OTP Matched"):
                sql_query       = "update user_otp set otp_verified = 1 where number = " + str(number)
                result          = Resp.make_result(result_code = 202, result_message = "OTP matched", disply_message = "Otp matched successfully")
                mycursor.execute(sql)
                mydb.commit()
                mycursor.close()
                return result
            else:
                error           = Resp.make_error(error_code = 200, error_message = "OTP mismatched", display_message = "otp does not match")
                mycursor.close()
                return error
        except Exception as e:
            log.warning(e)
            if(mycursor != None):
                mycursor.close()
            error = Resp.make_error(error_code = 500, error_message = "system failure", display_message = "Oops something went wrong !")
            return error