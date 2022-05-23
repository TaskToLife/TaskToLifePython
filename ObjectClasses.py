import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

ref = db.reference("app/")
admins = ref.child("admins")
logins = ref.child("logins")
players = ref.child("players")
taskXP = ref.child("tasks")

cred = credentials.Certificate('AccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://testing-a3c51-default-rtdb.firebaseio.com"
})


class Pet:
    def __init__(self, name, breed, mood, accessories=None):
        self.name = name
        self.breed = breed
        self.mood = mood
        self.accessories = accessories

    def changeName(self, newName):
        self.name = newName

    def changeMood(self, newMood):
        self.mood = newMood

    def addAccessory(self, accessory):
        if accessory in self.accessories:
            return False
        self.accessories.append(accessory)
        return True

    def removeAccessory(self, accessory):
        if accessory in self.accessories:
            self.accessories.remove(accessory)
            return True
        return False

    def getPetData(self):
        return {"name": self.name, "breed": self.breed, "mood": self.mood, "accessories": self.accessories}


class Plant:
    def __init__(self, species, mood, accessories):
        self.species = species
        self.mood = mood
        self.accessories = accessories

    def changeMood(self, newMood):
        self.mood = newMood

    def addAccessory(self, accessory):
        if accessory in self.accessories:
            return False
        self.accessories.append(accessory)
        return True

    def removeAccessory(self, accessory):
        if accessory in self.accessories:
            self.accessories.remove(accessory)
            return True
        return False

    def getPlantData(self):
        return {"breed": self.species, "mood": self.mood, "accessories": self.accessories}


class List:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks

    def addTask(self, task):
        self.tasks.append(task)

    def removeTask(self, task):
        self.removeTask(task)

    def changeName(self, name):
        self.name = name


class Task:
    def __init__(self, title, notification, xp, checklist=None, priority=5, deadline=None, private=True, comments=None):
        self.title = title
        self.notification = notification
        self.xp = xp
        self.checklist = checklist
        self.priority = priority
        self.deadline = deadline
        self.private = private
        self.comments = comments

    def changeTitle(self, title):
        self.title = title

    def changeNotification(self, notification):
        self.notification = notification

    def changePriority(self, priority):
        self.priority = priority

    def changeDeadline(self, deadline):
        self.deadline = deadline

    def changePrivacy(self):
        self.private = not self.private

    def addComment(self, comment):
        self.comments.append(comment)

    def removeComment(self, comment):
        self.comments.remove(comment)





