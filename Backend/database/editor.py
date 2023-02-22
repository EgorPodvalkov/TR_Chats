'''Module that manages data editions in database\n
Main functions:\n
- '''
#  other libs
from datetime import datetime
from html import escape as saveHTML
# my libs
from database.creator import initConnection, initUserWorkplacesTable, initWorkplaceChannelsTable
from database.extractor import (
        getUsersColumn, getUserFieldByLogin,
        getAuthenticationNames, 
        getWorkplaceColumn, getWorkplaceFieldByName,
        getWorkplaceChannelsColumn, getWorkplaceChannelsFieldByChannelId
    )
from myCommonFeatures import log, generateCode


# users
def addUser(nameDB: str, login: str, nickname: str, password: str, authentication_name: str) -> str:
    """
    Adds user to user table and authentication name to verification table if data is valid\n
    Returns:
    - 'Added' if added
    - 'Login is already taken' if login is taken
    - 'Error' if error
    """
    if userValidation(nameDB, login, authentication_name) == 'Login is already taken':
        return 'Login is already taken'
    
    if "@" in authentication_name:
        authentication_method = "Email"
    else:
        authentication_method = "Telegram"

    session_code = generateCode(40)

    connection = initConnection(nameDB)
    try:
        # inserting user to users table
        sql = f"INSERT INTO users(`login`, `nickname`, `password`, `authentication_method`, `authentication_name`, `session_code`) VALUES('{login}', '{nickname}', '{password}', '{authentication_method}', '{authentication_name}', '{session_code}')"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        log(f"User [yellow]{login}[/yellow] added to users table")
        initUserWorkplacesTable(nameDB, getUserFieldByLogin(nameDB, login, "id"))
        return 'Added'
    except:
        log(f"[red]Something wrong[/red]\nFailed to add user [yellow]{login}[/yellow] to [blue]users[/blue] table")
        return 'Error'
    finally:
        connection.close()


# verification
def userValidation(nameDB: str, login: str, authentication_name: str) -> str:
    """
    Added authentication_name into verification table if needed\n
    Returns: 
    - 'Validate' if user`s data is valid
    - 'Login is already taken' if login is taken
    - 'Error' if error
    """

    if login in getUsersColumn(nameDB, "login"):
        log(f"Login [yellow]{login}[/yellow] is [red]already taken[/red]")
        return 'Login is already taken'

    if authentication_name not in getAuthenticationNames(nameDB):
        connection = initConnection(nameDB)
        try:
            # inserting authentication_name into verification table
            sql = f"INSERT INTO verification(`authentication_name`) VALUES('{authentication_name}')"
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            log(f"User [yellow]{login}[/yellow] is [green]valid[/green]")
            return 'Validate'
        except:
            log(f"""[red]Something wrong![/red]\n
            Failed to insert authentication_name [yellow]{authentication_name}[/yellow] into [blue]verification[/blue] table!""")
            return 'Error'
        finally:
            connection.close()


def updateVerificationCode(nameDB: str, authentication_name: str, verification_code: str):
    '''Updates verification code in verification table'''
    connection = initConnection(nameDB)
    try:
        # changes verification code in verification table
        sql = f"UPDATE verification SET verification_code = '{verification_code}' WHERE authentication_name = '{authentication_name}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        log(f"Changed verification code by authentication_name [yellow]{authentication_name}[/yellow] in [blue]verification[/blue] table!")
    except:
        log(f"[red]Something wrong![/red]\nFailed to change verification code by authentication_name [yellow]{authentication_name}[/yellow] in [blue]verification[/blue] table!")
    finally:
        connection.close()


def deleteVerificationCode(nameDB: str, authentication_name: str):
    '''Deletes verification code in verification table'''
    connection = initConnection(nameDB)
    try:
        # deletes verification code from verification table
        sql = f"UPDATE verification SET verification_code = NULL WHERE authentication_name = '{authentication_name}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        log(f"Deleted verification code by authentication_name [yellow]{authentication_name}[/yellow] in [blue]verification[/blue] table!")
    except:
        log(f"[red]Something wrong![/red]\nFailed to delete verification code by authentication_name [yellow]{authentication_name}[/yellow] in [blue]verification[/blue] table!")
    finally:
        connection.close()


