# To do:
# 1. Change firebase (Maybe?)
# 2. Change to unique ID instead of username for friends and blocked
# 3. Upload to GitHub


import bcrypt as bcrypt
import firebase_admin
import requests
import os
from dotenv import load_dotenv
from firebase_admin import credentials
from firebase_admin import db

load_dotenv()

cred = credentials.Certificate('AccountKey.json')  # AccountKey.json file required
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("DB_URL")  # .env file required
})

ref = db.reference("app/")
admins = ref.child("admins")
logins = ref.child("logins")
players = ref.child("players")
taskXP = ref.child("tasks")

for i in range(1):
    user = requests.get('https://randomuser.me/api/').json()['results'][0]  # Just a random user generator for testing

    email = user['email'].lower()
    username = user['login']['username'].lower()
    password = user['login']['password'].encode('utf-8')

    salt = bcrypt.gensalt(rounds=10)
    encrypted_password = bcrypt.hashpw(password, salt).decode()

    logins.push({
        "email": email,
        "name": user["name"]["first"] + ' ' + user["name"]["last"],
        "password": encrypted_password,
        "username": username
    })

    admins.push(email)

    players.push({
        "pfp": "https://avatars.dicebear.com/api/identicon/" + user["name"]["first"] + ".svg",
        "username": username,
        "email": email,
        "xp": 0,
        "level": 0,
        "mul": 0,
        "cur": 0,
        "bio": "Hi, I'm new here!",
        "pets": [],
        "plants": [],
        "items": [],
        "socials": {},
        "friends": [],  # User ID instead of username
        "blocked": [],  # User ID instead of username
        "lists": [],
        "start": 8,
        "end": 22
    })
