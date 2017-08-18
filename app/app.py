import web
import os
import glob
import sys

import helpers as Help
import routes as Route

sys.path.insert(0, '../config')
import config

Index = Route.Index

urls = (
    '/',        'Index',
)

class Data:
    pass


render = web.template.render('templates/', base='layout')

def not_found():
    return web.notfound('Oh No')

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.notfound = not_found
    app.run()

def start():
    sys.argv[1] = config.Routes.port
    app = web.application(urls, globals())
    app.notfound = not_found
    app.run()
