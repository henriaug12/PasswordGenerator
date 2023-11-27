from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/get-one-password/<password_name>")
def get_one_password(password_name):
    queryToFind = {"name": password_name}
    nameAndPassword = col.find_one(queryToFind)
    password_data = {
        "name": password_name,
        "password": nameAndPassword['password']
    }
    return password_data

@app.route("/get-all-passwords")
def get_all_passwords():
    jsonList = []
    for nameAndPassword in col.find({}):
            jsonList += [{"name" : nameAndPassword['name'], 
                        "password": nameAndPassword['password']} 
                        ]      
    return jsonList

@app.route("/create-password/", methods=["POST"])
def create_password():
    data = request.get_json(force=True)
    insertedId = col.insert_one({"name": f"{data['name']}", "password": f"{data['password']}"})
    return f"Password entry {data['name']} created successfully",201


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['PasswordGenerator']
    col = db["passwords"]
    app.run(debug=True)