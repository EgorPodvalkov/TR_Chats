'''Module that manages editions in database\n
Main functions:\n
- prepareDataBase, initConnection, initUserWorkplacesTable, initWorkplaceChannelsTable'''
# other libs
import sqlite3
# my libs
from myCommonFeatures import log


def prepareDataBase(nameDB: str):
    '''Prepares database'''
    connection = initConnection(nameDB)
    initTables(connection)
    connection.close()

# Inition block
def initConnection(nameDB: str):
    '''Tries to init connection by the path'''
    connection = None
    try:
        connection = sqlite3.connect(nameDB)
    except sqlite3.Error as err:
        log(f"Error! {err} \n Conection failed!")
    return connection


def initTables(connection: str):
    '''Creates new tables for users, verification and workplaces if they not exists'''
    try:

        # user table creation (id, login, nickname, password, authentication_method, authentication_name, session_code)
        sql = """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY, 
            login TEXT NOT NULL, 
            nickname TEXT NOT NULL, 
            password TEXT NOT NULL, 
            authentication_method TEXT NOT NULL, 
            authentication_name TEXT NOT NULL, 
            session_code TEXT NOT NULL
        )"""
        connection.execute(sql)

        # verification table creation (id, authentication_name, verification_code)
        sql = """CREATE TABLE IF NOT EXISTS verification(
            id INTEGER PRIMARY KEY, 
            authentication_name TEXT NOT NULL, 
            verification_code TEXT
        )"""
        connection.execute(sql)

        # workplaces table creation (id, workplace_name, creator_name)
        sql = """CREATE TABLE IF NOT EXISTS workplaces(
            id INTEGER PRIMARY KEY, 
            workplace_name TEXT NOT NULL, 
            creator_name TEXT NOT NULL
        )"""
        connection.execute(sql)

        log("Tables [blue]users[/blue], [blue]verification[/blue], [blue]workplaces[/blue] created (if they not exist)!")
    except:
        log("Something wrong!\nFailed to create tables [blue]users[/blue], [blue]verification[/blue] and [blue]workplaces[/blue]!")


def initUserWorkplacesTable(nameDB: str, user_id: str):
    '''Creates new table for user`s workplaces by his id'''
    connection = initConnection(nameDB)
    
    try:
        # user{user_id}_workplaces table creation (id, global_id, workplace_name)
        sql = f"""CREATE TABLE IF NOT EXISTS user{user_id}_workplaces(
            id INTEGER PRIMARY KEY, 
            global_id TEXT NOT NULL, 
            workplace_name TEXT NOT NULL
        )"""
        connection.execute(sql)
        connection.close()

        log(f"Table [blue]user{user_id}_workplaces[/blue] created!")
    except:
        log(f"Something wrong!\nFailed to create tables [blue]user{user_id}_workplaces[/blue]!")


def initWorkplaceChannelsTable(nameDB: str, workplace_id: str):
    '''Creates new table for workplace`s channels by workplace_id'''
    connection = initConnection(nameDB)

    try:
        # workplace{workplace_id}_channels table creation (id, name , chat)
        sql = f"""CREATE TABLE IF NOT EXISTS workplace{workplace_id}_channels(
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL, 
            chat TEXT
        )"""
        connection.execute(sql)
        connection.close()

        log(f"Table [blue]workplace{workplace_id}_channels[/blue] created!")
    except:
        log(f"Something wrong!\nFailed to create tables [blue]workplace{workplace_id}_channels[/blue]!")
