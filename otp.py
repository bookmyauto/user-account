import  logging
import  requests
import  config
import  json
from    sql import Sql
from    response import Response


class Otp:

    # code to create otp
    @staticmethod
    def create_otp(number):
        conn   = None
        try:
            conn, cur               = Sql.get_connection()
            logging.debug("Connection and cursor received")
            response                = requests.get("https://2factor.in/API/V1/" + str(config.api_key_2factor) + "/SMS/+91" + str(number)[-10:]+ "/AUTOGEN")
            response                = dict(response.json())
            if response["Status"] == "Success":
                session_id          = response["Details"]
                logging.debug("OTP created successfully with session id: " + str(session_id))
                
                sql_query           = "insert into user_otp (number, session_id) values ('{0}', '{1}') on duplicate key update session_id = '{1}', otp_verified = 0"
                cur.execute(sql_query.format(number, session_id))
                conn.commit()
                logging.debug("Connection closed")
                result              = Response.make_result(result_code = 200, result_message = "OTP sent", display_message = "Please enter otp")
                conn.close()
                return result
            else:
                logging.warning("OTP could not be created")
                error = Response.make_error(error_code = 500, error_message = "System failure", display_message = "Oops something went wrong !")
                conn.close()
                return error
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in create_otp: " + str(e))
            error = Response.make_error(error_code = 500, error_message = "System failure", display_message = "Oops something went wrong !")
            return error

    # code to verify otp
    @staticmethod
    def verify_otp(number, otp):
        conn                        = None
        try:
            conn, cur               = Sql.get_connection()
            logging.debug("Connection and cursor received")
            sql_query               = "select session_id from user_otp where number = " + str(number)
            cur.execute(sql_query)
            data                    = cur.fetchone()
            session_id              = str(data[0])
            print(session_id)
            response                = requests.get("https://2factor.in/API/V1/" + str(config.api_key_2factor) + "/SMS/VERIFY/" + str(session_id)+ "/" + str(otp))
            response                = dict(response.json())
            if response["Status"] == "Success" and response["Details"] == "OTP Matched" :
                sql_query           = "update user_otp set otp_verified = 1 where number = " + str(number)
                cur.execute(sql_query)
                conn.commit()
                result              = Response.make_result(result_code = 200, match = 1, result_message = "OTP matched", display_message = "OTP matched successfully")
                logging.debug("OTP verified successfully")
                conn.close()
                return result
            else:
                logging.debug("OTP could not be verified")
                error               = Response.make_result(result_code = 200, match = 0, result_message = "OTP mismatched", display_message = "OTP does not match")
                conn.close()
                return error
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("Error in verify_otp: " + str(e))
            error               = Response.make_error(error_code = 500, error_message = "System failure", display_message = "Oops something went wrong !")
            return error