# workplaces
def addWorkplace(nameDB: str, workplace_name: str, creator_name: str) -> str:
    """
    Adds workplace to workplaces table
    Returns:
    - 'Added' if added\n
    - 'Workplace name is already taken' if name is taken
    - 'Error' if error
    """
    
    # workplace name checking
    if workplace_name in getWorkplaceColumn(nameDB, 'workplace_name'):
        return "Workplace name is already taken"

    connection = initConnection(nameDB)
    try:
        # inserting workplace into workplaces table
        sql = f"INSERT INTO workplaces(`workplace_name`, `creator_name`) VALUES('{workplace_name}', '{creator_name}')"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        log(f"Workplace [yellow]{workplace_name}[/yellow] added to workplaces table")
        global_id = getWorkplaceFieldByName(nameDB, workplace_name, 'id')
        initWorkplaceChannelsTable(nameDB, global_id)

        addWorkplaceToUserWorkplaces(nameDB, workplace_name, getUserFieldByLogin(nameDB, creator_name, "id"))
        return "Added"
    except:
        log(f"[red]Something wrong![/red]\nFailed to add workplace [yellow]{workplace_name}[/yellow] to workplaces table")
        return 'Error'
    finally:
        connection.close()


# userN_workplaces
def addWorkplaceToUserWorkplaces(nameDB: str, workplace_name: str, user_id: str) -> str:
    """Adds workplace to specified user_workplaces table
    Returns:
    - 'Success!' if added
    - 'Error' if error"""

    global_id = getWorkplaceFieldByName(nameDB, workplace_name, "id")

    connection = initConnection(nameDB)
    try:
        # inserting workplace to userN_workplaces table
        sql = f"INSERT INTO user{user_id}_workplaces(`global_id`, `workplace_name`) VALUES('{global_id}', '{workplace_name}')"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        log(f"Workplace [yellow]{workplace_name}[/yellow] added to user{user_id}_workplaces table")
        return "Success!"
    except:
        log(f"[red]Something wrong![/red]\nFailed to add workplace [yellow]{workplace_name}[/yellow] to user{user_id}_workplaces table")
        return "Error"
    finally:
        connection.close()


# workplaceN_channels
def addChannel(nameDB: str, channel_name: str, workplace_id: str) -> str:
    """
    Adds channel to workplacesN_channels table by workplace_id
    Returns:
    - 'Added' if added
    - 'Channel name is already taken' if name is taken
    """
    
    # channel name checking
    if channel_name in getWorkplaceChannelsColumn(nameDB, workplace_id, 'channel_name'):
        return "Channel name is already taken"

    connection = initConnection(nameDB)
    try:
        # inserting channel to workplaceN_channel table
        sql = f"INSERT INTO workplace{workplace_id}_channels(`name`) VALUES('{channel_name}')"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        log(f"Channel [yellow]{channel_name}[/yellow] added to workplaces{workplace_id}_channels table")
        return "Added"
    except:
        log(f"[red]Something wrong![/red]\nFailed to add workplace [yellow]{channel_name}[/yellow] to workplaces{workplace_id}_channels table")
        return "Error"
    finally:
        connection.close()


def updateChat(nameDB: str, workplace_id: str, channel_id: str, nickname: str, text: str):
    '''Adds message to chat column in workplaceN_channels table '''
    time = datetime.now().strftime("%H:%M")
    messages = getWorkplaceChannelsFieldByChannelId(nameDB, workplace_id, channel_id, 'chat')
    messages += f"<name>{saveHTML(nickname)}</name><time>{time}</time><br><text>{saveHTML(text)}</text><br>"

    connection = initConnection(nameDB)
    try:
        # changing chat by channel_id in workplaceN_channels table 
        sql = f"UPDATE workplace{workplace_id}_channels SET chat = '{messages}' WHERE id = '{channel_id}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        log(f"Chat [yellow]{channel_id}[/yellow] changed in workplaces{workplace_id}_channels table")
    except:
        log(f"[red]Something wrong![/red]\nFailed to change chat [yellow]{channel_id}[/yellow] in workplaces{workplace_id}_channels table")
        return "Error"
    finally:        
        connection.close()
