import models.user
from views.utils import get_nav_bar
import models.googleAuthenticator
from views.login import Login
import web
from views.forms import login_form
from views.forms import authenticator_form
import models.user
from views.utils import get_nav_bar
import os, hmac, base64, pickle
import hashlib
import models.googleAuthenticator

# Get html templates
render = web.template.render('templates/')


class Authenticator:
    secret = web.config.get('session_parameters')['secret_key']

    # Get the server secret to perform signatures
    # secret = web.config.get('session_parameters')['secret_key']

    def GET(self):
        """
        Show the login page

            :return: The login page showing other users if logged in
        """
        session = web.ctx.session
        if not hasattr(session, "newTwoAuth"):
            session.newTwoAuth = False
        nav = get_nav_bar(session)

        # Log the user in if the rememberme cookie is set and valid
        return render.authenticator(nav, authenticator_form, "")


    def POST(self):
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input(token="")
        if not hasattr(session, "twoAuth"):
            return render.authenticator(nav, authenticator_form, "You need to log in first")
        else:
            if data.token == models.googleAuthenticator.get_totp_token(session.twoAuth) :
                if session.newTwoAuth :
                    models.user.insert_twoauth_by_name(session.tempusername, session.twoAuth)
                self.login(session.tempusername, session.tempuserid, session.tempremember)
                raise web.seeother("/")

        return render.authenticator(nav, authenticator_form, "Your token doesn't match")

    def login(self, username, userid, remember):
        """
        Log in to the application
        """
        session = web.ctx.session
        session.username = username
        session.userid = userid
        if remember:
            rememberme = self.rememberme()
            web.setcookie('remember', rememberme , 300000000)

        models.user.update_login_info_by_username(username)

    def rememberme(self):
        """
        Encode a base64 object consisting of the username signed with the
        host secret key and the username. Can be reassembled with the
        hosts secret key to validate user.
            :return: base64 object consisting of signed username and username
        """
        session = web.ctx.session
        creds = [ session.username, self.sign_username(session.username) ]
        return base64.b64encode(pickle.dumps(creds))

    @classmethod
    def sign_username(self, username):
        """
        Sign the current users name with the hosts secret key
            :return: The users signed name
        """
        secret = base64.b64decode(self.secret)
        return hmac.HMAC(secret, username.encode('ascii')).hexdigest()