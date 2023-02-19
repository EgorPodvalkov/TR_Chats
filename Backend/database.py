'''
Module that manages databases\n
Main functions are prepareDataBase, addUser, getUsersColumn, getUserInfoByLogin, userValidation, 
getLoginBySession, updateVerificationCode, deleteVerificationCode,
'''
# other libs
import sqlite3
from datetime import datetime
from typing import Literal
from html import escape as saveHTML
# my libs
from myCommonFeatures import log, generateCode


def prepareDataBase(nameDB: str):
    '''Prepares database'''
    connection = initConnection(nameDB)
    initTables(connection)
    connection.close()

# inition block


def initConnection(nameDB: str):
    '''Tries to init connection by the path'''
    connection = None
    try:
        connection = sqlite3.connect(nameDB)
        log("Connection established!")
    except sqlite3.Error as err:
        log(f"Error! {err} \n Conection failed!")
    return connection


def initTables(connection: str):
    '''Tries to create new tables for users, verefication and workplaces'''
    sql = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, login TEXT NOT NULL, nickname TEXT NOT NULL, password TEXT NOT NULL, authentication_method TEXT NOT NULL, authentication_name TEXT NOT NULL, session_code TEXT NOT NULL)"
    connection.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS verification( id INTEGER PRIMARY KEY, authentication_name TEXT NOT NULL, verification_code TEXT)"
    connection.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS workplaces( id INTEGER PRIMARY KEY, workplace_name TEXT NOT NULL, creator_name TEXT NOT NULL)"
    connection.execute(sql)
    log("Tables [blue]users[/blue], [blue]verification[/blue], [blue]workplaces[/blue] created (if they not exist)!")



def initUserWorkplacesTable(nameDB: str, user_id: str):
    '''Creates new table with all workplaces of user'''
    connection = initConnection(nameDB)
    sql = f"CREATE TABLE IF NOT EXISTS user{user_id}_workplaces( id INTEGER PRIMARY KEY, global_id TEXT NOT NULL, workplace_name TEXT NOT NULL)"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Table [blue]user{user_id}_workplaces[/blue] created!")


def initWorkplaceChannelsTable(nameDB: str, workplace_id: str):
    '''Creates new table with all workplaces of user'''
    connection = initConnection(nameDB)
    sql = f"CREATE TABLE IF NOT EXISTS workplace{workplace_id}_channels( id INTEGER PRIMARY KEY, name TEXT NOT NULL, chat TEXT)"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Table [blue]workplace{workplace_id}_channels[/blue] created!")


# change data block

def addUser(nameDB: str, login: str, nickname: str, password: str, authentication_name: str) -> str:
    """
    Adds user to user table and authentication name to verification table if data is valid\n
    Returns 'Added' if added\n
    Returns 'Login is already taken' if login is taken\n
    Returns 'Authentication name is already taken' if authentication_name is taken
    """
    valid = userValidation(nameDB, login, authentication_name)
    if valid != 'Validate':
        return valid
    
    if "@" in authentication_name:
        authentication_method = "Email"
    else:
        authentication_method = "Telegram"

    session_code = generateCode(30)

    connection = initConnection(nameDB)
    sql = f"INSERT INTO users(`login`, `nickname`, `password`, `authentication_method`, `authentication_name`, `session_code`) VALUES('{login}', '{nickname}', '{password}', '{authentication_method}', '{authentication_name}', '{session_code}')"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"User [yellow]{login}[/yellow] added to users table")

    initUserWorkplacesTable(nameDB, getUserInfoByLogin(nameDB, login, "id"))

    return 'Added'


def addWorkplace(nameDB: str, workplace_name: str, creator_name: str) -> str:
    """
    Adds workplace to workplaces table
    Returns 'Added' if added\n
    Returns 'Workplace name is already taken' if name is taken
    """
    
    # workplace name checking
    if workplace_name in getWorkplaceNames(nameDB):
        return "Workplace name is already taken"

    connection = initConnection(nameDB)
    sql = f"INSERT INTO workplaces(`workplace_name`, `creator_name`) VALUES('{workplace_name}', '{creator_name}')"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Workplace [yellow]{workplace_name}[/yellow] added to workplaces table")

    global_id = getIdByWorkplaceName(nameDB, workplace_name)
    initWorkplaceChannelsTable(nameDB, global_id)

    addUserToWorkplace(nameDB, workplace_name, getUserInfoByLogin(nameDB, creator_name, "id"))
    return "Added"


