from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

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
        insertedId = col.insert_one({"name": f"{data['name']}", "password": f"{data['password']}"})
        if insertedId:
            return f"Password entry {data['name']} created successfully",201
    
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        queryToUpdate = {"name": data['name']}
        newValues = { "$set": { "password": f"{data['password']}" } }
        updateSuccess = col.update_one(queryToUpdate,newValues)
        if updateSuccess:
            return "Password updated successfully"

if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['PasswordGenerator']
    col = db["passwords"]
    app.run(debug=True)