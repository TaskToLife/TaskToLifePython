#TODO:
#add addNewTask()
#add profile()
#add editTask()
#add sort functionality to tasksDetailed()

import datetime
from turtle import color
from functions import *
from classes import *
from ObjectClasses import *

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
    docs = tasks.where("userID", "==", userID)\
        .where("completed", "==", False).get()
    print("="*32, "\nCurrent Tasks:")
    if len(docs) > 0:
        for doc in docs:
            task = doc.to_dict()             
            print(task["title"])
    else: 
        print("Nothing To Do")


"""
Displays a detailed list of the tasks, giving access to delete and edit task
"""
def tasksDetailed(userID):
    #initail task load
    taskList = []
    docs = tasks.where("userID", "==", userID)\
        .where("completed", "==", False).get()
    if len(docs) > 0:
        i = 1
        for doc in docs:
            task = Task(doc.id)
            taskList.append(task)               
            displayTask(task, i)
            i += 1
    
    loop = True
    while loop:
        print(  "\n1. Edit Task",
                "\n2. Delete Task", 
                "\n3. Go Back")
        choice = input( "What would you like to do? ")
        while choice not in ["1", "2", "3"]:
            choice = input( "Please enter a vaild number: ")
        if choice == "1":
            taskNum = input("What task you like to edit: ")
            if taskNum.isdigit(): #check
                taskNum = int(taskNum)
            while taskNum not in range(1, i):
                taskNum = input("Please enter a vaild number: ")
                if taskNum.isdigit(): #check2
                    taskNum = int(taskNum)
            editTask(taskList[taskNum - 1])
        elif choice == "2":
            taskNum = input("What task you like to delete: ")
            if taskNum.isdigit(): #check
                taskNum = int(taskNum)
            while taskNum not in range(1, i):
                taskNum = input("Please enter a vaild number: ")
                if taskNum.isdigit(): #check2
                    taskNum = int(taskNum)
            tasks.document(taskList[taskNum - 1]).delete()
            taskList.remove(taskNum - 1)
        else:
            return  

"""
Adds new task the task list
"""
def addNewTask(userID):
    docs = lists.where("userID", "==", userID).get()
    doc_list = []
    for doc in docs:
        doc_list.append(doc)
    title = input("Title: ")
    desc = input("Description: ")
    category_name = input("Category Name: ")
    for i in range(len(doc_list)):
        if doc_list[i].get("name") != category_name:
            cat_color = input("Choose a color for the category: ")
            catID = createList(userID, category_name, cat_color)
            break

    privacy = input("Public? (Y/n): ")
    deadline = input("Deadline: ")
    newTask = createTask(userID, catID.getID(), title, deadline)
    newTask.changeDescription(desc)
    if privacy == "Y".lower():
        newTask.changePrivacy()


"""
If 0, Gives the ability to change any of the task properties. 
If 1, can only change the completion
"""
def editTask(task):
    editable_list = ["category", "collab", "deadline", "description", "link", "location", "privacy", "repeatable", "starred", "tags", "timer", "title"]
    print("1. Edit task properties")
    print("2. Complete the task")
    userChoice = input("What would you like to do?: ")
    while userChoice not in ["1", "2"]:
            userChoice = input( "Please enter a vaild number: ")
    if userChoice == "1":
        print()
        editDone = False
        while not editDone:
            for i in range(len(editable_list)):
                print(str(i+1) + ".", editable_list[i])
            userEdit = input("What would you like to edit?: ")
            if userEdit == "1":
                new_cat = input("What category would you like to change to?: ")
            elif userEdit == "3":
                return
            elif userEdit == "4":
                return
            elif userEdit == "5":
                return
            elif userEdit == "7":
                return
            elif userEdit == "8":
                return
            elif userEdit == "9":
                return
            elif userEdit == "10":
                return
            elif userEdit == "11":
                return
            elif userEdit == "12":
                return
            else:
                print("That option is either currently unavailable or does not exist.")
    elif userChoice == "2":
        task.changeCompleted()

"""
Displays all completed task
"""
def taskHistory(userID):
    completedTaskList = []
    docs = tasks.where("userID", "==", userID)\
        .where("completed", "==", True).get()
    if len(docs) > 0:
        i = 1
        for doc in docs:
            task = Task(doc.id)

            if (datetime.datetime.now() - task.getStartAndEnd()[1]).days < 30:
                completedTaskList.append(task)
                print(  "="*32,
                        "\nTask Number:", i,
                        "\nTitle:", task.getTitle(),
                        "\nDescription:", task.getDescription(),
                        "\nCompletion Date:", task.getStartAndEnd()[1].strftime("%Y-%m-%d"))
            i += 1
    else: 
        print("No complete task found")

    print(  "\n1. Edit Task",
            "\n3. Go Back")
    choice = input( "What would you like to do? ")
    while choice not in ["1", "3"]:
        choice = input( "Please enter a vaild number: ")
    if choice == "1":
        if len(docs) > 0:
            taskNum = input("What task you like to edit: ")
            while taskNum not in range(1, i):
                taskNum = input("Please enter a vaild number: ")
            editTask(completedTaskList[i - 1])
        else:
            print("No completed tasks found")
    else:
        return  


"""
Displays the user profile, giving access to change their data
"""
def profile(userID):
    return




def displayTask(task, i):
    print(  "="*32,
            "\nTask Number:", i,
            "\nTitle:", task.getTitle(),
            "\nDescription:", task.getDescription(),
            "\nTimer:", task.getTimer(),
            "\nDeadline:", task.getDeadline().strftime("%Y-%m-%d"),
            "\nLocation:", task.getLoc(),
            "\nPrivate:", task.getPrivacy(),
            "\nStarred:", task.getStarred(),
            "\nRepeatable:", task.getRepeatable(), 
            "\nTags:", end=" ")
    if len(task.getTags()) > 0:
        for tag in task.getTags():
            print(tag, end=", ")
        print()
    else:
        print("No tags specified")

# Testing of task
# tasksDetailed("GCfxc0X812iEKxQEkk3d")
mainLoop("GCfxc0X812iEKxQEkk3d")