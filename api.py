import web
from pymongo import MongoClient
import time
import datetime
import json

urls = (
    "/register", "register"
)
client = MongoClient("localhost", 27017)
db = client["poker"]
requests = db["requests"]
users = db["users"]

def write(payload, status):
    payload["status"] = status
    return json.dumps(payload)

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
    #
    # request_id = requests.insert_one(request_info).inserted_id

class register:
    def POST(self):
        new_request(self)
        data = web.input()
        username = data["username"]
        password = data["password"]

        try:
            username.decode("utf-8")
            password.decode("utf-8")
        except UnicodeError:
            return write({"payload": {"error": "Username or password not UTF-8 encoded. "}}, 210)

        if len(username) < 3:
            return write({"payload": {"error": "Username must be at least 3 characters long. "}}, 210)
        elif len(username) > 20:
            return write({"payload": {"error": "Username must be at most 20 characters long. "}}, 210)
        elif len(password) > 100:
            return write({"payload": {"error": "Password must be at most 100 characters long. "}}, 210)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
