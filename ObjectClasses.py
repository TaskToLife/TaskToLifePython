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
        List(self.listID).removeTask(self.taskID)
        self.listID = listID
        tasks.document(self.taskID).update({
            "listID": self.listID
        })
        List(self.listID).addTask(self.taskID)

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


class Player:
    def __init__(self, userID):
        data = snapToDict(players.document(userID))
        if data[userID]:
            data = data["userID"]

            # List elements
            self.blocked = data["blocked"]
            self.categories = data["categories"]
            self.friend_req = data["friend_req"]
            self.friends = data["friends"]
            self.notifications = data["notifications"]
            self.plant = data["growth"]  # { growth: [list of int per week], startDate: date, type: string }
            self.socials = data["socials"]  # {Social (like FaceBook for example): string (username)}

            # Integer elements
            self.currency = data["currency"]
            self.level = data["level"]
            self.multiplier = data["multiplier"]
            self.xp = data["xp"]

            # String elements
            self.userID = userID
            self.pfp = data["pfp"]
            self.username = data["username"]

        else:
            print("Data doesn't exist")

    def getUsername(self):
        return self.username

    def changeUsername(self, username):
        self.username = username
        players.document(self.userID).update({
            "username": self.username
        })

    def getPFP(self):
        return self.pfp

    def changePFP(self, pfp):
        self.pfp = pfp
        players.document(self.userID).update({
            "pfp": self.pfp
        })

    def getXP(self):
        return self.xp

    def changeXP(self, XP):
        self.xp = XP
        players.document(self.userID).update({
            "xp": self.xp
        })

        # Add level change formula here

    def getMultiplier(self):
        return self.multiplier

    def changeMultiplier(self, mul):
        self.multiplier = mul

    def getLevel(self, mul):
        return self.level

    def changeLevel(self, level):
        self.level = level
        players.document(self.userID).update({
            "level": self.level
        })

    def getCurrency(self):
        return self.currency

    def changeCurrency(self, currency):
        self.currency = currency
        players.document(self.userID).update({
            "currency": self.currency
        })

    def getBlocked(self):
        return self.blocked

    def addBlocked(self, userID):
        self.blocked.add(userID)
        players.document(self.userID).update({
            "blocked": self.blocked
        })

    def removeBlocked(self, userID):
        self.blocked.remove(userID)
        players.document(self.userID).update({
            "blocked": self.blocked
        })

    def getCategories(self):
        return self.categories

    def addCategory(self, category):
        self.categories.add(category)
        players.document(self.userID).update({
            "categories": self.categories
        })

    def removeCategory(self, category):
        self.categories.remove(category)
        players.document(self.userID).update({
            "categories": self.categories
        })

    def getFriendReqs(self):
        return self.friend_req

    def addFriendReqs(self, req):
        self.friend_req.add(req)
        players.document(self.userID).update({
            "friend_req": self.friend_req
        })

    def removeFriendReqs(self, req):
        self.friend_req.add(req)
        players.document(self.userID).update({
            "friend_req": self.friend_req
        })

    def getFriends(self):
        return self.friends

    def addFriend(self, userID):
        self.friends.add(userID)
        players.document(self.userID).update({
            "friends": self.friends
        })

    def removeFriend(self, userID):
        self.friends.remove(userID)
        players.document(self.userID).update({
            "friends": self.friends
        })

    def getNotifications(self):
        return self.notifications

    def addNotification(self, notification):
        self.notifications.add(notification)
        players.document(self.userID).update({
            "notifications": self.notifications
        })

    def removeNotification(self, notification):
        self.notifications.remove(notification)
        players.document(self.userID).update({
            "notifications": self.notifications
        })

    def getPlant(self):
        return self.plant

    def addPlantStat(self, stat):
        self.plant["growth"].append(stat)
        players.document(self.userID).update({
            "plant": self.plant
        })

    def setPlantDate(self, date):
        self.plant["startDate"] = date
        players.document(self.userID).update({
            "plant": self.plant
        })

    def setPlantType(self, plantType):
        self.plant["type"] = plantType
        players.document(self.userID).update({
            "plant": self.plant
        })

    def getSocials(self):
        return self.socials

    def changeSocial(self, social, username):
        self.socials[social] = username
        players.document(self.userID).update({
            "socials": self.socials
        })

    def removeSocial(self, social):
        del self.socials[social]
        players.document(self.userID).update({
            "socials": self.socials
        })




