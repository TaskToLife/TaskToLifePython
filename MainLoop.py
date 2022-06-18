# TODO:
# add addNewTask()
# add profile()
# add editTask()
# add sort functionality to tasksDetailed()

from ObjectClasses import *

"""
This is the main loop of the application
"""


def mainLoop(userID):
    # A low detailed list, probably just the name of the task
    tasksSimple(userID)
    loop = True
    while loop:
        print("1. View Task List",
              "\n2. Add New Task",
              "\n3. View Task History",
              "\n4. View Profile",
              "\n5. Log Out")
        choice = input("What would you like to do: ")
        while choice not in ["1", "2", "3", "4", "5"]:
            choice = input("Please enter a valid number: ")
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
    docs = tasks.where("userID", "==", userID) \
        .where("completed", "==", False).get()
    print("=" * 32, "\nCurrent Tasks:")
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
    # initial task load
    taskList = []
    docs = tasks.where("userID", "==", userID) \
        .where("completed", "==", False).get()
    i = 0
    if len(docs) > 0:
        i = 1
        for doc in docs:
            task = Task(doc.id)
            taskList.append(task)
            displayTask(task, i)
            i += 1

    loop = True
    while loop:
        print("\n1. Edit Task",
              "\n2. Delete Task",
              "\n3. Sort/Filter List of Tasks",
              "\n4. Go Back")
        choice = input("What would you like to do? ")
        while choice not in ["1", "2", "3", "4"]:
            choice = input("Please enter a valid number: ")
        if choice == "1":
            taskNum = input("What task you like to edit: ")
            if taskNum.isdigit():  # check
                taskNum = int(taskNum)
            while taskNum not in range(1, i):
                taskNum = input("Please enter a valid number: ")
                if taskNum.isdigit():  # check2
                    taskNum = int(taskNum)
            editTask(taskList[taskNum - 1])
        elif choice == "2":
            taskNum = input("What task you like to delete: ")
            if taskNum.isdigit():  # check
                taskNum = int(taskNum)
            while taskNum not in range(1, i):
                taskNum = input("Please enter a valid number: ")
                if taskNum.isdigit():  # check2
                    taskNum = int(taskNum)
            tasks.document(taskList[taskNum - 1]).delete()
            taskList.pop(taskNum - 1)
        elif choice == "3":
            sortTasks(taskList, 0)
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

    title = None
    desc = input("Description: ")
    category_name = input("Category Name: ")
    catID = None
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
    editable_list = ["category", "collab", "deadline", "description", "link", "location", "privacy", "repeatable",
                     "starred", "tags", "timer", "title"]
    print("1. Edit task properties")
    print("2. Complete the task")
    userChoice = input("What would you like to do?: ")
    while userChoice not in ["1", "2"]:
        userChoice = input("Please enter a valid number: ")
    if userChoice == "1":
        editDone = False
        while not editDone:
            for i in range(len(editable_list)):
                print(str(i + 1) + ".", editable_list[i])
            userEdit = input("What would you like to edit?: ")
            if userEdit == "1":
                new_desc = input("Enter your new description: ")
                task.changeDescription(new_desc)
                return
    elif userChoice == "2":
        task.changeCompleted()


"""
Displays all completed task
"""


def taskHistory(userID):
    while True:
        completedTaskList = []
        docs = tasks.where("userID", "==", userID) \
            .where("completed", "==", True).get()
        i = 0
        if len(docs) > 0:
            i = 1
            for doc in docs:
                task = Task(doc.id)

                if (datetime.datetime.now() - task.getStartAndEnd()[1]).days < 30:
                    completedTaskList.append(task)
                    displayTaskHistory(task, i)
                i += 1
        else:
            print("No complete task found")

        print("\n1. Edit Task",
              "\n2. Sort/Filter Task",
              "\n3. Clear Task History",
              "\n4. Display Detailed Task History"
              "\n5. Go Back")
        choice = input("What would you like to do? ")
        while choice not in ["1", "2", "3", "4", "5"]:
            choice = input("Please enter a valid number: ")
        if choice == "1":
            if len(docs) > 0:
                taskNum = input("What task you like to edit: ")
                while taskNum not in range(1, i):
                    taskNum = input("Please enter a valid number: ")
                editTask(completedTaskList[i - 1])
            else:
                print("No completed tasks found")
        elif choice == "2":
            sortTasks(completedTaskList, 1)
        elif choice == "3":
            while len(completedTaskList) > 0:
                tasks.document(completedTaskList[0]).delete()
                completedTaskList.pop(0)
        elif choice == "4":
            for i in range(len(completedTaskList)):
                displayTask(completedTaskList[i], i + 1)
        else:
            return


