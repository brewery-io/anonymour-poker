import web
from pymongo import MongoClient
import time
import datetime
import json
from config import Config
import pysqlw
import hashlib
import os

db = pysqlw.pysqlw(**{
    "db_type": Config.db_type,
    "db_host": Config.db_host,
    "db_user": Config.db_user,
    "db_pass": Config.db_pass,
    "db_name": Config.db_name
})

urls = (
    "/register", "register",
    "/login", "login"
)
# client = MongoClient("localhost", 27017)
# db = client["poker"]
# requests = db["requests"]
# users = db["users"]

def write(payload, status):
    payload["status"] = status
    return json.dumps({"payload": payload, "status": status})

def notfound():
    # web.header("Content-Type", "application/json; charset=UTF-8")
    new_request(self)
    return web.notfound('{"payload": {"error_message": "Endpoint not found. "}, "status": 404}')

def new_request(request):
    web.header("Content-Type", "application/json")
    web.header("Access-Control-Allow-Origin", "*")
    # request_info = {}
    # request_info["ip"] = web.ctx["ip"]
    # request_info["type"] = "POST"
    # request_info["time"] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    # request_id = requests.insert_one(request_info).inserted_id

class login:
    def POST(self):
        new_request(self)
        data = web.input()
        if data["username"] and data["password"]:
            username = data["username"]
            password = data["password"]
            password_hash = hashlib.sha224(password).hexdigest()
        else:
            return write({"error": "Username or password can't be empty. "}, 210)

        hash = os.urandom(32).encode("hex")

        user = db.where("username", db.escape(username)).get("users")

        if user == ():
            return write({"error": "Username not found. "}, 211)
        elif user[0]["password"] == password_hash:
            db.insert("users_sessions", {"user_id": user[0]["id"], "hash": hash})
            return write({"message": "Successfully logged in. ", "hash": hash}, 200)
        else:
            return write({"error": "Password was incorrect. "}, 211)


class register:
    def POST(self):
        new_request(self)
        data = web.input()
        if data["username"] and data["password"]:
            username = data["username"]
            password = data["password"]
            password_hash = hashlib.sha224(password).hexdigest()
        else:
            return write({"error": "Username or password can't be empty. "}, 210)

        try:
            username.decode("utf-8")
            password.decode("utf-8")
        except UnicodeError:
            return write({"error": "Username or password not UTF-8 encoded. "}, 210)

        if len(username) < 3:
            return write({"error": "Username must be at least 3 characters long. "}, 210)
        elif len(username) > 20:
            return write({"error": "Username must be at most 20 characters long. "}, 210)
        elif len(password) > 100:
            return write({"error": "Password must be at most 100 characters long. "}, 210)
        elif username == "" or password == "":
            return write({"error": "Username or password can not be empty. "}, 210)

        user = db.where("username", db.escape(username)).get("users")

        if user != ():
            return write({"error": "Username already exists. "}, 211)

        inserted = db.insert("users", {"username": db.escape(username), "password": password_hash, "balance": 0})

        if inserted:
            return write({"message": "Successfully registered %s. " % username}, 200)
        else:
            return write({"error": "Unable to register. "}, 500)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
    db.close()
