"""
Manager for telegram bot what will be send authentication messages\n
Main functions are send_verification_code_telegram and run_telegram_bot
"""
# other libs
from telebot import TeleBot
from telegram.constants import ParseMode
from rich.console import Console
from threading import Thread
# my lisbs
from telegramBotAPI import API

bot = TeleBot(API)
log = Console().log


@bot.message_handler(commands=['start'])
def send_id(message):
    '''Gives user chat id for verification in telegram bot'''
    bot.send_message(chat_id = message.chat.id, 
    text = f"Hi\! Paste this code to my website for verification in this bot\. `{message.chat.id}`",
    parse_mode = ParseMode.MARKDOWN_V2)

    log(f"[b]Chat id[/b] sent to user {message.chat.id}")


def send_verification_code_telegram(chat_id: str, code: str):
    '''Gives user verification code in telegram bot'''
    bot.send_message(chat_id = chat_id, 
    text = f"Hi\! Your verification code is `{code}`\.\nGood luck\! 😋",
    parse_mode = ParseMode.MARKDOWN_V2)

    log(f"[b]Verification code[/b] sent to user {chat_id}")


def run_telegram_bot():
    '''Runs telegram bot "TR chat" for sending chat id codes'''
    
    log("[bold yellow]Bot[/bold yellow] is running[white]...")

    bot.polling()

# run_telegram_bot()