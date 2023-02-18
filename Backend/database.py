'''
Module that manages databases\n
Main functions are prepareDataBase, addUser, getUsersColumn, getUserInfoByLogin, userValidation, 
getLoginBySession, updateVerificationCode, deleteVerificationCode
'''
# other libs
import sqlite3
from datetime import datetime
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


def initWorkplaceChanelsTable(nameDB: str, workplace_id: str):
    '''Creates new table with all workplaces of user'''
    connection = initConnection(nameDB)
    sql = f"CREATE TABLE IF NOT EXISTS workplace{workplace_id}_chanels( id INTEGER PRIMARY KEY, name TEXT NOT NULL, chat TEXT)"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Table [blue]workplace{workplace_id}_chanels[/blue] created!")


# change data block

def addUser(nameDB: str, login: str, nickname: str, password: str, authentication_name: str):
    """
    Adds user to user table and authentication name to verification table if data is valid\n
    Returns 'Added' if added\n
    Returns 'Login is already taken' if login is taken\n
    Returns 'Authentication name is already taken' if authentication_name is taken
    """
    valid = userValidation(nameDB, login, authentication_name)
    if valid == 'Validate':
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
    else:
        return valid


def addWorkplace(nameDB: str, workplace_name: str, creator_name: str):
    """Adds workplace to workplaces table"""
    
    # workplace name checking
    if workplace_name in getWorkplaceNames(nameDB):
        return "Workplace name is already taken"

    connection = initConnection(nameDB)
    sql = f"INSERT INTO worplaces(`workplace_name`, `creator_name`) VALUES('{workplace_name}', '{creator_name}')"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Workplace [yellow]{workplace_name}[/yellow] added to workplaces table")

    global_id = getIdByWorkplaceName(nameDB, workplace_name)
    initWorkplaceChanelsTable(nameDB, global_id)

    addUserToWorkplace(nameDB, workplace_name, getUserInfoByLogin(nameDB, creator_name, "id"))

    


def addUserToWorkplace(nameDB: str, workplace_name: str, user_id: str):
    """Adds workplace to specified user_workplaces table"""

    global_id = getIdByWorkplaceName(nameDB, workplace_name)

    connection = initConnection(nameDB)
    sql = f"INSERT INTO user{user_id}_workplaces(`global_id`, `workplace_name`) VALUES('{global_id}', '{workplace_name}')"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    connection.close()
    log(f"Workplace [yellow]{workplace_name}[/yellow] added to user{user_id}_workplaces table")


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

def getUsersColumn(nameDB: str, column: str) -> list[str]:
    """Returns list of specified column\n
    Columns: 'id', 'login', 'nickname', 'password', 'authentication_method', 'authentication_name', 'session_code'"""
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM users"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()        
    return [str(row[0]) for row in rows]


def getUserInfoByLogin(nameDB: str, login:str, column: str) -> str:
    """Returns specified info by user login\n
    Columns: 'id', 'login', 'nickname', 'password', 'authentication_method', 'authentication_name', 'session_code'"""
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM users WHERE login = '{login}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return str(result)


def getLoginBySession(nameDB: str, session_code:str):
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


def getVerificationCode(nameDB: str, authentication_name:str) -> str:
    """Returns verification_code by authentication_name from verification table"""
    connection = initConnection(nameDB)
    sql = f"SELECT verification_code FROM verification WHERE authentication_name = '{authentication_name}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return result

    # workplace
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


# nameDB = "TRChat.db"
# prepareDataBase(nameDB)
# addUser(nameDB, "kuka", "kokamd", "password", "312412113")
# addUser(nameDB, "kuka1221", "kokamd", "password", "312412231213")
# addUser(nameDB, "kuka11", "kokamd", "password", "3124123")
# addUser(nameDB, "kuka2", "kokamd", "password", "312412321")

# log(getAuthenticationNames(nameDB))

# log(getVerificationCode(nameDB, getUserInfoByLogin(nameDB, "kuka", "authentication_name")))
# log(getVerificationCode(nameDB, getUserInfoByLogin(nameDB, "kuka11", "authentication_name")))