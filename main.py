from flask      import Flask
from flask      import request
from flask_api  import status
from otp        import Otp
from create     import Create
import logging
import json

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

logging.basicConfig(level=logging.ERROR)
app             = Flask(__name__)

default_error   = json.dumps({"errorCode": 500, "errorMessage": "System failure", "displayMessage": "Oops something went wrong !"})

logging.info("python code started")
        
@app.route("/v1")
def working():
    return {"response":"user-account service running"}


# otp related actions
@app.route("/v1/otp", methods=["GET"])
def otp():
    try:
        if request.method == "GET":
            number  = request.args["number"]
            logging.debug("incoming request: number = " + str(number))
            if "otp" not in request.form:
                response = json.dumps(Otp.create_otp(number))
                return response
            else:
                user_otp    = request.args["otp"]
                logging.debug("incoming request: otp = " + str(otp))
                response    = json.dumps(Otp.verify_otp(number, user_otp))
                return response
    except RuntimeError as e:
        logging.critical("failure in v1/otp with error: " + str(e))
        return default_error

# creation of user is handled here
@app.route("/v1/createuser", methods = ["GET", "POST"])
def createuser():
    try:
        if request.method == "GET":
            logging.debug("incoming GET request: " + str(dict(request.args)))
            user_number     = request.args["number"]
            response        = Create.check_user_repetition(user_number)
            logging.debug("createuser returned: " + str(response))
            return response
        if request.method == "POST":
            logging.debug("incoming POST request: " + str(request.form))
            user_name       = request.form["name"]
            user_number     = request.form["number"]
            response        = Create.create_user(user_number, user_name)
            logging.debug("createuser returned:\n" + str(response))
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/createuser with error: " + str(e))
        return default_error

@app.route("/v1/updateuser", methods = ["POST"])
def updateuser():
    try:
        if request.method == "POST":
            number      = request.form["number"]
            name        = request.form["name"]
            photo_link  = request.form["profile_pic_link"]
            response    = Create.update_user(number, name, photo_link)
            logging.debug("Responded to update user request")
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/updateuser with error: " + str(e) + " |for request: " + str(dict(request.form)))
        return default_error


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7002, ssl_context='adhoc')
