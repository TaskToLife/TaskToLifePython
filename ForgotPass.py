import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from firebase_admin import firestore
from functions.functions import *

db = firestore.client()
logins = db.collection('logins')

load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

# def info():
#     email_recover = input("Please enter your email address: ")
#     data = snapToDict(logins.where("email", "==", email_recover.lower()))
#     if data == {}:
#         return -1, "Email does not exist"
#     else:
#         forgotpass(email_recover)

def forgotpass(email):
    msg = EmailMessage()
    msg['Subject'] = 'Password Reminder'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content('Here is your password: ')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)
