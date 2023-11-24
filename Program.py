import pymongo
from pymongo import MongoClient
import random
i = 0
def generatePassword(userMaxSize):
    passArray = ["1","2","3","4","5","6","7","8","9","0",
                 "a","b","c","d","e","f","g","h","i","j",
                 "k","l","m","n","o","p","q","r","s","t",
                 "u","v","w","x","y","z","A","B","C","D",
                 "E","F","G","H","I","J","K","L","M","N",
                 "O","P","Q","R","S","T","U","V","W","X",
                 "Y","Z","`","~","!","@","#","$","%","^",
                 "&","*","(",")","_","-","+","=","{","}",
                 "[","]",":",";","|","<",",",".","?","/"]
    newPassword = ""
    for i in range(userMaxSize):
        newPassword = newPassword + (passArray[random.randint(0, len(passArray)-1)])
    return newPassword

while(i == 0):
    print("\nWhat service do you want to use?\n"+
          "1: Generate a new random password\n"+
          "2: See all passwords\n"+
          "3: Delete a password\n"+
          "4: Update a password\n"+
          "0: Exit\n")
    userInput = input("")
    userInput = int(userInput)
    client = MongoClient('mongodb://localhost:27017/')
    dblist = client.list_database_names()
    db = client['PasswordGenerator']
    col = db["passwords"]

    if(userInput==1):
        userNameInput = input("What will this password be used for?\n")
        userNameQuery = {"name": f"{userNameInput}"}
        if(not col.find_one(userNameQuery)):
            userMaxSize = input("What is the maximum length of the password?\n")
            userMaxSize = int(userMaxSize)
            createdPassword = generatePassword(userMaxSize)
            print(createdPassword)
            userConfirmation = input("Is this password okay?(Y/N)\n")
            userConfirmation = userConfirmation.lower()
            while(userConfirmation != "y"):
                if(userConfirmation=="n"):
                    createdPassword = generatePassword(userMaxSize)
                    print(createdPassword)
                    userConfirmation = input("Is this password okay?(Y/N)\n")
                else: userConfirmation = input("Input not recognized, try again\n")
            insertedId = col.insert_one({"name": f"{userNameInput}", "password": f"{createdPassword}"})
        else: print("Name already taken, try updating instead.\n")
    
    if(userInput==2):
        print("Passwords:\n")
        for nameAndPassword in col.find({}):
            print(f"{nameAndPassword['name']}: {nameAndPassword['password']}")
    
    if(userInput==3):
        print("Passwords:\n")
        for nameAndPassword in col.find({}):
            print(f"{nameAndPassword['name']}: {nameAndPassword['password']}")
        pwToDelete = input("\nWhat's the name of the password you want deleted?\n")
        nameToDelete = {"name": f"{pwToDelete}"}
        if(col.find_one(nameToDelete)):
            confirmationInput = input(f"Are you sure? {pwToDelete} will be deleted.(Y/N)\n")
            confirmationInput.lower()
            if(confirmationInput == "y"):
                if(bool(col.delete_one(nameToDelete))):
                    print("Deletion was successful")
                else: print("Deletion failed")
            elif(confirmationInput == "n"): 
                print("The deletion was cancelled")
            else: print("Invalid input")
        else: print("Name not found")
   # Check for wrong input (not y or n)^
    if(userInput==4):
        pwToUpdate = input("What's the name of the password you want updated?\n")
        nameToUpdate = {"name": f"{pwToUpdate}"}
        documentToUpdate = col.find_one(nameToUpdate)
        if(documentToUpdate):
            updateChoice = input("Would you like to change the name or the password?\n")
            updateChoice = updateChoice.lower()
            if(updateChoice == "name"):
                newName = input("What would you like the new name to be?\n")
                newValues = { "$set": { "name": f"{newName}" } }
                nameConfirmation = input(f"{documentToUpdate['name']} will be renamed to {newName}. Is this okay?(Y/N)")
                nameConfirmation.lower()
                if(nameConfirmation == "y"):
                    if(bool(col.update_one(nameToUpdate,newValues))):
                        print("Update successful")
                    else: print("Update failed")
                elif(nameConfirmation == "n"):
                    print("Update cancelled")
                else: print("Invalid choice")
            elif(updateChoice == "password"):
                userMaxSize = input("What is the maximum length of the password?\n")
                userMaxSize = int(userMaxSize)
                newPassword = generatePassword(userMaxSize)
                print(newPassword)
                userConfirmation = input("Is this password okay?(Y/N)\n")
                userConfirmation = userConfirmation.lower()
                while(userConfirmation != "y"):
                    if(userConfirmation=="n"):
                        newPassword = generatePassword(userMaxSize)
                        print(newPassword)
                        userConfirmation = input("Is this password okay?(Y/N)\n")
                    else: userConfirmation = input("Input not recognized, try again\n")
                updateConfirmation = input(f"{documentToUpdate['name']} will have its password changed from " + 
                      f"{documentToUpdate['password']} to {newPassword}.\nIs this okay(Y/N)?\n")
                newValues = { "$set": { "password": f"{newPassword}" } }
                updateConfirmation = updateConfirmation.lower()
                if(updateConfirmation == "y"):
                    if(bool(col.update_one(nameToUpdate,newValues))):
                        print("Update successful")
                    else: print("Update failed")
                
            else: print("Invalid choice")
        else: print("Name not found. Check the existing passwords for a typo, or create a new one\n")
    if(userInput==0):
        break
client.close()    
