#TODO: 
#finish login()
#finish signup()

"""
This file contains the start of the application.
Logging in and signing up
"""
from MainLoop import mainLoop

def main():
    loop = True
    while loop:
        print(  "Welcome to TaskToLife.",
                "\n"+"="*64,  
                "\n1. Login",  
                "\n2. Sign Up",
                "\n3. Quit" )
        choice = input("What would you like to do: ")
        while choice not in ["1", "2", "3"]:
            choice = input("Please enter a valid number: ")
        if choice == "1":
            login()
        elif choice == "2":
            signup()
        elif choice == "3":
            loop = False
            print("Quitting...")


def login():
    #on success run mainLoop()
    # mock userID
    userID = "hajdfgjfgbhsaclg"
    mainLoop(userID)

    #on failure
    #not sure what do to here (Allan)
    return 



def signup():
    return 


if __name__ == "__main__":
    main()