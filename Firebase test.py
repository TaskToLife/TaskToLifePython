# To do:
# 1. Change firebase (Maybe?)
# 2. Change to unique ID instead of username for friends and blocked
# 3. Upload to GitHub


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('AccountKey.json')  # AccountKey.json file required
firebase_admin.initialize_app(cred)

db = firestore.client()

admins = db.collection('admins')
items = db.collection('items')
logins = db.collection('logins')
players = db.collection('players')
tasks = db.collection('tasks')
lists = db.collection('lists')

