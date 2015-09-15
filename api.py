import SimpleHTTPServer
import SocketServer
import cgi
import sys
import score
import json

if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""

def return_json(payload, status, request_id):
    json_obj = {"error": message, "status": status, "request_id": request_id}
    json_str = json.dumps(json_obj)
    # print json_str

def new_request():
    return ""

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):

        request_id = new_request()

        # print self.headers
        # print self.client_address[0]

        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )
        for key in form.keys():

            if key == "action":
                action = form.getValue(key)

            if action == "score":

                if "cards" in form.keys():
                    cards = form.getvalue("cards");
                    result = score.api_main(cards)

                    if result:
                        return_json({"result": result}, 200, request_id)

                    else:
                        return_json({"error": "Invalid cards. "}, 202, request_id)
                else:
                    return_json({"error": "Cards not supplied. "}, 201, request_id)

    def end_headers(self):
        self.send_headers()
        SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def send_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*" )
        self.send_header("Content-Type": "application/json")

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at: http://%(interface)s:%(port)s" % dict(interface = I or "localhost", port = PORT)
httpd.serve_forever()
