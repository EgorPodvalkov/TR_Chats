"""Main module that managed threads with backend webserver and telegram bot"""
# other libs
from threading import Thread
import os
# my libs
from webserver import run_webserver
from verification.telegramBot import run_telegram_bot


def manager():
    '''Manages threads for backend'''
    threads = [
        Thread(target = run_telegram_bot),
        Thread(target = run_webserver),
    ]

    for thread in threads:
        thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        os.exit()


if __name__ == '__main__':
    manager()
