import datetime
from functions.functions import snapToDict
from classes.list import List
from firebase_admin import firestore

db = firestore.client()
tasks = db.collection('tasks')


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
