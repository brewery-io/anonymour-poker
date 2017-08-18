import web
import os
import glob
import sys

sys.path.insert(0, '..')
from config import config

#########################################################
#
#               INITIAL SETTINGS
#
#########################################################


urls = (
    '/',        'Index',
    '/login',   'Login',
    '/game',    'Game',
)

class Data:
    pass

def write(payload, status):
    payload['status'] = status
    return json.dumps({'payload': payload, 'status': status})

def not_found():
    new_request()
    return web.notfound('Not found!')

def new_request():
    web.header('Content-Type', 'text/html')
    web.header('Access-Control-Allow-Origin', '*')
    web.setcookie('api', config.API.url)

render = web.template.render('templates/', base='layout')

#########################################################
#
#               ROUTES
#
#########################################################

class Index:
    def GET(self):

        new_request()

        token = web.cookies().get('token')

        if token is None:
            return render.welcome(data)
        else:
            page = 'home'

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

def start():
    sys.argv[1] = config.Routes.port
    app = web.application(urls, globals())
    app.notfound = not_found
    app.run()
