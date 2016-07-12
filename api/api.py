import web
import time
import datetime
import json
from config import conf
import hashlib
import os
import pg_simple as pg
from random import randint
from multiprocessing import Process

#########################################################
#
#               INITIAL SETTINGS
#
#########################################################

urls = (
    "/user/register", "user_register",
    "/user/login", "user_login",
    "/user/logout", "user_logout",

    "/room/create", "room_create",
    "/room/list", "room_list",
    "/room/join", "room_join",
    "/room/leave", "room_leave",
    "/room/status", "room_status",

    "/game/state", "game_state",
    "/game/leave", "game_leave"
)

pg.config_pool(host=conf.db_host, database=conf.db_name, user=conf.db_user, password=conf.db_pass, max_conn=250, expiration=60)

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

def get_user(sesh=None, username=None):

    with pg.PgSimple() as db:

        if sesh is not None:

            user_session = db.fetchone("user_sessions", fields=["user_id"], where=("sesh = %s", [sesh]))

            if user_session is None:
                return None

            user = db.fetchone("users", where=("id = %s", [user_session[0]]))

        else:
            user = db.fetchone("users", where=("username = %s", [username]))

        return user

def deal(used, amount):

    f = open("inc/deck.json")
    deck = json.loads(f.read())
    f.close()

    used_cards = json.loads(used)

    for used_card in used_cards:
        deck.pop(used_card)

    result = []

    for i in xrange(amount):
        result.append(deck.pop(randint(0, len(deck))))

    return result

def autofold(user_id, game_id):

    time.sleep(2)

    with pg.PgSimple() as db:

        game = db.fetchone("games", where=("id = %s", [game_id]))

def win(user_id, game_id):

    with pg.PgSimple() as db:

        # db.update("rooms", where=("game_id = %s", [game_id]), fields={"status"})

        game = db.update("games", where=("id = %s", [game_id]), data={"status": "ended"}, returning="room_id")
        db.update("rooms", where=("id = %s", [game.room_id]), data={"status": "open"})

def endofround(bets, actions, turn):

    if turn % len(bets) == 0:

        ingame = {}

        for userid in bets:
            if actions[userid] is not "leave" and actions[userid] is not "fold":
                ingame[userid] = bets[userid]

        if set(ingame) == 1:  # all bets are the same, end of round
            return true

    return false


#########################################################
#
#               GAME CLASSES
#
#########################################################


class game_state:
    def POST(self):
        new_request(self)
        data = web.input()

        try:
            sesh = data["sesh"].decode("utf-8")
            state_id = int(data["state_id"].decode("utf-8"))
            game_id = int(data["game_id"].decode("utf-8"))
        except KeyError:
            return write({"error": "Data can't be empty. "}, 400)
        except UnicodeError:
            return write({"error": "Data must be UTF-8 encoded. "}, 400)
        except ValueError:
            return write({"error": "State and game IDs must be integers. "}, 400)

        with pg.PgSimple() as db:
            game_state = db.fetchone("game_states", where=("game_id = %s", [game_id]))

            if game_state.id > state_id:

                user = get_user(sesh=sesh)

                if user is None:
                    return write({"error": "User doesn't exist. "}, 400)

                game = db.fetchone("games", where=("id = %s AND status = %s", [game_id, "running"]))

                if game is None:
                    return write({"error": "The game doesn't exist. "}, 404)

                state = db.fetchone("game_states", where=("game_id = %s", [game_id]))
                user_ids = game.user_ids.split(",")

                if str(user.id) not in user_ids:
                    return write({"error": "You are not in this game. "}, 403)

                if len(user_ids) == 1:
                    Process(target=autofold, args=(user_ids[0], game_id)).start()
                    return write({"message:": "You have won this game. "}, 200)

                holes = json.loads(game_state.holes)

                hand = holes[str(user.id)]

                return write({"message": "Game state. ",\
                            "id": game_state.id,\
                            "changed": True,\
                            "hand": hand,\
                            "community": json.loads(game_state.community),\
                            "bets": json.loads(game_state.bets),\
                            "money": json.loads(game_state.money),\
                            "pot": game_state.pot,\
                            "big": game_state.big,\
                            "small": game_state.small,\
                            "bets": json.loads(game_state.bets),\
                            "actions": json.loads(game_state.actions),\
                            "next_id": game_state.next_id,\
                            "expiry": str(game_state.expiry),\
                            "user_ids": user_ids}, 200)

            return write({"message": "State hasn't changed. ", "changed": False}, 200)

