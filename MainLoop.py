#TODO:
#add taskSimple()
#add tasksDetailed()
#add addNewTask()
#add taskHistory()
#add profile()

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
    return

"""
Displays the user profile, giving access to change their data
"""
def profile(userID):
    return
