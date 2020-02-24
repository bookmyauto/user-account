import  logging
import  requests
import  config
from    sql import Sql
from    response import Response
from    create import Create


class Otp:

    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                   CREATES OTP                                                                                 #
    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def create_otp(number):
        conn   = None
        try:
            conn, cur               = Sql.get_connection()
            logging.debug("  " + str(number) + ":  Connection and cursor received")
            response                = requests.get("https://2factor.in/API/V1/" + str(config.api_key_2factor) + "/SMS/+91" + str(number)[-10:]+ "/AUTOGEN")
            response                = dict(response.json())
            if response["Status"] == "Success":
                session_id          = response["Details"]
                logging.debug("  " + str(number) + ":  OTP created successfully with session id: " + str(session_id))
                
                sql_query           = "insert into user_otp (number, session_id) values ('{0}', '{1}') on duplicate key update session_id = '{1}', otp_verified = 0"
                cur.execute(sql_query.format(number, session_id))
                conn.commit()
                logging.debug("  " + str(number) + ":  Connection closed")
                result              = Response.make_response(200, "OTP sent", "Please enter otp")
                conn.close()
                return result
            else:
                logging.warning("  " + str(number) + ":  OTP could not be created")
                error = Response.make_response(500, "System failure", "Oops something went wrong !")
                conn.close()
                return error
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("  " + str(number) + ":  Error in create_otp: " + str(e))
            error = Response.make_response(500, "System failure", "Oops something went wrong !")
            return error

    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                   VERIFY OTP                                                                                  #
    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def verify_otp(number, otp):
        conn                        = None
        try:
            conn, cur               = Sql.get_connection()
            logging.debug("  " + str(number) + ":  Connection and cursor received")
            sql_query               = "select session_id from user_otp where number = " + str(number)
            cur.execute(sql_query)
            data                    = cur.fetchone()
            session_id              = str(data[0])
            response                = requests.get("https://2factor.in/API/V1/" + str(config.api_key_2factor) + "/SMS/VERIFY/" + str(session_id)+ "/" + str(otp))
            response                = dict(response.json())
            if response["Status"] == "Success" and response["Details"] == "OTP Matched" :
                sql_query           = "update user_otp set otp_verified = 1 where number = " + str(number)
                cur.execute(sql_query)
                conn.commit()
                response            = Create.check_user_repetition(number)
                if "present" in response["data"]:
                    if response["data"]["present"]  == 1:
                        result              = Response.make_response(200, "OTP matched", "OTP matched successfully", action = "login", match = 1)
                    if response["data"]["present"]  == 0:
                        result              = Response.make_response(200, "OTP matched", "OTP matched successfully", action = "signUp", match = 1)
                    logging.debug("  " + str(number) + ":  OTP verified successfully")
                    conn.close()
                    return result
                else:
                    conn.close()
                    error               = Response.make_response(500, "System failure", "Oops something went wrong !")
                    return error
            else:
                logging.debug("OTP could not be verified")
                error               = Response.make_response(200, "OTP mismatched", "OTP does not match", match = 0)
                conn.close()
                return error
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("  " + str(number) + ":  Error in verify_otp: " + str(e))
            error               = Response.make_response(500, "System failure", "Oops something went wrong !")
            return error
