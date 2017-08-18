import web
import sys

import routes as Route

Index = Route.Index

urls = (
    '/',        'Index',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.notfound = Route.NotFound
    app.run()
