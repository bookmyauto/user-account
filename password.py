import logging
from sql import Sql
from response import Response


class Password:

    # change password here
    @staticmethod
    def change_password(payload):
        mycursor    = None
        try:
            mydb, mycursor = Sql.get_connection()
            mycursor        = mydb.cursor()
            old_password    = str(payload["old_password"])
            new_password    = str(payload["new_password"])
            number          = str(payload["number"])
            sql_query       = "select password from users where number = %s"
            val             = str(number)
            mycursor.execute(sql_query, val)
            data        = mycursor.fetchone()
            if len(data) > 0:
                old     = str(data[0])
                if old_password == old:
                    sql_query = "update users set password = %s where number = %s"
                    val = (new_password, number)
                    mycursor.execute(sql_query, val)
                    mydb.commit()
                    result  = Response.make_result(result_messagee = "password updated", result_ode = "201", result_message = "Password updated")
                    return result
                else:
                    error   = Response.make_error(error_message = "password mismatch", error_code = 200, display_message = "Oops something went wrong !")
                    return error
            else:
                error   = Response.make_error(error_message = "account does not exist", error_code = 405, display_message = "Account does not exist")
                return error
        except Exception as e:
            logging.warning(e)
            if mycursor is not None:
                mycursor.close()
            error = Response.make_error(error_message = "system failure", error_code = 500, display_message = "Oops something went wrong !")
            return error

    # change password after forgetting
    @staticmethod
    def forgot_password_change(payload):
        mycursor    = None
        try:
            mydb, mycursor  = Sql.get_connection()
            new_password    = str(payload["new_password"])
            number          = str(payload["number"])
            sql_query       = "update users set password = %s where number = %s"
            val             = (new_password, number)
            mycursor.execute(sql_query, val)
            mydb.commit()
            result  = Response.make_result(result_message = "password updated", result_code = "200", display_message = "Password updated")
            return result
        except Exception as e:
            logging.warning(e)
            if mycursor is not None:
                mycursor.close()
            error = Response.make_error(error_message = "system failure", error_code = 500, display_message = "Oops something went wrong !")
            return error
