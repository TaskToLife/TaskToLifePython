from functions.initializeApp import getDB
from classes.player import Player
from classes.list import List
from classes.task import Task

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


player = Player("5VOVCxFm6IKK9QLs1t91")
task = Task("V7IsJiCh17DKNlqgCaqE")
category = List("W3msGQIN65uik9Ya5fvh")
print(player.getUsername() + " " + task.getTitle() + " " + category.getName())
