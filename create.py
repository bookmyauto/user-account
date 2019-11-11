import  logging
from    bson import ObjectId
from    sql import Sql
from    response import Response


class Create:

    @staticmethod
    def check_user_repetition(number):
        myconnection    = None
        try:
            myconnection, mycursor  = Sql.get_connection()
            logging.debug("Connection and cursor received")
            # check from db
            sql_query       = "select u_id from users where number = \'" + str(number) + "\'"
            mycursor.execute(sql_query)
            data            = mycursor.fetchone()
            logging.debug("Length of data is: " + str(len(data)))
            if len(data) == 0:
                result = Response.make_result(result_code=200, result_message="Phone number does not exist",
                                              display_message="Phone number does not exist",
                                              present=0)
                return result
            result = Response.make_result(result_code=200, result_message="Phone number already exists",
                                          display_message="Phone number already exists",
                                          present=1)
            myconnection.close()
            logging.debug("Connection closed")
            return result
        except Exception as e:
            if myconnection is not None:
                myconnection.close()
            logging.error("Error in checking user repetition: " + str(e) + " |for number: " + str(number))
            error = Response.make_error(error_message="system failure", error_code=500, display_message="Oops something went wrong !")
            return error

    @staticmethod
    def create_user(name, number, password):
        myconnection    = None
        try:
            myconnection, mycursor  = Sql.get_connection()
            logging.debug("Connection and cursor received")
            u_id                    = str(ObjectId())
            # insert in db
            sql_query       = "insert into users (u_id, name, number, password) values (%s, %s, %s, %s)"
            val             = (u_id, name, number, password)
            mycursor.execute(sql_query, val)
            myconnection.commit()
            myconnection.close()
            logging.debug("User successfully inserted in table and generated u_id is: " + str(u_id))
            result          = Response.make_result(result_code = 201, result_message = "Account created",
                                                   display_message = "Your account has been created",
                                                   u_id = u_id)
            return result
        except Exception as e:
            if myconnection is not None:
                myconnection.close()
            logging.error("Error in creating user: " + str(e) + " |for number: " + str(number))
            error = Response.make_error(error_message = "system failure", error_code = 500, display_message = "Oops something went wrong !")
            return error
