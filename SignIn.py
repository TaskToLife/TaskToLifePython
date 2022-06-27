"""
This file contains the start of the application.
Logging in and signing up
"""
from MainLoop import mainLoop
from classes.login import *
from ForgotPass import info

db = firestore.client()
logins = db.collection('logins')

def main():
    loop = True
    while loop:
        print(  "Welcome to TaskToLife.",
                "\n"+"="*64,  
                "\n1. Login",  
                "\n2. Sign Up",
                "\n3. Forgot Password"
                "\n4. Quit" )
        choice = input("What would you like to do: ")
        while choice not in ["1", "2", "3", "4"]:
            choice = input("Please enter a valid number: ")
        if choice == "1":
            email = input("Please enter your email address: ")
            password = input("Please enter your password: ")
            data = login(email, password)
            if data[0] == 1:
                mainLoop(data[1])
            else:
                if data == -1:
                    print("Email Error")
                else:
                    print("Password Error")
        elif choice == "2":
            signUp()
        elif choice == "3":
            # info()
            pass
        elif choice == "4":
            loop = False
            print("Quitting...")


if __name__ == "__main__":
    main()