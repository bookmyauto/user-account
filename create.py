import  logging
from    sql import Sql
from    response import Response


class Create:

    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                   CHECK IF USER IS BEING REPEATED
    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def check_user_repetition(number):
        conn    = None
        try:
            conn, cur       = Sql.get_connection()
            logging.debug("  " + str(number) + ":  Connection and cursor received")
            
            # check from db
            sql_query       = "select count(number) from users where number = '{0}'"
            cur.execute(sql_query.format(number))
            data            = cur.fetchone()
            logging.debug("  " + str(number) + ":  Count is: " + str(data[0]))
            if int(data[0]) == 0:
                conn.close()
                result  = Response.make_response(200, "Phone number does not exist", "Phone number does not exist", present=0)
                return result
            result      = Response.make_response(200, "Phone number already exists", "Phone number already exists", present=1)
            conn.close()
            logging.debug("  " + str(number) + ":  Connection closed")
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("  " + str(number) + ":  Error in checking user repetition: " + str(e))
            error = Response.make_response(500, "System failure", "Oops something went wrong !")
            return error

    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    #                                                   CREATE USER                                                                                 #
    # --------------------------------------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def create_user(number, name):
        conn    = None
        try:
            conn, cur       = Sql.get_connection()
            logging.debug("  " + str(number) + ":  Connection and cursor received")
            
            # insert in db
            sql_query       = "insert into users (number, name) values ('{0}', '{1}')"
            cur.execute(sql_query.format(number, name))
            conn.commit()
            logging.debug("  " + str(number) + ":  User successfully inserted in users table")
            result          = Response.make_response(201, "Account created", "Your account has been created")
            conn.close()
            return result
        except Exception as e:
            if conn is not None:
                conn.close()
            logging.error("  " + str(number) + ":  Error in creating user: " + str(e))
            error = Response.make_response(500, "System failure", "Oops something went wrong !")
            return error
