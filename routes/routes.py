import web
import os
import glob
import sys

# sys.path.insert(0, '..')
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

base = os.path.dirname(os.path.realpath(__file__))

html = '''
<!DOCTYPE html >
<html >
<head >
<title >title | %s</title>
<style >
%s
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js" ></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-cookie/2.1.4/js.cookie.min.js" ></script>
</head>
<body >
%s
</body>
<script >
%s
</script>
</html>
'''

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
            page = 'welcome'
        else:
            page = 'home'

        with open(os.path.join(base, 'html/%s.html' % page), 'r') as f:
            body = f.read()

        with open(os.path.join(base, 'css/%s.css' % page), 'r') as f:
            style = f.read()

        script = ''
        for fname in glob.glob(os.path.join(base, 'js/%s.*.js' % page)):
            with open(os.path.join(base, fname), 'r') as f:
                script += f.read()

        return html % (page, style, body, script)

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
