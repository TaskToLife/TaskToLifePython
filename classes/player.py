import datetime
import requests
from functions.functions import *
from firebase_admin import firestore

db = firestore.client()
players = db.collection('players')


class Player:
    def __init__(self, userID):
        data = snapToDict(players.document(userID))
        if data[userID]:
            data = data[userID]

            # List elements
            self.blocked = data["blocked"]
            self.categories = data["categories"]
            self.friend_req = data["friend_req"]
            self.friends = data["friends"]
            self.notifications = data["notifications"]
            self.plant = data["plant"]  # { growth: [list of int per week], startDate: date, type: string }
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

    def getLevel(self):
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
        self.blocked.append(userID)
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
        self.categories.append(category)
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
        self.friend_req.append(req)
        players.document(self.userID).update({
            "friend_req": self.friend_req
        })

    def removeFriendReqs(self, req):
        self.friend_req.remove(req)
        players.document(self.userID).update({
            "friend_req": self.friend_req
        })

    def getFriends(self):
        return self.friends

    def addFriend(self, userID):
        self.friends.append(userID)
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
        self.notifications.append(notification)
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

    def getID(self):
        return self.userID


def createPlayer() -> Player:
    key = getKey(players)
    players.document(key).set(
        {
            "blocked": [],
            "categories": [],
            "currency": 0,
            "friend_req": [],
            "friends": [],
            "level": 1,
            "multiplier": 0,
            "notifications": [],
            "pfp": "https://avatars.dicebear.com/api/identicon/" + key + ".svg",
            "plant": {
                "growth": [],
                "startDate": str(datetime.datetime.now()),
                "type": "Pine"
            },
            "socials": {},
            "username": requests.get("https://randomuser.me/api/").json()["results"][0]["login"]["username"],
            "xp": 0
        }
    )
    return Player(key)
