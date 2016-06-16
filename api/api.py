import web
# from pymongo import MongoClient
import time
import datetime
import json
from config import conf
import hashlib
import os
from simplemysql import SimpleMysql

#########################################################
#
#               INITIAL SETTINGS
#
#########################################################

urls = (
	"/user/register", "user_register",
	"/user/login", "user_login",
	"/room/create", "room_create"
)

mysql = SimpleMysql(
	host = conf.db_host,
	user = conf.db_user,
	passwd = conf.db_pass,
	db = conf.db_name,
	keep_alive = False
)

# mongo_client = MongoClient("localhost", 27017)
# mongo_db = mongo_client["poker"]
# rooms_doc = mongo_db["rooms"]

#########################################################
#
#               SUPPORT METHODS
#
#########################################################

def write(payload, status):
	payload["status"] = status
	return json.dumps({"payload": payload, "status": status})

def notfound(self):
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

#########################################################
#
#               GAME CLASSES
#
#########################################################

class game_start:
	def POST(self):
		new_request(self)
		data = web.input()
		print "first print"
		time.sleep(10)
		print "second print"

#########################################################
#
#               ROOM CLASSES
#
#########################################################

class room_create:
	def POST(self):
		new_request(self)
		data = web.input()
		if data["hash"]:
			shash = data["hash"]

		user_session = mysql_db.where("hash", mysql_db.escape(shash)).get("user_sessions")

		if user_session == ():
			return write({"error": "Session doesn't exist ."}, 211)
		else:
			user = mysql_db.where("id", user_session[0]["user_id"]).get("users")
			permissions = json.loads(user[0]["permissions"])
			if permissions["Admin"] == 1:
				if data["name"] and data["max_players"] and data["buyin"]:
					name = mysql_db.escape(data["name"])
					max_players = mysql_db.escape(data["max_players"])
					buyin = mysql_db.escape(data["buyin"])
					inserted = mysql_db.insert("rooms", {"name": name, "max_players": max_players, "buyin": buyin})
					room = {
						"name": name,
						"max_players": max_players,
						"buyin": buyin
					}
					room_id = rooms_doc.insert_one()
					if inserted:
						return write({"message": "Room created successfully. "}, 200)
					else:
						return write({"error": "Error inserting into database. "}, 212)
				else:
					return write({"error": "Name not supplied. "}, 210)
			else:
				return write({"error": "You don't have permission to do this. "}, 211)

#########################################################
#
#               USER CLASSES
#
#########################################################

class user_login:
	def POST(self):
		new_request(self)
		data = web.input()
		try:
			username = data["username"].decode("utf-8")
			password = data["password"].decode("utf-8")
			password_hash = hashlib.sha224(password).hexdigest()
		except KeyError:
			return write({"error": "Username or password can't be empty. "}, 400)
		except UnicodeError:
			return write({"error": "Username or password not UTF-8 encoded. "}, 400)

		shash = os.urandom(64).encode("hex")

		user = mysql.getOne("users", ["id", "password"])

		if user is None:
			return write({"error": "Username not found. "}, 400)
		elif user.password == password_hash:
			try:
				mysql.insert("user_sessions", {"user_id": user.id, "hash": shash})
				return write({"message": "Successfully logged in. ", "hash": shash}, 200)
			except:
				return write({"error": "Error inserting into database. "}, 500)
		else:
			return write({"error": "Password was incorrect. "}, 400)


class user_register:
	def POST(self):
		new_request(self)
		data = web.input()
		try:
			username = data["username"].decode("utf-8")
			password = data["password"].decode("utf-8")
			password_hash = hashlib.sha224(password).hexdigest()
		except KeyError:
			return write({"error": "Username or password can't be empty. "}, 400)
		except UnicodeError:
			return write({"error": "Username or password not UTF-8 encoded. "}, 400)

		if len(username) < 3:
			return write({"error": "Username must be at least 3 characters long. "}, 400)
		elif len(username) > 20:
			return write({"error": "Username must be at most 128 characters long. "}, 400)
		elif len(password) > 100:
			return write({"error": "Password must be at most 128 characters long. "}, 400)
		elif username == "" or password == "":
			return write({"error": "Username or password can not be empty. "}, 400)

		user = mysql.getOne("users", ["id"], ["username = '%s'" % username])

		if user is not None:
			return write({"error": "Username already exists. "}, 400)

		try:
			x = mysql.insert("users", {"username": username, "password": password_hash, "balance": 0, "permissions": "{\"Standard\": 1, \"Admin\": 0}"})
			print x
			return write({"message": "Successfully registered %s. " % username}, 200)
		except:
			return write({"error": "Error inserting into database. "}, 500)


#########################################################
#
#               INIT STATEMENTS
#
#########################################################

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()
