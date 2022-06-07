import datetime

from functions.initializeApp import getDB
from classes.player import Player, createPlayer
from classes.list import List, createList
from classes.task import Task, createTask
from classes.login import *

db = getDB()

admins = db.collection('admins')
items = db.collection('items')
logins = db.collection('logins')
players = db.collection('players')
tasks = db.collection('tasks')
lists = db.collection('lists')

# # Get specific data by key
# print(snapToDict(admins.document('245dsIgKk6A8tH0ZNQYk')))
#
# # Get specific data by child
# print(snapToDict(admins.where("email", "==", "apandey3@ualberta.ca")))
#
# # Get all data
# print(snapToDict(admins))
#
# # Get ordered data by child elem
# data = snapToDict(admins.order_by('email', direction=firestore.Query.DESCENDING))
# print(data)
#
# # Add data
# key = getKey(admins)
# admins.document(key).set(
#     {
#         "email": "akshatpandeymyself@gmail.com"
#     }
# )
#
# # Update data
# logins.document("245dsIgKk6A8tH0ZNQYk").update(
#     {
#         "email": "apisop@gmail.com"
#     }
# )
#
# # Delete data
# admins.document("1BEXOBL5gepNlSZt5wFh").delete()

# elem1 = createPlayer()
# print(elem1.getUsername())
# elem2 = createList(elem1.getID(), "TaskToLife", "red")
# print(elem2.getName())
# elem3 = createTask(elem1.getID(),
#                    elem2.getID(),
#                    "Build firebase", datetime.datetime.now() + datetime.timedelta(days=1))
# print(elem3.getTitle())

# signUp()
# print(changePass("ap@gmail.com", "akshat", "pass"))
# print(login("ap@gmail.com", "pass"))
