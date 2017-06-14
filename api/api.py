import web
import json

urls = (
    '/user/register',   'UserRegister',
    '/user/login',      'UserLogin',
    '/user/logout',     'UserLogout',
    '/user/(.+)',       'User',

    '/game/join',       'GameJoin',

)

def write(payload, status):
    payload["status"] = status
    return json.dumps({"payload": payload, "status": status})

def not_found():
    new_request()
    return web.notfound('{"payload": {"error_message": "Endpoint not found. "}, "status": 404}')

def new_request():
    web.header("Content-Type", "application/json")
    web.header("Access-Control-Allow-Origin", "*")

class UserRegister:

    def POST(self):

        new_request()

        i = web.input()

        print i

class UserLogin:

    def POST(self):

        new_request()

class UserLogout:

    def POST(self):

        new_request()

class User:

    def POST(self, uid):

        new_request()

class GameJoin:

    def POST(self, uid):

        new_request()
