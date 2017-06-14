import sys

sys.path.insert(0, '..')

import web
import json
import random
import string

from passlib.hash import pbkdf2_sha256

from config import Config

urls = (
    '/user/register',   'UserRegister',
    '/user/login',      'UserLogin',
    '/user/logout',     'UserLogout',
    '/user/(.+)',       'User',

    '/game/join',       'GameJoin',

)

db = web.database(dbn=Config.dbn, db=Config.db, user=Config.user, pw=Config.pw)

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

        if i.username == '' or i.password == '':
            return write({'message': 'Credentials not supplied. '}, 400)

        hashed = pbkdf2_sha256.hash(i.password)

        db.insert('users', username=i.username, password=hashed)

        return write({'message': 'Successfully logged in. '}, 200)


class UserLogin:

    def POST(self):

        new_request()

        i = web.input()

        if i.username == '' or i.password == '':
            return write({'message': 'Credentials not supplied. '}, 400)

        user = db.select('users', dict(username=i.username), where='username=$username').first()

        if user is None:
            return write({'message': 'Username or password incorrect. '}, 403)

        if not pbkdf2_sha256.verify(i.password, user.password):
            return write({'message': 'Username or password incorrect. '}, 403)

        token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(64))
        db.insert('user_sessions', user_id=user.id, token=token)

        return write({'message': 'Successfully logged in. ', 'token': token}, 200)


class UserLogout:

    def POST(self):

        new_request()

        web.setcookie('token', 0, expires=-1)

        return write({'message': 'Logged out successfully. '}, 200)

class User:

    def POST(self, uid):

        new_request()

class GameJoin:

    def POST(self, uid):

        new_request()

if __name__ == '__main__':

    app = web.application(urls, globals())
    app.notfound = not_found
    app.run()
