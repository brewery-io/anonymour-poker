import helpers as Help

class Index:
    def GET(self):

        Help.Request.new_route()

        token = web.cookies().get('token')

        print Help.Token.is_valid(token)

        if token is None:
            return render.welcome()
        else:
            return render.home(data)
