'''Module that gets info from database\n
Main functions:
- (users) getUsersColumn, getUserFieldByLogin, getUserFieldBySession;
- (verification) getAuthenticationNames, getVerificationCode;
- (workplaces) getWorkplaceColumn, getWorkplaceFieldByName, getWorkplaceFieldById;
- (userN_workplaces) getUserWorkplacesColumn;
- (workspaceN_channles) getWorkplaceChannelsColumn, getWorkplaceChannelsFieldByChannelId;
'''
# other libs
from typing import Literal
# my libs
from database.creator import initConnection
from myCommonFeatures import log


# user
def getUsersColumn(
        nameDB: str, 
        column: Literal['id', 'login', 'nickname', 'password', 'authentication_method', 'authentication_name', 'session_code']
    ) -> list[str]:
    """Returns list of specified column from user table"""

    connection = initConnection(nameDB)
    try:
        # selection of full column from users table
        sql = f"SELECT {column} FROM users"
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [str(row[0]) for row in rows]
    except:
        log(f"[red]Something wrong![/red]\nFailed to select {column}s from [blue]users[/blue] table!")
        return [""]
    finally:
        connection.close()


def getUserFieldByLogin(
        nameDB: str, 
        login: str, 
        column: Literal['id', 'login', 'nickname', 'password', 'authentication_method', 'authentication_name', 'session_code']
    ) -> str:
    """Returns first field in column by user login from user table"""

    connection = initConnection(nameDB)
    try:
        # selection of the first field from users table by login
        sql = f"SELECT {column} FROM users WHERE login = '{login}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        return str(result)
    except:
        log(f"[red]Something wrong![/red]\nFailed to select {column} of user [yellow]{login}[/yellow] from [blue]users[/blue] table!")
        return ""
    finally:
        connection.close()


def getUserFieldBySession(
        nameDB: str, 
        session_code: str, 
        column: Literal['id', 'login', 'nickname', 'password', 'authentication_method', 'authentication_name', 'session_code']
    ) -> str:
    """Returns first field in column by user session"""

    connection = initConnection(nameDB)
    try:
        # selection of the first field from users table by session_code
        sql = f"SELECT {column} FROM users WHERE session_code = '{session_code}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        return str(result)
    except:
        log(f"[red]Something wrong![/red]\nFailed to select {column} of session {session_code} from [blue]users[/blue] table!")
        return ""
    finally:
        connection.close()


# verification
def getAuthenticationNames(
        nameDB: str
    ) -> list[str]:
    """Returns list of authentication names from verification table"""

    connection = initConnection(nameDB)
    try:
        # selection of full column from verification table
        sql = f"SELECT authentication_name FROM verification"
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except:
        log("[red]Something wrong![/red]\nFailed to select authentication_names from [blue]verification[/blue] table!")
        return [""]
    finally:
        connection.close()


def getVerificationCode(
        nameDB: str, 
        authentication_name: str
    ) -> str:
    """Returns verification_code by authentication_name from verification table"""

    connection = initConnection(nameDB)
    try:
        # selection of the first field from verification table by authentication_name
        sql = f"SELECT verification_code FROM verification WHERE authentication_name = '{authentication_name}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        return result
    except:
        log(f"""[red]Something wrong![/red]\n
        Failed to select verification_code by authentication_name [yellow]{authentication_name}[/yellow] 
        from [blue]verification[/blue] table!""")
        return ""
    finally:
        connection.close()


# workplaces
def getWorkplaceColumn(
        nameDB: str, 
        column: Literal['id', 'workplace_name', 'creator_name']
    ) -> list[str]:
    """Returns list of specified column from workplaces table"""

    connection = initConnection(nameDB)
    try:
        # selection full column from workplaces table
        sql = f"SELECT {column} FROM workplaces"
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except:
        log(f"[red]Something wrong![/red]\nFailed to select {column}s from [blue]workplaces[/blue] table!")
        return [""]
    finally:
        connection.close()


def getWorkplaceFieldByName(
        nameDB: str, 
        workplace_name: str,
        column: Literal['id', 'workplace_name', 'creator_name']
    ) -> str:
    """Returns specified field by workplace_name from workplaces table"""

    connection = initConnection(nameDB)
    try:
        # selection of the first field from workplaces table by workplace_name
        sql = f"SELECT {column} FROM workplaces WHERE workplace_name = '{workplace_name}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        return str(result)
    except:
        log(f"""[red]Something wrong![/red]\n
        Failed to select {column} by workplace_name [yellow]{workplace_name}[/yellow] 
        from [blue]workplaces[/blue] table!""")
        return ""
    finally:
        connection.close()


def getWorkplaceFieldById(
        nameDB: str, 
        id: str,
        column: Literal['id', 'workplace_name', 'creator_name']
    ) -> str:
    """Returns specified field by id from workplaces table"""

    connection = initConnection(nameDB)
    try:
        # selection of the first field from workplaces table by id
        sql = f"SELECT {column} FROM workplaces WHERE id = '{id}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        return str(result)
    except:
        log(f"""[red]Something wrong![/red]\n
        Failed to select {column} by id [yellow]{id}[/yellow] 
        from [blue]workplaces[/blue] table!""")
        return ""
    finally:
        connection.close()


# userN_workplaces
def getUserWorkplacesColumn(
        nameDB: str, 
        user_id: str, 
        column: Literal['id', 'global_id', 'workplace_name']
    ) -> list[str]:
    '''Return list of specified column from userN_workplaces table by user_id'''

    connection = initConnection(nameDB)
    try:
        # selection full column from user{user_id}_workplaces table
        sql = f"SELECT {column} FROM user{user_id}_workplaces"
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except:
        log(f"[red]Something wrong![/red]\nFailed to select {column}s from [blue]user{user_id}_workplaces[/blue] table!")
        return [""]
    finally:
        connection.close()


# workspaceN_channles
def getWorkplaceChannelsColumn(
        nameDB: str, 
        workplace_id: str, 
        column: Literal['id', 'channel_name', 'chat']
    ) -> list[str]:
    '''Return list of specified column from workspaceN_channels table by workplace_id'''

    connection = initConnection(nameDB)
    try:
        # selection full column from workplace{workplace_id}_channels
        sql = f"SELECT {column} FROM workplace{workplace_id}_channels"
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except:
        log(f"[red]Something wrong![/red]\nFailed to select {column}s from [blue]workplace{workplace_id}_channels[/blue] table!")
        return[""]
    finally:
        connection.close()


def getWorkplaceChannelsFieldByChannelId(
        nameDB: str, 
        workplace_id: str, 
        channel_id: str,
        column: Literal['id', 'channel_name', 'chat']
    ) -> str:
    '''Returns specified field from workplaceN_channels by channel_id'''

    connection = initConnection(nameDB)
    try:
        # selection of the first field from workplaceN_channels table by id
        sql = f"SELECT {column} FROM workplace{workplace_id}_channels WHERE id = '{channel_id}'"
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()[0][0]
        return str(result)
    except:
        log(f"""[red]Something wrong![/red]\n
        Failed to select {column} by channel_id [yellow]{channel_id}[/yellow] 
        from [blue]workplace{workplace_id}_channels[/blue] table!""")
        return ""
    finally:
        connection.close()
