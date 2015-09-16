import web

urls = ("/", "index",
        '/hello', "hello",

)

def notfound():
    web.header("Content-Type", "application/json")
    return web.notfound('{"payload": {"error_message": "Endpoint not found. "}, "status": 404}')

class index:
    def GET(self):
        web.header("Content-Type", "application/json")
        return "Hello, World!"

class hello:
    def GET(self):
        return "hello thing"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
