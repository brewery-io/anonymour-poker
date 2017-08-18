import web
import validators as Validate
import models as Model

class Login:

    def POST(self):

        data = Validate.User.POST(web.input())

        if data.is_valid:
            if Model.User.logged_in(data)