class game_leave:

    def POST(self):

        new_request(self)

        data = web.input()

        try:
            sesh = data["sesh"].decode("utf-8")
            action = data["action"].decode("utf-8")
            game_id = data["game_id"].decode("utf-8")
        except KeyError:
            return write({"error": "Data can't be empty. "}, 400)
        except UnicodeError:
            return write({"error": "Data not UTF-8 encoded. "}, 400)

        user = get_user(sesh=sesh)

        with pg.PgSimple() as db:

            game = db.fetchone("games", where=("id = %s", [game_id]))
            state = db.fetchone("game_states", where=("game_id = %s", [game_id]))

            user_ids = state.user_ids.split(",")

            if game.status != "running":
                return write({"error": "The game has not been found. "}, 404)

            if str(user.id) not in user_ids:
                return write({"error": "You are not in this game. "}, 403)

            if state.next_id != user.id:
                return write({"error": "It's not your turn. "}, 403)

            print json.loads(state.money)
            holes = json.loads(state.holes)
            bets = json.loads(state.holes)
            money = json.loads(state.holes)
            actions = json.loads(state.actions)
            user_ids.remove(str(user.id))

            print user_ids

            holes.pop(str(user.id))
            bets.pop(str(user.id))
            money.pop(str(user.id))
            actions[str(user.id)] = "leave"

            if state.turn == len(user_ids):

                # this is the end of the round
                pass

            else:

                print "insert new state and leave"
                print holes
                print bets
                print money
                print actions
                print user_ids


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

        user = get_user(sesh=sesh)

        if user is None:
            return write({"error": "Session doesn't exist. "}, 404)

        permissions = json.loads(user.permissions)
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
            try:
                with pg.PgSimple() as db:
                    if db.insert("rooms", data={"name": name, "buyin": buyin, "max_players": max_players, "status": "open"}) == 1:
                        db.commit()
                        return write({"message": "Room %s created successfully. " % name}, 200)
                    else:
                        return write({"error": "Error inserting into database. "}, 500)
            except:
                return write({"error": "Error inserting into database. "}, 500)

        return write({"error": "You don't have permission to do this. "}, 403)

class room_list:
    def POST(self):
        new_request(self)
        data = web.input()

        with pg.PgSimple() as db:
            rooms = db.fetchall("rooms")

            result = []

            for room in rooms:

                result.append([room.id, room.name, room.max_players, room.buyin, room.status])

            return write({"message": "List of rooms. ", "rooms": result}, 200)

class room_join:
    def POST(self):
        new_request(self)
        data = web.input()

        try:
            sesh = data["sesh"].decode("utf-8")
            room_id = int(data["room_id"].decode("utf-8"))
        except KeyError:
            return write({"error": "Sesh and room id can't be empty. "}, 400)
        except UnicodeError:
            return write({"error": "Sesh and room id must be UTF-8 encoded. "}, 400)
        except ValueError:
            return write({"error": "Room id must be an integer. "}, 400)

        user = get_user(sesh=sesh)

        if user is None:
            return write({"error": "Session doesn't exist. "}, 404)

        if user.room_id is not None:
            return write({"error": "Leave the room you're in before joining another one. "}, 400)

        with pg.PgSimple() as db:

            room = db.fetchone("rooms", where=("id = %s", [room_id]))

            if room.status == "open":
                users_in_room = db.fetchall("users", where=("room_id = %s", [room_id]))

                user_ids = []
                for u in users_in_room:
                    user_ids.append(u.id)
                    user_ids.append(user.id)
                if len(users_in_room) == room.max_players - 1:
                    #try:
                    room = db.update("rooms", where=("id = %s", [room_id]), data={"status": "ingame"}, returning="max_players")
                    db.update("users", where=("id = %s", [user.id]), data={"room_id": room_id})

                    game_id = db.insert("games", {"room_id": room_id, "user_ids": ",".join(str(v) for v in user_ids), "status": "running"}, returning="id")

                    to_deal = deal("[]", 3 + 2 * room[0].max_players)

                    community = []

                    community.extend([to_deal.pop(), to_deal.pop(), to_deal.pop()])

                    holes = {}
                    money = {}
                    bets = {}
                    actions = {}

                    for user_id in user_ids:
                        holes[user_id] = [to_deal.pop(), to_deal.pop()]
                        money[user_id] = 1000
                        bets[user_id] = 0
                        actions[user_id] = ""

                    money[user_ids[-2]] = 950
                    money[user_ids[-1]] = 975
                    bets[user_ids[-2]] = 50
                    bets[user_ids[-1]] = 25

                    game_state = db.insert("game_states", {"game_id": game_id,\
                                                         "user_ids": ",".join(str(v) for v in user_ids),\
                                                        "state": "flop",\
                                                        "community": json.dumps(community),\
                                                        "holes": json.dumps(holes),\
                                                        "big": 50,\
                                                        "small": 25,\
                                                        "bets": json.dumps(bets),\
                                                        "actions": json.dumps(actions),\
                                                        "pot": 75,\
                                                        "round": 1,\
                                                        "turn": 1,\
                                                        "money": json.dumps(money),\
                                                        "next_id": user_ids[0],\
                                                        "played": datetime.datetime.now(),\
                                                        "expiry": datetime.datetime.now() + datetime.timedelta(seconds=30)}, returning="id")

                    db.commit()

                    Process(target=autofold, args=(user_ids[0], game_id)).start()

                    return write({"message": "Joined room and started game. ", "game_id": game_id, "room_id": room_id, "started": True}, 200)
                    #except Exception:
                    #	return write({"error": "Error joining room. "}, 500)

                try:
                    db.update("users", where=("id = %s", [user.id]), data={"room_id": room_id})
                    db.commit()
                    return write({"message": "Joined room %s. " % room.name, "started": False, "room_id": room_id}, 200)

                except:
                    return write({"error": "Error joining room. "}, 500)

            return write({"error": "Room is not open. "}, 403)