"""
Displays the user profile, giving access to change their data
"""


def profile(userID):
    pass


def displayTask(task, i):
    print("=" * 32,
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


def displayTaskHistory(task, i):
    print("=" * 32,
          "\nTask Number:", i,
          "\nTitle:", task.getTitle(),
          "\nDescription:", task.getDescription(),
          "\nCompletion Date:", task.getStartAndEnd()[1].strftime("%Y-%m-%d"))


"""
Gives users the ability to sort and filter the tasks
n = 0 is taskList
n = 1 is taskHistory
"""


def sortTasks(taskList, n):
    loop = True
    tempList = taskList.copy()
    while loop:
        tempList2 = []
        print("1. Sort",
              "\n2. Filter",
              "\n3. Go Back",
              "\nNote: You can filter the list as many times as you would like before or after sorting.")
        choice = input("What would you like to do? ")

        if choice == "1":  # Sorting
            print("Sort By: ",
                  "\n1. Ascending",
                  "\n2. Descending",
                  "\n3. Go Back")
            choice2 = input("What would you like to sort by? ")
            while choice2 not in ["1", "2", "3"]:
                choice2 = input("Please enter a valid number: ")
            if choice2 == "1":
                tempList.sort(key=lambda x: x.getTitle())
                for i in range(len(tempList)):
                    if n == 0:
                        displayTask(tempList[i], i + 1)
                    else:
                        displayTaskHistory(tempList[i], i + 1)

            elif choice2 == "2":
                tempList.sort(key=lambda x: x.getTitle(), reverse=True)
                for i in range(len(tempList)):
                    if n == 0:
                        displayTask(tempList[i], i + 1)
                    else:
                        displayTaskHistory(tempList[i], i + 1)

        elif choice == "2":  # Filtering
            print("Filter By:",
                  "\n1. Tags",
                  "\n2. Categories",
                  "\n3. Starred",
                  "\n4. Go Back")
            choice2 = input("What would you like to filter by? ")
            while choice2 not in ["1", "2", "3"]:
                choice2 = input("Please enter a valid number: ")

            if choice2 == "1":  # Tags
                tagList = []
                for task in tempList:
                    for tag in task.getTags():
                        if tag not in tagList:
                            tagList.append(tag)
                if len(tagList) > 0:
                    for i in range(len(tagList)):
                        print(str(i + 1) + ". " + tagList[i])
                    choice3 = input("What tag would you like to filter by? ")
                    if choice3.isdigit():
                        choice3 = int(choice3)
                    while choice3 not in range(1, len(tagList)):
                        choice3 = input("Please enter a valid number: ")
                        if choice3.isdigit():
                            choice3 = int(choice3)
                    for j in range(len(tempList)):
                        task = tempList[j]
                        if tagList[choice3 - 1] in task.getTags():
                            tempList2.append(task)
                            if n == 0:
                                displayTask(task, j + 1)
                            else:
                                displayTaskHistory(task, j + 1)
                    tempList = tempList2.copy()
                else:
                    print("There are no tags to filter by.")

            elif choice2 == "2":  # Categories
                categoryList = []
                for task in tempList:
                    if task.getCategory() not in categoryList:
                        categoryList.append(List(task.getCategory()))
                if len(categoryList) > 0:
                    for i in range(len(categoryList)):
                        print(str(i + 1) + ". " + categoryList[i].getName())
                    choice3 = input("What category would you like to filter by? ")
                    if choice3.isdigit():
                        choice3 = int(choice3)
                    while choice3 not in range(1, len(categoryList)):
                        choice3 = input("Please enter a valid number: ")
                        if choice3.isdigit():
                            choice3 = int(choice3)
                    for j in range(len(tempList)):
                        task = tempList[j]
                        if categoryList[choice3 - 1].getID() in task.getCategory():
                            tempList2.append(task)
                            if n == 0:
                                displayTask(task, j + 1)
                            else:
                                displayTaskHistory(task, j + 1)
                    tempList = tempList2.copy()
                else:
                    print("There are no categories to filter by.")

            elif choice2 == "3":  # Starred
                lengthTempList = len(tempList)
                for j in range(lengthTempList):
                    task = tempList[j]
                    if task.getStarred():
                        tempList2.append(task)
                if len(tempList2) > 0:
                    for task in tempList2:
                        if n == 0:
                            displayTask(task, lengthTempList + 1)
                        else:
                            displayTaskHistory(task, lengthTempList + 1)
                    tempList = tempList2.copy()
                else:
                    print("There are no task that are starred.")

        else:
            return


if __name__ == "__main__":
    mainLoop("GCfxc0X812iEKxQEkk3d")
