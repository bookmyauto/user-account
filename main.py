from flask      import Flask
from flask      import request
from otp        import Otp
from password   import Password
from create     import Create
import logging
import json

logging.basicConfig(level=logging.DEBUG)
app             = Flask(__name__)

default_error   = json.dumps({"error_code": 500, "error_message": "Internal server error", "disaply_message": ""})


@app.route("/")
def working():
    return "user-account service running"


# otp related actions
@app.route("/v1/otp", methods=["GET"])
def otp():
    try:
        if request.method == "GET":
            action  = request.form["action"]
            number  = request.form["number"]
            if action == "create":
                response = json.dumps(Otp.create_otp(number))
                return response
            if action == "verify":
                user_otp    = request.form["otp"]
                response    = json.dump(Otp.verify_otp(number, user_otp))
                return response
    except RuntimeError as e:
        logging.critical("failure in v1/otp with error: " + str(e) + " |for request: " + str(request.form))
        return default_error


# password related actions
@app.route("/v1/password", methods = ["POST"])
def password():
    try:
        if request.method == "POST":
            action          = request.form["action"]
            number          = request.form["number"]
            new_password    = request.form["new_password"]
            if action == "change":
                old_password    = request.form["old_password"]
                response        = Password.change_password(number, old_password, new_password)
                return response
            if action == "forgot":
                response        = Password.forgot_password_change(number, new_password)
                return response
    except RuntimeError as e:
        logging.critical("failure in v1/password with error: " + str(e) + " |for request: " + str(request.form))
        return default_error


# creation of user is handled here
@app.route("/v1/createuser", methods = ["GET", "POST"])
def createuser():
    try:
        if request.method == "GET":
            logging.debug("GET request received in createuser with request:\n" + str(dict(request.form)))
            user_number     = request.form["number"]
            response        = Create.check_user_repetition(user_number)
            logging.debug("createuser returned:\n" + str(dict(request.form)))
            return response
        if request.method == "POST":
            logging.debug("POST request received in createuser with request:\n" + str(request.form))
            user_name       = request.form["name"]
            user_number     = request.form["number"]
            user_password   = request.form["password"]
            response        = Create.create_user(user_name, user_number, user_password)
            logging.debug("createuser returned:\n" + str(dict(request.form)))
            return response
    except RuntimeError as e:
        logging.critical("failure in v1/createuser with error: " + str(e) + " |for request: " + str(dict(request.form)))
        return default_error


if __name__ == '__main__':
    app.run(debug=True)
