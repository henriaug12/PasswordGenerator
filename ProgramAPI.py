from flask import Flask, request
from pymongo import MongoClient
import random

app = Flask(__name__)

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

@app.route("/api/<password_name>", methods=['GET','DELETE'])
def manage_passwords_url(password_name):
    if request.method == 'GET':
        queryToFind = {"name": password_name}
        nameAndPassword = col.find_one(queryToFind)
        password_data = {
            "name": nameAndPassword['name'],
            "password": nameAndPassword['password']
        }
        return password_data
    
    elif request.method == 'DELETE':
        queryToDelete = {"name": password_name}
        if(bool(col.delete_one(queryToDelete))):
            return "Deletion was successful"

@app.route("/api", methods=['GET','POST','PUT'])
def manage_passwords():
    if request.method == 'GET':
        jsonList = []
        for nameAndPassword in col.find({}):
                jsonList += [{"name" : nameAndPassword['name'], 
                            "password": nameAndPassword['password']} 
                            ]      
        return jsonList
    
    elif request.method == 'POST':
        data = request.get_json(force=True)
        newPassword = generatePassword(32)
        insertedId = col.insert_one({"name": f"{data['name']}", "password": f"{newPassword}"})
        if insertedId:
            return f"Password created successfully:<br>{data['name']}: {newPassword}",201
    
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        queryToUpdate = {"name": data['name']}
        newPassword = generatePassword(32)
        newValues = { "$set": { "password": f"{newPassword}" } }
        updateSuccess = col.update_one(queryToUpdate,newValues)
        if updateSuccess:
            return f"Password updated successfully:<br> {data['name']}: {newPassword}"

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['PasswordGenerator']
    col = db["passwords"]
    app.run(debug=True)