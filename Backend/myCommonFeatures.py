'''
This module contains log \n
Also this module loads venv values from .env file
'''
from rich.console import Console
import os
from dotenv import load_dotenv

log = Console().log

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    log("vEnv values from .env file loaded")
