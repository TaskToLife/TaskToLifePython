import bcrypt
from firebase_admin import firestore
from classes.player import Player, createPlayer
from functions.functions import *

db = firestore.client()
logins = db.collection('logins')


# SignUp function
# - Returns -1 if email already exists
# - Returns Player if after signup
def signUp() -> Player or int:
    email = input("Enter email id: ").lower()
    if snapToDict(logins.where("email", "==", email)):
        print("Email exists")
        return -1
    password = input("Enter password: ")
    salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(password.encode(), salt)

    player = createPlayer()
    logins.document(player.getID()).set(
        {
            "email": email,
            "password": encrypted_password
        }
    )
    return player


# Login function
# - Returns -1 if user doesn't exist
# - Returns 0 if user's password is incorrect
# - Returns 1 if user's password is correct
def login(email, password) -> int:
    data = snapToDict(logins.where("email", "==", email.lower()))
    if data == {}:
        return -1, None

    key = list(data.keys())[0]
    data = getData(data)
    success = bcrypt.checkpw(password.encode(), data["password"])
    if success:
        return 1, key
    return 0, None


# Change password function
# - Returns -1 if the email was found
# - Returns 0 if the password was incorrect
# - Returns 1 if the password was correct and was changed
def changePass(email, password, new_pass) -> int:
    data = snapToDict(logins.where("email", "==", email.lower()))
    if data == {}:
        return -1

    key = list(data.keys())[0]
    data = getData(data)

    success = bcrypt.checkpw(password.encode(), data["password"])
    if success:
        logins.document(key).delete()
        salt = bcrypt.gensalt()
        encrypted_password = bcrypt.hashpw(new_pass.encode(), salt)
        logins.document(key).set(
            {
                "email": email,
                "password": encrypted_password
            }
        )
        return 1
    return 0


# Change email function
# - Returns -1 if the email was found
# - Returns 0 if the password was incorrect
# - Returns 1 if the password was correct and email was changed
def changeEmail(email, password, new_email) -> int:
    data = snapToDict(logins.where("email", "==", email.lower()))
    if data == {}:
        return -1

    key = list(data.keys())[0]
    data = getData(data)

    success = bcrypt.checkpw(password.encode(), data["password"])
    if success:
        logins.document(key).update(
            {
                "email": new_email,
            }
        )
        return 1
    return 0
