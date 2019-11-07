import logging
from sql import Sql
from response import Response


class Password:

    # change password here
    @staticmethod
    def change_password(number, old_password, new_password):
        myconnecton    = None
        try:
            myconnecton, mycursor = Sql.get_connection()
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
                    myconnecton.commit()
                    result  = Response.make_result(result_messagee = "password updated", result_ode = "201", result_message = "Password updated")
                    return result
                else:
                    error   = Response.make_error(error_message = "password mismatch", error_code = 200, display_message = "Oops something went wrong !")
                    return error
            else:
                error   = Response.make_error(error_message = "account does not exist", error_code = 405, display_message = "Account does not exist")
                return error
        except Exception as e:
            if myconnecton is not None:
                myconnecton.close()
            logging.warning("Error in change password: " + str(e) + " |for number: " + str(number))
            error = Response.make_error(error_message = "system failure", error_code = 500, display_message = "Oops something went wrong !")
            return error

    # change password after forgetting
    @staticmethod
    def forgot_password_change(number, new_password):
        myconnection    = None
        try:
            myconnection, mycursor  = Sql.get_connection()
            sql_query       = "update users set password = %s where number = %s"
            val             = (new_password, number)
            mycursor.execute(sql_query, val)
            myconnection.commit()
            result  = Response.make_result(result_message = "password updated", result_code = "200", display_message = "Password updated")
            return result
        except Exception as e:
            if myconnection is not None:
                myconnection.close()
            logging.warning("Error in forgot password: " + str(e) + " |for number: " + str(number))
            error = Response.make_error(error_message = "system failure", error_code = 500, display_message = "Oops something went wrong !")
            return error
