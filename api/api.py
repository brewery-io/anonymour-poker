import web
# from pymongo import MongoClient
import time
import datetime
import json
from config import conf
import hashlib
import os
import pysqlw

#########################################################
#
#               INITIAL SETTINGS
#
#########################################################

urls = (
	"/user/register", "user_register",
	"/user/login", "user_login",
	"/room/create", "room_create",

	"/game/join", "game_join",
	"/game/leave", "game_leave"
)

db = pysqlw.pysqlw(db_type="sqlite", db_path="db.db")

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

def get_user(sesh):

	user_session = db.where("sesh", sesh).get("user_sessions")

	if len(user_session) == 0:
		return None

	return db.where("id", user_session[0]["user_id"]).get("users")

#########################################################
#
#               GAME CLASSES
#
#########################################################

class game_join:
	def POST(self):
		new_request(self)
		data = web.input()

		try:
			sesh = data["sesh"].decode("utf-8")
			room_id = data["room_id"].decode("utf-8")
		except KeyError:
			return write({"error": "Sesh and room id can't be empty. "}, 400)
		except UnicodeError:
			return write({"error": "Sesh and room id must be UTF-8 encoded. "}, 400)

		game = db.where("room_id", room_id).where("status", "open").get("games")
		room = db.where("id", room_id).get("rooms")
		user = get_user(sesh)

		if user is None:
			return write({"error": "User not logged in. "}, 401)

		if len(game) == 0:
			return write({"error": "Game isn't open or doesn't exist. "}, 403)

		if db.where("game_id", game[0]["id"]).update("games", {"user_ids", "%s,%s" % (game[0]["user_ids"], user[0]["id"])}):
			db.insert("log", {"user_id", user[0]["id"], "action": "join", "value": game[0]["id"]})

			if len(game[0]["user_ids"].split(",")) == room[0]["max_players"]:
				db.where("game_id", game[0]["id"]).update("games", {"status": "started"})
				pass
				#start game proc

			return write({"message": "Joined game. "}, 200)
		else:
			return write({"error": "Error joining game. "}, 500)

class game_leave:
	def POST(self):
		new_request(self)
		data = web.input()

		try:
			sesh = data["sesh"].decode("utf-8")
			room_id = data["room_id"].decode("utf-8")
		except KeyError:
			return write({"error": "Sesh and room id can't be empty. "}, 400)
		except UnicodeError:
			return write({"error": "Sesh and room id must be UTF-8 encoded. "}, 400)

		game = db.where("room_id", room_id).where("status", "open").get("games")

		user = get_user(sesh)

		if user is None:
			return write({"error": "User not logged in. "}, 401)

		if len(game) == 0:
			game = db.where("room_id", room_id).where("status", "started").get("games")
			if len(game) == 0:
				return write({"error": "You're not in this game. "}, 400)

		userlist = game[0]["user_ids"].split(",")
		userlist = userlist.pop(user[0]["id"])
		newlist = ",".join(userlist)

		if db.where("id", game[0]["id"]).update("user_ids", newlist):
			return write({"message": "Successfuly left room. "}, 200)
		else:
			return write({"error": "Couldn't leave room. "}, 500)


#########################################################
#
#               ROOM CLASSES
#
#########################################################

class room_create:
	def POST(self):
		new_request(self)
		data = web.input()

		try:
			sesh = data["sesh"].decode("utf-8")
		except KeyError:
			return write({"error": "Sesh can't be empty. "}, 400)
		except UnicodeError:
			return write({"error": "Sesh not UTF-8 encoded. "}, 400)

		user_session = db.where("sesh", sesh).get("user_sessions")

		if len(user_session) == 0:
			return write({"error": "Session doesn't exist. "}, 401)
		else:
			user = db.where("id", user_session[0]["user_id"]).get("users")
			print user[0]["permissions"]
			permissions = json.loads(user[0]["permissions"])
			if permissions["Admin"] == 1:
				try:
					name = data["name"].decode("utf-8")
					max_players = data["max_players"].decode("utf-8")
					buyin = data["buyin"].decode("utf-8")
				except KeyError:
					return write({"error": "Fields can't be empty. "}, 400)
				except UnicodeError:
					return write({"error": "Fields not UTF-8 encoded. "}, 400)
				try:
					buyin = int(buyin)
					max_players = int(max_players)
				except ValueError:
					return write({"error": "Buyin and max players must be numbers. "}, 400)
				if db.insert("rooms", {"name": name, "buyin": buyin, "max_players": max_players}):
					return write({"message": "Created room. "}, 200)
				else:
					return write({"error": "Error inserting into database. "}, 500)
			else:
				return write({"error": "You don't have permission to do this. "}, 403)

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

		user = db.where("username", username).get("users")

		if len(user) == 0:
			return write({"error": "Username not found. "}, 400)
		elif user[0]["password"] == password_hash:
			if db.insert("user_sessions", {"user_id": user[0]["id"], "sesh": sesh}):
				return write({"message": "Successfully logged in. ", "sesh": sesh}, 200)
			else:
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

		if len(db.where("username", username).get("users")) > 0:
			return write({"error": "Username already exists. "}, 400)

		if db.insert("users", {"username": username, "password": password_hash, "balance": 0, "permissions": "perms"}):
			return write({"message": "Successfully registered %s. " % username}, 200)
		else:
			return write({"error": "Error inserting into database. "}, 500)


#########################################################
#
#               INIT STATEMENTS
#
#########################################################

if __name__ == "__main__":
	db.close()
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()
