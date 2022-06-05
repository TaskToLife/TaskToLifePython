import datetime
import json
import firebase_admin
import bcrypt
import pytz
import requests
from firebase_admin import credentials
from firebase_admin import firestore
from dateutil import parser

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
def myConverter(o) -> str:
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
            self.timer = data["timer"]

            # Boolean elements
            self.completed = data["completed"]
            self.private = data["private"]
            self.repeatable = data["repeatable"]
            self.starred = data["starred"]

            # String elements
            self.taskID = userID
            self.title = data["title"]
            self.description = data["description"]
            self.listID = data["listID"]
            self.link = data["link"]
            self.userID = data["userID"]

            # Datetime elements
            self.start = datetime.datetime.fromisoformat(data["start"])
            self.end = datetime.datetime.fromisoformat(data["end"])
            self.deadline = datetime.datetime.fromisoformat(data["deadline"])

            # String array elements
            self.tags = data["tags"]
            self.collab = data["collab"]
            self.days = data["days"]

            # Location dict
            self.location = data["location"]  # {"long": number, "lat": number}

        else:
            print("Data doesn't exist")

    def getPrivacy(self):
        return self.private

    def changePrivacy(self):
        self.private = not self.private
        tasks.document(self.taskID).update({
            "private": self.private
        })

    def getCategory(self):
        return self.listID

    def changeCategory(self, listID):
        self.listID = listID
        tasks.document(self.taskID).update({
            "listID": self.listID
        })

    def getPlayers(self):
        return self.collab

    def addPlayer(self, userID):
        self.collab.append(userID)
        tasks.document(self.taskID).update({
            "collab": self.collab
        })

    def removePlayer(self, userID):
        self.collab.remove(userID)
        tasks.document(self.taskID).update({
            "collab": self.collab
        })

    def getAge(self):
        return self.age

    def changeAge(self, age):
        self.age = age
        tasks.document(self.taskID).update({
            "age": self.age
        })

    def getStarred(self):
        return self.starred

    def changeStarred(self):
        self.starred = not self.starred
        tasks.document(self.taskID).update({
            "starred": self.starred
        })

    def getTags(self):
        return self.tags

    def addTag(self, tag):
        self.tags.append(tag)
        tasks.document(self.taskID).update({
            "tags": self.tags
        })

    def removeTag(self, tag):
        self.tags.remove(tag)
        tasks.document(self.taskID).update({
            "tags": self.tags
        })

    def getTimer(self):
        return self.timer

    def setTimer(self, minutes):
        self.timer = minutes
        tasks.document(self.taskID).update({
            "timer": self.timer
        })

    def getDeadline(self):
        return self.deadline

    def setDeadline(self, deadline):
        self.deadline = deadline
        tasks.document(self.taskID).update({
            "deadline": self.deadline
        })

    def getCompleted(self):
        return self.completed

    def changeCompleted(self):
        self.completed = not self.completed
        tasks.document(self.taskID).update({
            "completed": True
        })

    def getTitle(self):
        return self.title

    def changeTitle(self, title):
        self.title = title
        tasks.document(self.taskID).update({
            "title": self.title
        })

    def getDescription(self):
        return self.description

    def changeDescription(self, description):
        self.description = description
        tasks.document(self.taskID).update({
            "description": self.description
        })

    def getRepeatable(self):
        return self.repeatable

    def changeRepeatable(self):
        self.repeatable = not self.repeatable
        tasks.document(self.taskID).update({
            "repeatable": self.repeatable
        })

    def getFailed(self):
        return self.failed

    def increaseFailed(self):
        self.failed += 1
        tasks.document(self.taskID).update({
            "failed": self.failed
        })

    def resetFailed(self):
        self.failed = 0
        tasks.document(self.taskID).update({
            "failed": self.failed
        })

    def getLoc(self):
        return self.location

    def changeLoc(self, long, lat):
        self.location["long"] = long
        self.location["lat"] = lat
        tasks.document(self.taskID).update({
            "location": self.location
        })

    def getDays(self):
        return self.days

    def setDays(self, days):
        self.days = days
        tasks.document(self.taskID).update({
            "days": self.days
        })


class List:
    def __init__(self, listID):
        data = snapToDict(lists.document(listID))
        if data[listID]:

            data = data[listID]

            # String elements
            self.listID = listID
            self.name = data["name"]
            self.username = data["userID"]
            self.color = data["color"]

            # List elements
            self.tasks = data["tasks"]

        else:
            print("Data doesn't exist")

    def getName(self):
        return self.name

    def changeName(self, name):
        self.name = name
        lists.document(self.listID).update({
            "name": self.name
        })

    def getColor(self):
        return self.color

    def changeColor(self, color):
        self.color = color
        lists.document(self.listID).update({
            "color": self.color
        })

    def getTasks(self):
        return self.tasks

    def addTask(self, taskID):
        self.tasks.append(taskID)
        lists.document(self.listID).update({
            "tasks": self.tasks
        })

    def removeTask(self, taskID):
        self.tasks.remove(taskID)
        lists.document(self.listID).update({
            "tasks": self.tasks
        })

    def getUser(self):
        return self.username

    def changeUser(self, userID):
        self.username = userID
        lists.document(self.listID).update({
            "userID": self.username
        })


print(List("W3msGQIN65uik9Ya5fvh").getColor())
