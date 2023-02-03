"""
Manager for email bot that will send authentication messages\n 
Main function is send_verification_code_email
"""
# other libs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from os import environ
# my libs
from myCommonFeatures import log

def send_verification_code_email(user_email: str, code: str):
    '''Gives user verification code to their email'''
    message = MIMEMultipart()

    message["From"] = environ.get("BOT_EMAIL")
    message["To"] = user_email
    message["Subject"] = "Autentication in TR Chat"

    messageText = f"""
    Hi!\n
    Your verification code is {code} .\n 
    Enter this code on the website to confirm the activity on your account.\n
    Good luck!😸
    """

    message.attach(MIMEText(messageText))

    #create server 
    server = SMTP('smtp.gmail.com: 587')
    server.starttls()

    # Login Credentials for sending the mail 
    server.login(message['From'], environ.get("BOT_EMAIL_PASSWORD"))
    # send the message via the server. 
    server.sendmail(message['From'], message['To'], message.as_string())
    server.quit()

    log(f"[b]Verification code[/b] sent to email {user_email}")

send_verification_code_email(environ.get("BOT_EMAIL"), "12345")