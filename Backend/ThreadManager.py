"""Main module that managed threads with backend webserver and telegram bot"""
# other libs
from threading import Thread
# my libs
from webserver import run_webserver
from telegramBot import run_telegram_bot

def manager():
    '''Manages threads for backend'''
    threads = [
        Thread(target = run_webserver),
        Thread(target = run_telegram_bot)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

manager()