def addChannel(nameDB: str, channel_name: str, workplace_id: str) -> str:
    """
    Adds channel to workplacesN_channels table by workplace_id
    Returns 'Added' if added\n
    Returns 'Channel name is already taken' if name is taken
    """
    
    # channel name checking
    if channel_name in getWorkplaceChannelsColumn(nameDB, workplace_id, 'name'):
        return "Channel name is already taken"

    connection = initConnection(nameDB)
    sql = f"INSERT INTO workplace{workplace_id}_channels(`name`) VALUES('{channel_name}')"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Workplace [yellow]{channel_name}[/yellow] added to workplaces{workplace_id}_channels table")
    return "Added"


def addUserToWorkplace(nameDB: str, workplace_name: str, user_id: str) -> str:
    """Adds workplace to specified user_workplaces table
    Returns 'Success!'"""

    global_id = getIdByWorkplaceName(nameDB, workplace_name)

    connection = initConnection(nameDB)
    sql = f"INSERT INTO user{user_id}_workplaces(`global_id`, `workplace_name`) VALUES('{global_id}', '{workplace_name}')"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Workplace [yellow]{workplace_name}[/yellow] added to user{user_id}_workplaces table")
    return "Success!"


def updateChat(nameDB: str, workplace_id: str, channel_id: str, nickname: str, text: str):
    '''Adds message to chat column in workplaceN_channels table '''
    time = datetime.now().strftime("%H:%M")
    messages = getMessages(nameDB, workplace_id, channel_id)
    messages += f"<name>{saveHTML(nickname)}</name><time>{time}</time><br><text>{saveHTML(text)}</text><br>"

    connection = initConnection(nameDB)
    sql = f"UPDATE workplace{workplace_id}_channels SET chat = '{messages}' WHERE id = '{channel_id}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()



def updateVerificationCode(nameDB: str, authentication_name: str, verification_code: str):
    '''Updates verification code in verification table'''
    connection = initConnection(nameDB)
    sql = f"UPDATE verification SET verification_code = '{verification_code}' WHERE authentication_name = '{authentication_name}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()


def deleteVerificationCode(nameDB: str, authentication_name: str):
    '''Deletes verification code in verification table'''
    connection = initConnection(nameDB)
    sql = f"UPDATE verification SET verification_code = NULL WHERE authentication_name = '{authentication_name}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()


# getting data block

def userValidation(nameDB: str, login: str, authentication_name: str) -> str:
    """
    Returns 'Validate' if user`s data is valid\n
    Returns 'Login is already taken' if login is taken\n
    Returns 'Authentication name is already taken' if authentication_name is taken
    """

    if login in getUsersColumn(nameDB, "login"):
        log(f"Login [yellow]{login}[/yellow] is [red]already taken[/red]")
        return 'Login is already taken'

    if authentication_name in getUsersColumn(nameDB, "authentication_name") and authentication_name != "419047817":
        log(f"Authentication name [yellow]{authentication_name}[/yellow] is [red]already taken[/red]")
        return 'Authentication name is already taken'

    if authentication_name not in getAuthenticationNames(nameDB):
        connection = initConnection(nameDB)
        sql = f"INSERT INTO verification(`authentication_name`) VALUES('{authentication_name}')"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()

    log(f"User [yellow]{login}[/yellow] is [green]valid[/green]")
    return 'Validate'

    # users

def getUsersColumn(nameDB: str, column: Literal['id', 'login', 'nickname', 'password', 'authentication_method', 'authentication_name', 'session_code']) -> list[str]:
    """Returns list of specified column"""
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM users"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()        
    return [str(row[0]) for row in rows]


def getUserInfoByLogin(nameDB: str, login:str, column: Literal['id', 'login', 'nickname', 'password', 'authentication_method', 'authentication_name', 'session_code']) -> str:
    """Returns specified info by user login"""
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM users WHERE login = '{login}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return str(result)


def getLoginBySession(nameDB: str, session_code: str) -> str:
    """Returns login by session"""
    connection = initConnection(nameDB)
    sql = f"SELECT login FROM users WHERE session_code = '{session_code}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    try:
        result = cursor.fetchall()[0][0]
        connection.close()
        return result
    except:
        return None

    # verification

def getAuthenticationNames(nameDB: str) -> list[str]:
    """Returns authentication names from verification table"""
    connection = initConnection(nameDB)
    sql = f"SELECT authentication_name FROM verification"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()        
    return [row[0] for row in rows]


def getVerificationCode(nameDB: str, authentication_name: str) -> str:
    """Returns verification_code by authentication_name from verification table"""
    connection = initConnection(nameDB)
    sql = f"SELECT verification_code FROM verification WHERE authentication_name = '{authentication_name}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return result

    # workplaces
