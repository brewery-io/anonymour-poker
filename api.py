import web
from pymongo import MongoClient
import time
import datetime

urls = (
    "/register", "register"
)
client = MongoClient("localhost", 27017)
db = client["poker"]

def notfound():
    # web.header("Content-Type", "application/json; charset=UTF-8")
    new_request(self)
    return web.notfound('{"payload": {"error_message": "Endpoint not found. "}, "status": 404}')

def new_request(request):
    web.header("Content-Type", "application/json")
    web.header("Access-Control-Allow-Origin", "*")
    request_info = {}
    request_info["ip"] = web.ctx["ip"]
    request_info["type"] = "POST"
    request_info["time"] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    requests = db["requests"]
    request_id = requests.insert_one(request_info).inserted_id

    print request_id

    # requests = db["requests"]
    # requests.insert_one(request_info)

    # print "%s recorded" % request_id

    print request_info

class register:
    def POST(self):
        new_request(self)
        return '{"status": 200}'

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.notfound = notfound
    app.run()
