import web
import helpers as Help

class Index:

    def GET(self):

        Help.Request.new_route()

        token = web.cookies().get('token')

        print Help.Token.is_valid(token)

        render = web.template.render('templates')

        if not Help.Token.is_valid(token):
            return Help.Render.home()
        else:
            return Help.Render.welcome()
