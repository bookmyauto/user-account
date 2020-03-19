"""
                Description : main file for user account service
                Author      : Rahul Tudu
"""
from    flask   import make_response
from    flask   import Flask
from    flask   import request
from    otp     import Otp
from    create  import Create
import  requests
import  logging
import  json
# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       INITIALIZATION                                                                          #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
default_error = json.dumps(
    {"errorCode": 500, "errorMessage": "System failure", "displayMessage": "Oops something went wrong !"})
with app.app_context():
    default_error = make_response(default_error)
logging.info("user account started")


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       CHECK IF WORKING                                                                        #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
@app.route("/v1")
def working():
    return "user-account service running"


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       GETS OTP                                                                                #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
@app.route("/v1/otp", methods=["GET"])
def otp_create():
    try:
        if request.method == "GET":
            number = request.args["number"]
            logging.info("  Incoming request:\n" + str(request.args))
            response = json.dumps(Otp.create_otp(number))
            logging.info("  Response:\n" + str(response))
            with app.app_context():
                response = make_response(response)
            return response
    except RuntimeError as e:
        logging.critical("  Failure in v1/otp with error: " + str(e))
        return default_error


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       OTP VERIFY RELATED ACTIONS                                                              #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
@app.route("/v1/otp/verify", methods=["GET"])
def otp_verify():
    try:
        if request.method == "GET":
            number = request.args["number"]
            logging.info("  Incoming request:\n" + str(request.args))
            user_otp = request.args["otp"]
            response = json.dumps(Otp.verify_otp(number, user_otp))
            logging.info("  Response:\n" + str(response))
            with app.app_context():
                response = make_response(response)
            token    = requests.get("http://127.0.0.1:8080/v1/getJWT?number=" + str(number))
            token    = token.json()
            if token["data"]["token"] == "":
                raise ValueError
            else:
                response.headers["token"] = token["data"]["token"]
            return response
    except RuntimeError as e:
        logging.critical("  Failure in v1/otp/verify with error: " + str(e))
        return default_error


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       CREATION OF USER                                                                        #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
@app.route("/v1/createuser", methods=["GET", "POST"])
def createuser():
    try:
        if request.method == "GET":
            logging.info("  Incoming request:\n" + str(request.args))
            user_number = request.args["number"]
            response = Create.check_user_repetition(user_number)
            logging.info("  Response:\n" + str(response))
            with app.app_context():
                response = make_response(response)
            return response
        if request.method == "POST":
            logging.info("  Incoming request:\n" + str(request.args))
            user_name = request.form["name"]
            user_number = request.form["number"]
            response = Create.create_user(user_number, user_name)
            logging.info("  Response:\n" + str(response))
            with app.app_context():
                response = make_response(response)
            return response
    except RuntimeError as e:
        logging.critical("  Failure in v1/createuser with error: " + str(e))
        return default_error


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       UPDATE USER                                                                             #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
@app.route("/v1/updateuser", methods=["POST"])
def updateuser():
    try:
        if request.method == "POST":
            logging.info("  Incoming request:\n" + str(request.form))
            number = request.form["number"]
            name = request.form["name"]
            photo_link = request.form["profile_pic_link"]
            response = Create.update_user(number, name, photo_link)
            logging.info("  Response:\n" + str(response))
            with app.app_context():
                response = make_response(response)
            return response
    except RuntimeError as e:
        logging.critical("  Failure in v1/updateuser with error: " + str(e))
        return default_error


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       LOGIN AND RETURN JWT                                                                    #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
@app.route("/v1/login", methods=["GET"])
def login():
    try:
        if request.method == "GET":
            logging.info("  Incoming request:\n" + str(request.args))
            number = request.args["number"]
            response = requests.get("https://127.0.0.1:8080/v1/getJWT?number=" + str(number))
            response = response.json()
            if response["data"]["token"] == "":
                raise ValueError
            else:
                logging.info("  Response:\n" + str(response))
                return response
    except RuntimeError as e:
        logging.critical("  Failure in v1/login with error: " + str(e))
        return default_error


# --------------------------------------------------------------------------------------------------------------------------------------------- #
#                                                       THE MAIN FUNCTION                                                                       #
# --------------------------------------------------------------------------------------------------------------------------------------------- #
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=7002)