def getWorkplaceNames(nameDB: str) -> list[str]:
    """Returns list of workplace names"""
    connection = initConnection(nameDB)
    sql = f"SELECT workplace_name FROM workplaces"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()        
    return [row[0] for row in rows]


def getIdByWorkplaceName(nameDB: str, workplace_name:str) -> str:
    """Returns id by workplace_name from workplaces table"""
    connection = initConnection(nameDB)
    sql = f"SELECT id FROM workplaces WHERE workplace_name = '{workplace_name}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return str(result)

def getNameByWorkplaceID(nameDB: str, workplace_id:str) -> str:
    """Returns name by id from workplaces table"""
    connection = initConnection(nameDB)
    sql = f"SELECT workplace_name FROM workplaces WHERE id = '{workplace_id}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return str(result)

    # userN_workplaces
def getUserWorkplacesColumn(nameDB: str, user_id: str, column: Literal['id', 'global_id', 'workplace_name']) -> list[str]:
    '''Return list of specified column from userN_workplaces by user_id'''
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM user{user_id}_workplaces"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()        
    return [row[0] for row in rows]


def getWorkplacesHTML(nameDB: str, user_id: str) -> str:
    '''Returns html code with workplaces buttons'''
    names = getUserWorkplacesColumn(nameDB, user_id, 'workplace_name')
    ids = getUserWorkplacesColumn(nameDB, user_id, 'global_id')

    # user haven`t workplaces
    if len(names) == 0:
        return '<button onclick="show_workplaces_adder()">Add Workplace</button>'

    result = ""
    for index, id in enumerate(ids):
        result += f"<button onclick='getChannels({id})'>{saveHTML(names[index])}</button>"
    return result

    # workspaceN_channels
def getWorkplaceChannelsColumn(nameDB: str, workplace_id: str, column: Literal['id', 'name', 'chat']) -> list[str]:
    '''Return list of specified column from workspaceN_channels table by workplace_id'''
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM workplace{workplace_id}_channels"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()        
    return [row[0] for row in rows]


def getChannelsHTML(nameDB: str, workplace_id: str) -> str:
    '''Returns html code with channels buttons'''
    names = getWorkplaceChannelsColumn(nameDB, workplace_id, 'name')
    ids = getWorkplaceChannelsColumn(nameDB, workplace_id, 'id')

    name = getNameByWorkplaceID(nameDB, workplace_id)


    result = f'''
        <h3>
            {name}
            <button onclick="show_channels_adder()" class="add_channel" >+</button>
        </h3>
        <div class="channels_area">
    '''

    # workplace haven`t channels
    if len(names) == 0:
        return result + '<button onclick="show_channels_adder()">Add Channel</button></div>'

    for index, id in enumerate(ids):
        result += f"<button onclick='getChat({id}, true)'>{saveHTML(names[index])}</button>"
    return result + "</div>"


def getMessages(nameDB: str, workplace_id: str, channel_id: str) -> str:
    '''Returns chat from workplaceN_channels by channel_id'''
    connection = initConnection(nameDB)
    sql = f"SELECT chat FROM workplace{workplace_id}_channels WHERE id = '{channel_id}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return str(result) if result else ""


def getWorkplaceNChannelName(nameDB: str, workplace_id: str, channel_id: str) -> str:
    '''Returns chat name by id in workplaceN_channel table'''
    connection = initConnection(nameDB)
    sql = f"SELECT name FROM workplace{workplace_id}_channels WHERE id = '{channel_id}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return result



def getMessagesHtml(nameDB: str, workplace_id: str, channel_id: str) -> str:
    '''Returns Html code with chat'''
    channel_name = getWorkplaceNChannelName(nameDB, workplace_id, channel_id)
    result = f'''
        <h3>{channel_name}</h3>
        <div class="chat_area">
            <messages class="messages">
    '''
    result += getMessages(nameDB, workplace_id, channel_id)
    result += '''
            </messages>
        </div>
        '''
    return result

# nameDB = "TRChat.db"
# prepareDataBase(nameDB)
# addUser(nameDB, "kuka", "kokamd", "password", "312412113")
# addUser(nameDB, "kuka1221", "kokamd", "password", "312412231213")
# addUser(nameDB, "kuka11", "kokamd", "password", "3124123")
# addUser(nameDB, "kuka2", "kokamd", "password", "312412321")

# log(getAuthenticationNames(nameDB))

# log(getVerificationCode(nameDB, getUserInfoByLogin(nameDB, "kuka", "authentication_name")))
# log(getVerificationCode(nameDB, getUserInfoByLogin(nameDB, "kuka11", "authentication_name")))