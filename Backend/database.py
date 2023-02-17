'''
Module that manages databases\n
Main functions are prepareDataBase, addUser, getUsersColumn, getUserInfoByLogin, userValidation
'''
# other libs
import sqlite3
from datetime import datetime
# my libs
from myCommonFeatures import log


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
    '''Tries to create new tables for users, verefication'''
    sql = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, login TEXT NOT NULL, nickname TEXT NOT NULL, password TEXT NOT NULL, authentication_method TEXT NOT NULL, authentication_name TEXT NOT NULL)"
    connection.execute(sql)
    sql = "CREATE TABLE IF NOT EXISTS verification( id INTEGER PRIMARY KEY, authentication_name TEXT NOT NULL, verification_code TEXT)"
    connection.execute(sql)


# change block

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

        connection = initConnection(nameDB)
        sql = f"INSERT INTO users(`login`, `nickname`, `password`, `authentication_method`, `authentication_name`) VALUES('{login}', '{nickname}', '{password}', '{authentication_method}', '{authentication_name}')"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        connection.close()
        log(f"User [yellow]{login}[/yellow] added to users table")
        return 'Added'
    else:
        return valid


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


# select block

def userValidation(nameDB: str, login: str, authentication_name: str) -> str:
    """
    Returns 'Validate' if user`s data is valid\n
    Returns 'Login is already taken' if login is taken\n
    Returns 'Authentication name is already taken' if authentication_name is taken
    """

    if login in getUsersColumn(nameDB, "login"):
        log(f"Login [yellow]{login}[/yellow] is [red]already taken[/red]")
        return 'Login is already taken'

    if authentication_name in getUsersColumn(nameDB, "authentication_name"):
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


def getUsersColumn(nameDB: str, column: str) -> list[str]:
    """Returns list of specified column\n
    Columns: 'login', 'nickname', 'password', 'authentication_method', 'authentication_name'"""
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM users"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()        
    return [row[0] for row in rows]


def getUserInfoByLogin(nameDB: str, login:str, column: str) -> str:
    """Returns specified info by user login\n
    Columns: 'login', 'nickname', 'password', 'authentication_method', 'authentication_name'"""
    connection = initConnection(nameDB)
    sql = f"SELECT {column} FROM users WHERE login = '{login}'"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()[0][0]
    connection.close()
    return result


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





# nameDB = "TRChat.db"
# prepareDataBase(nameDB)
# addUser(nameDB, "kuka", "kokamd", "password", "312412113")
# addUser(nameDB, "kuka1221", "kokamd", "password", "312412231213")
# addUser(nameDB, "kuka11", "kokamd", "password", "3124123")
# addUser(nameDB, "kuka2", "kokamd", "password", "312412321")

# log(getAuthenticationNames(nameDB))

# log(getVerificationCode(nameDB, getUserInfoByLogin(nameDB, "kuka", "authentication_name")))
# log(getVerificationCode(nameDB, getUserInfoByLogin(nameDB, "kuka11", "authentication_name")))