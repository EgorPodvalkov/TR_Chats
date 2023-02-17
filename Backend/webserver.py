"""Module that launch webserver for backend based on Flask"""
# other libs
from flask import Flask, request, make_response
# my libs
from database import prepareDataBase, userValidation, updateVerificationCode, getVerificationCode, addUser
from myCommonFeatures import log, generateVerifCode
from emailSender import send_verification_code_email
from telegramBot import send_verification_code_telegram


nameDB = "TRChat.db"
prepareDataBase(nameDB)

app = Flask("TR chat back")


def run_webserver():
    '''Runs backend webserver on Flask'''
    app.run(host = "0.0.0.0", port = 8081)


def generateResponse(data = ""):
    """Returns response with data"""
    response = make_response(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/checkVerlidation")
def checkVerlidation():
    """Returns response with result of verification"""
    login = request.args.get("login")
    authentication_name = request.args.get("authentication")

    return generateResponse(userValidation(nameDB, login, authentication_name))


@app.route("/getVerifCode")
def sendVerifCode():
    authentication_name = request.args.get("authentication")
    code = generateVerifCode()
    try:
        if "@" in authentication_name:
            send_verification_code_email(authentication_name, code)
            updateVerificationCode(nameDB, authentication_name, code)
            return generateResponse("Email sended")
        else:
            send_verification_code_telegram(authentication_name, code)
            updateVerificationCode(nameDB, authentication_name, code)
            return generateResponse("Tg sended")
    except:
        return generateResponse("Error")


@app.route("/createAccount")
def addAccount():
    login = request.args.get("login")
    nickname = request.args.get("nickname")
    password = request.args.get("password")
    authentication_name = request.args.get("authentication")
    verification_code = request.args.get("verification")

    if verification_code == getVerificationCode(nameDB, authentication_name):
        addUser(nameDB, login, nickname, password, authentication_name)
        res = generateResponse("account created")
        res.set_cookie("session", "login", max_age = 60 * 60 * 24 * 100)
        return res
    else:
        return generateResponse("verif code mismatch")



run_webserver()