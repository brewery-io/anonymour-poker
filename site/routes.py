import web
import os

#########################################################
#
#               INITIAL SETTINGS
#
#########################################################

urls = (
    '/', 'Home',
    '/login', 'Login',
    '/game', 'Game',
)

base = os.path.dirname(os.path.realpath(__file__))

def write(payload, status):
    payload['status'] = status
    return json.dumps({'payload': payload, 'status': status})

def not_found():
    new_request()
    return web.notfound('Not found!')

def new_request():
    web.header('Content-Type', 'text/html')
    web.header('Access-Control-Allow-Origin', '*')


class Home:
    def GET(self):
        new_request()

        with open(os.path.join(base, 'html/home.html'), 'r') as f:
            return f.read()

class Login:
    def GET(self):
        new_request()
        page = 'login'
        with open('%s/static/login.html' % base, 'r') as f:
            return f.read()

class Game:
    def GET(self):
        new_request()
        page = 'game'
        with open('%s/static/game.html' % base, 'r') as f:
            return f.read()

#########################################################
#
#               INIT STATEMENTS
#
#########################################################

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.notfound = not_found
    app.run()
