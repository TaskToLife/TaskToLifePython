import os
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from firebase_admin import firestore
from functions.functions import *
import string
import secrets
import bcrypt

db = firestore.client()
logins = db.collection('logins')

load_dotenv()
EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

def info():
    email_recover = input("Please enter your email address: ")
    data = snapToDict(logins.where("email", "==", email_recover.lower()))
    if data == {}:
        return -1, print("Email does not exist")
    else:
        forgotPass(email_recover)

def forgotPass(email):
    token = string.ascii_letters + string.digits
    # Generates an 8 character long code. Can change to 6 or smth later
    recovery_code = ''.join(secrets.choice(token) for i in range(8))

    msg = EmailMessage()
    msg['Subject'] = 'Password Recovery Code'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content('Here is your recovery code: ' + recovery_code)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    passChange(recovery_code, email)

    
def passChange(secret_token, email):
    correct_code = True
    while correct_code:
        code_input = input("Please enter your recovery code or type 'c' to cancel: ")
        if code_input == "c":
            correct_code = False
        elif secret_token != code_input:
            print("Incorrect code.")
        else:
            new_pass = input("Please enter your new password: ")

            # Checks if email exists
            data = snapToDict(logins.where("email", "==", email.lower()))

            # Gets the password in a sense
            key = list(data.keys())[0]
            data = getData(data)

            # Deletes old password
            logins.document(key).delete()

            # Sets new password
            salt = bcrypt.gensalt()
            encrypted_password = bcrypt.hashpw(new_pass.encode(), salt)
            logins.document(key).set(
                {
                    "email": email,
                    "password": encrypted_password
                }
            )
            print("Password changed successfully!")
            return 1




