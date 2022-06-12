#TODO:
#add taskSimple()
#add tasksDetailed()
#add addNewTask()
#add options to taskHistory()
#add profile()

from functions import *
from classes import *

"""
This is the main loop of the application
"""

def mainLoop(userID):
    #A low detailed list, probably just the name of the task
    tasksSimple(userID)
    loop = True
    while loop:
        print(  "1. View Task List", 
                "\n2. Add New Task", 
                "\n3. View Task History", 
                "\n4. View Profile", 
                "\n5. Log Out" )
        choice = input("What would you like to do: ")
        while choice not in ["1", "2", "3", "4", "5"]:
            choice = input("Please enter a vaild number: ")
        if choice == "1":
            tasksDetailed(userID)
        elif choice == "2":
            addNewTask(userID)
        elif choice == "3":
            taskHistory(userID)
        elif choice == "4":
            profile(userID)
        elif choice == "5":
            loop = False
            print("Logging Out...")

"""
Displays the task list simply by displaying just the name
"""
def tasksSimple(userID):
    return

"""
Displays a detailed list of the tasks, giving access to delete and edit task
"""
def tasksDetailed(userID):
    return

"""
Adds new task the task list
"""
def addNewTask(userID):
    return

"""
Displays all completed task
"""
def taskHistory(userID):
    taskList = []
    docs = tasks.where("userID", "==", userID)\
    .where("completed", "==", True).get()
    if len(docs) > 0:
        i = 1
        for doc in docs:
            task = doc.to_dict()
            taskList.append(task)
            print(  "============================================",
                    "Task Number:", n,
                    "\nTitle:", task["title"], 
                    "\nDescription:", task["description"], 
                    "\nCompletion Date:", task["end"][0:10])
    else: 
        print("No complete task found")

    print(  "\n1. Edit Task",
            "\n2. Go Back")
    choice = input( "What would you like to do? ")
    while choice not in ["1", "2"]:
        choice = input( "Please enter a vaild number: ")
    if choice == "1":
        taskNum = input("What task you like to edit: ")
        while taskNum not in range(1, i):
            taskNum = input("Please enter a vaild number: ")
    else:
        return  

"""
Displays the user profile, giving access to change their data
"""
def profile(userID):
    return