class room_leave:
    def POST(self):
        new_request(self)
        data = web.input()

        try:
            sesh = data["sesh"].decode("utf-8")
        except KeyError:
            return write({"error": "Sesh can't be empty. "}, 400)
        except UnicodeError:
            return write({"error": "Sesh must be UTF-8 encoded. "}, 400)

        user = get_user(sesh=sesh)

        with pg.PgSimple() as db:
            room = db.fetchone("rooms", where=("id = %s", [user.room_id]))

            if room is None:
                return write({"error": "You are not in a room. "}, 400)

            if room.status == "open":
                try:
                    db.update("users", where=("id = %s", [user.id]), data={"room_id": None})
                    db.commit()
                    return write({"message": "Successfully left room. "}, 200)
                except:
                    return write({"error": "Error leaving room. "}, 500)
            else:
                return write({"error": "Room is not open to leave. "}, 400)

class room_status:
    def POST(self):
        new_request(self)
        data = web.input()

        try:
            room_id = data["room_id"].decode("utf-8")
            if room_id == "":
                return write({"error": "Room id can't be empty. "}, 400)
        except KeyError:
            return write({"error": "Room id can't be empty. "}, 400)
        except UnicodeError:
            return write({"error": "Room id must be UTF-8 encoded. "}, 400)

        with pg.PgSimple() as db:

            room = db.fetchone("rooms", where=("id = %s", [room_id]))

            if room is None:
                return write({"error": "Room doesn't exist. "}, 404)

            if room.status == "ingame":
                game = db.fetchone("games", where=("room_id = %s AND status = %s", [room_id, "running"]))
                if game is None:

                    return write({"error": "Room is in game, but error getting game. "}, 500)

                return write({"message": "Game has started. ", "ingame": True, "game_id": game.id}, 200)


            return write({"message": "Game has not started. ", "ingame": False}, 200)

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

        sesh = os.urandom(64).encode("hex")

        #user = db.where("username", username).get("users")
        user = get_user(username=username)

        if len(user) == 0:
            return write({"error": "Username not found. "}, 400)
        elif user.password == password_hash:
            #if db.insert("user_sessions", {"user_id": user[0]["id"], "sesh": sesh}):
            try:
                with pg.PgSimple() as db:
                    if db.insert("user_sessions", data={"sesh": sesh, "user_id": user.id}) == 1:
                        db.commit()
                        return write({"message": "Successfully logged in. ", "sesh": sesh, "user_id": user.id}, 200)
                    return write({"error": "Error inserting into database. "}, 500)
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

        if get_user(username=username) is not None:
            return write({"error": "Username already exists. "}, 400)
        try:
            with pg.PgSimple() as db:
                if db.insert("users", data={"username": username, "password": password_hash, "credits": 0, "permissions": "{\"Admin\": 0, \"Standard\": 1}"}) == 1:
                    db.commit()
                    return write({"message": "Successfully registered %s. " % username}, 200)
                return write({"error": "Error inserting into database. "}, 500)
        except:
            return write({"error": "Error inserting into database. "}, 500)

class user_logout:
    def POST(self):
        new_request(self)
        data = web.input()

        try:
            sesh = data["sesh"].decode("utf-8")
        except KeyError:
            return write({"error": "Sesh can't be empty. "}, 400)
        except UnicodeError:
            return write({"error": "Sesh not UTF-8 encoded. "}, 400)

        user = get_user(sesh=sesh)

        if user is None:
            return write({"error": "Session doesn't exist. "}, 404)

        try:
            with pg.PgSimple() as db:
                db.delete("user_sessions", where=("user_id = %s", [user.id]))
                db.commit()
                return write({"message": "Successfully logged out. "}, 200)
        except:
            return write({"error": "Error logging out. "}, 500)
#########################################################
#
#               INIT STATEMENTS
#
#########################################################

if __name__ == "__main__":
    try:
        app = web.application(urls, globals())
        app.notfound = notfound
        app.run()
    except KeyboardInterrupt:
        print "Closed. "
