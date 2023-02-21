"""Module that launch webserver for backend based on Flask"""
# other libs
from flask import Flask, request, make_response
# my libs
from database.database import (
    prepareDataBase, userValidation, updateChat,                # specific functions
    updateVerificationCode, deleteVerificationCode, getVerificationCode,    # verif code funcs
    addUser, addWorkplace, addChannel, addUserToWorkplace,      # adding funcs
    
    getUserInfoByLogin, getUsersColumn, getLoginBySession,  # getting from user table funcs
    getUserWorkplacesColumn, getWorkplacesHTML,             # getting from userN_workplces table funcs
    getNameByWorkplaceID,                                   # getting from workplaces table funcs
    getChannelsHTML, getMessagesHtml,                       # getting from workplaceN_channels table funcs
                                                 
)
from myCommonFeatures import log, generateCode
from sender.emailSender import send_verification_code_email
from sender.telegramBot import send_verification_code_telegram


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


@app.route("/addWorkplace")
def newWorkplace():
    workplace_name = request.args.get("name")
    session_code = request.args.get("session")

    # session checking
    if session_code not in getUsersColumn(nameDB, 'session_code'):
        return generateResponse("Bad session code")

    login = getLoginBySession(nameDB, session_code)
    return generateResponse(addWorkplace(nameDB, workplace_name, login))


@app.route("/addChannel")
def newChannel():
    channel_name = request.args.get("name")
    workplace_id = request.args.get("workplace_id")
    session_code = request.args.get("session")

    # session checking
    if session_code not in getUsersColumn(nameDB, 'session_code'):
        return generateResponse("Bad session code")

    # user workspaces checking
    user_id = getUserInfoByLogin(nameDB, getLoginBySession(nameDB, session_code), 'id')
    if workplace_id not in getUserWorkplacesColumn(nameDB, user_id, 'global_id'):
        return generateResponse("No access")

    return generateResponse(addChannel(nameDB, channel_name, workplace_id))


@app.route("/getWorkplaces")
def sendWorkplaces():
    session_code = request.args.get("session")

    # session checking
    if session_code not in getUsersColumn(nameDB, 'session_code'):
        return generateResponse("Bad session code")
    
    user_id = getUserInfoByLogin(nameDB, getLoginBySession(nameDB, session_code), 'id')
    return generateResponse(getWorkplacesHTML(nameDB, user_id))


@app.route("/getChannels")
def sendWChannels():
    session_code = request.args.get("session")
    workplace_id = request.args.get("workplace_id")

    # session checking
    if session_code not in getUsersColumn(nameDB, 'session_code'):
        return generateResponse("Bad session code")
    
    # user workspaces checking
    user_id = getUserInfoByLogin(nameDB, getLoginBySession(nameDB, session_code), 'id')
    if workplace_id not in getUserWorkplacesColumn(nameDB, user_id, 'global_id'):
        return generateResponse("No access")

    return generateResponse(getChannelsHTML(nameDB, workplace_id))


@app.route("/getWorkplaceName")
def sendWorkplaceName():
    workplace_id = request.args.get("workplace_id")
    try:
        return generateResponse(getNameByWorkplaceID(nameDB, workplace_id))
    except:
        return generateResponse("Bad id")


@app.route("/getChat")
def sendChat():
    channel_id = request.args.get("channel_id")
    workplace_id = request.args.get("workplace_id")
    session_code = request.args.get("session")

    # session checking
    if session_code not in getUsersColumn(nameDB, 'session_code'):
        return generateResponse("Bad session code")
    
    # user workspaces checking
    user_id = getUserInfoByLogin(nameDB, getLoginBySession(nameDB, session_code), 'id')
    if workplace_id not in getUserWorkplacesColumn(nameDB, user_id, 'global_id'):
        return generateResponse("No access")
    
    return generateResponse(getMessagesHtml(nameDB, workplace_id, channel_id))


@app.route("/sendMessage")
def sendMessage():
    text = request.args.get("text")
    workplace_id = request.args.get("workplace_id")
    channel_id = request.args.get("channel_id")
    session_code = request.args.get("session")

    # session checking
    if session_code not in getUsersColumn(nameDB, 'session_code'):
        return generateResponse("Bad session code")
    
    # user workspaces checking
    login = getLoginBySession(nameDB, session_code)
    user_id = getUserInfoByLogin(nameDB, login, 'id')
    if workplace_id not in getUserWorkplacesColumn(nameDB, user_id, 'global_id'):
        return generateResponse("No access")

    nickname = getUserInfoByLogin(nameDB, login, 'nickname')
    updateChat(nameDB, workplace_id, channel_id, nickname, text)
    return generateResponse("Success")



@app.route("/joinWorkplace")
def joinWorkplace():
    workplace_id = request.args.get("workplace_id")
    session_code = request.args.get("session")

    # session checking
    if session_code not in getUsersColumn(nameDB, 'session_code'):
        return generateResponse("Bad session code")

    # user workspaces chacking
    user_id = getUserInfoByLogin(nameDB, getLoginBySession(nameDB, session_code), 'id')
    if workplace_id in getUserWorkplacesColumn(nameDB, user_id, 'global_id'):
        return generateResponse("You are already in workplace!")
    
    return generateResponse(addUserToWorkplace(nameDB, getNameByWorkplaceID(nameDB, workplace_id), user_id))


if __name__ == '__main__':
    run_webserver()