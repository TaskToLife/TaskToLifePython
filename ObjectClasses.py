import datetime
import json
import firebase_admin
import bcrypt
import requests
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


# Convert snapshot return type to dictionary
def snapToDict(elem) -> dict:
    elem = elem.get()
    try:
        iter(elem)
        return {doc.id: doc.to_dict() for doc in elem}
    except TypeError:
        return {elem.id: elem.to_dict()}


# Generate random key that works with our database
def getKey(ref) -> str:
    return list(snapToDict(ref.document()).keys())[0]


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

# Convert datatime object to string
def myConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


class Task:
    def __init__(self, userID):
        data = snapToDict(tasks.document(userID))
        if data[userID]:
            data = data[userID]

            # Integer elements
            self.age = data["age"]
            self.xp = data["xp"]
            self.failed = data["failed"]

            # Boolean elements
            self.completed = data["completed"]
            self.private = data["private"]
            self.repeatable = data["repeatable"]
            self.starred = data["starred"]

            # String elements
            self.title = data["title"]
            self.description = data["description"]
            self.listID = data["listID"]
            self.link = data["link"]
            self.userID = data["userID"]
            self.taskID = userID

            # Datetime elements
            self.start = datetime.datetime.fromisoformat(str(data["start"]))
            self.end = datetime.datetime.fromisoformat(str(data["end"]))
            self.timer = datetime.datetime.fromisoformat(str(data["timer"]))
            self.deadline = datetime.datetime.fromisoformat(str(data["timer"]))

            # String array elements
            self.tags = data["tags"]
            self.users = data["collab"]

        else:
            print("Data doesn't exist")

    def getPrivacy(self):
        return self.private

    def changePrivacy(self):
        self.private = not self.private
        tasks.document(self.taskID).update({
            "private": self.private
        })

    def getPlayers(self):
        return self.users

    def addPlayer(self, userID):
        self.users.append(userID)

    def removePlayer(self, userID):
        self.users.remove(userID)

    def getAge(self):
        return self.age

    def updateAge(self, age):
        self.age = age

    def getStarred(self):
        return self.starred

    def changeStarred(self):
        self.starred = not self.starred

    def getTags(self):
        return self.tags

    def addTag(self, tag):
        self.tags.append(tag)

    def removeTag(self, tag):
        self.tags.remove(tag)


Task("V7IsJiCh17DKNlqgCaqE").changePrivacy()
print(Task("V7IsJiCh17DKNlqgCaqE").getPrivacy())
