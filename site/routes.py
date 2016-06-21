import web
import os

#########################################################
#
#               INITIAL SETTINGS
#
#########################################################

urls = (
	"/", "index",
	"/login", "login",
	"/panel", "panel"
)

base = os.path.dirname(os.path.realpath(__file__))

def write(payload, status):
	payload["status"] = status
	return json.dumps({"payload": payload, "status": status})

def notfound():
	web.header("Content-Type", "text/html")
	return web.notfound("404")

def new_request(request):
	web.header("Content-Type", "text/html")
	web.header("Access-Control-Allow-Origin", "*")
	# request_info = {}
	# request_info["ip"] = web.ctx["ip"]
	# request_info["type"] = "POST"
	# request_info["time"] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	# request_id = requests.insert_one(request_info).inserted_id

class index:
	def GET(self):
		new_request(self)

		with open("%s/static/home.html" % base, "r") as f:
			return f.read()

class login:
	def GET(self):
		new_request(self)

		with open("%s/static/login.html" % base, "r") as f:
			return f.read()

class panel:
	def GET(self):
		new_request(self)

		with open("%s/static/panel.html" % base, "r") as f:
			return f.read()


#########################################################
#
#               INIT STATEMENTS
#
#########################################################

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()
