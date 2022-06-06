from classes.player import Player
from functions.functions import *
from firebase_admin import firestore

db = firestore.client()
lists = db.collection('lists')


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

    def getID(self):
        return self.listID

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


def createList(userID, name, color) -> List:
    key = getKey(lists)
    lists.document(key).set(
        {
            "userID": userID,
            "color": color,
            "name": name,
            "tasks": []
        }
    )
    Player(userID).addCategory(key)
    return List(key)
