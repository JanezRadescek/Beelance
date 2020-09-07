import web
from views.forms import verify_form
import models.user
from views.utils import get_nav_bar
import os, hmac, base64, pickle
import hashlib
import random

# Get html templates
render = web.template.render('templates/')


class Verify():

    # Get the server secret to perform signatures
    secret = web.config.get('session_parameters')['secret_key']

    def GET(self):
        """
        Verify mail form.
        """
        session = web.ctx.session
        nav = get_nav_bar(session)

        return render.verify(nav, verify_form)

    def POST(self):
        """
        Update data base.
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()
      
        # Validate email with database query
        verified = models.user.validate_mail(data.username, data.number)
        if verified:
            raise web.seeother("/login")
        
        return render.verify(nav, verify_form)

 