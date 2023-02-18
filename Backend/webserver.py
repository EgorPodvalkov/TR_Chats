"""Module that launch webserver for backend based on Flask"""
# other libs
from flask import Flask, request, make_response
from datetime import timedelta
# my libs
from database import prepareDataBase, userValidation, updateVerificationCode, deleteVerificationCode, getVerificationCode, addUser, getUserInfoByLogin, getLoginBySession, getUsersColumn
from myCommonFeatures import log, generateCode
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


@app.route("/getVerifCodeReg")
def sendVerifCodeReg():
    authentication_name = request.args.get("authentication")
    code = generateCode(5)
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


@app.route("/getVerifCodeLog")
def sendVerifCodeLog():
    
    # login checking
    login = request.args.get("login")
    logins = getUsersColumn(nameDB, "login")
    if login not in logins:
        return generateResponse("No login")

    # password checking
    password = request.args.get("password")
    if password != getUserInfoByLogin(nameDB, login, "password"):
        return generateResponse("Bad password")
    
    # code sending
    authentication_name = getUserInfoByLogin(nameDB, login, 'authentication_name')
    code = generateCode(5)
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

    # verif code checking
    if verification_code != getVerificationCode(nameDB, authentication_name):
        return generateResponse("verif code mismatch")
    
    addUser(nameDB, login, nickname, password, authentication_name)
    deleteVerificationCode(nameDB, authentication_name)
    return generateResponse("account created," + getUserInfoByLogin(nameDB, login, 'session_code'))


@app.route("/logIn")
def logIn():
    
    # login checking
    login = request.args.get("login")
    logins = getUsersColumn(nameDB, "login")
    if login not in logins:
        return generateResponse("No login")

    # password checking
    password = request.args.get("password")
    if password != getUserInfoByLogin(nameDB, login, "password"):
        return generateResponse("Bad password")
    
    # verif code checking
    verification_code = request.args.get("verification")
    authentication_name = getUserInfoByLogin(nameDB, login, "authentication_name")
    if verification_code != getVerificationCode(nameDB, authentication_name):
        return generateResponse("Bad verif")

    deleteVerificationCode(nameDB, authentication_name)
    return generateResponse("login successfully," + getUserInfoByLogin(nameDB, login, 'session_code'))


@app.route("/checkSession")
def checkSession():
    session_code = request.args.get("session")
    login = getLoginBySession(nameDB, session_code)
    if login == None:
        return generateResponse("None")


    return generateResponse()

run_webserver()