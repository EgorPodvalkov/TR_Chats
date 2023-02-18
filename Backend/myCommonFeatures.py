'''
This module contains log, generateCode \n
Also this module loads venv values from .env file
'''
from rich.console import Console
import os
from dotenv import load_dotenv
from string import ascii_uppercase
from random import randint

log = Console().log

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    log("vEnv values from .env file loaded")


def generateCode(length: int) -> str:
    '''Returnes random code specified length'''
    chars = ascii_uppercase + "1234567890"
    result = ""
    for index in range(length):
        result += chars[randint(0, len(chars) - 1)]
    return result

