import web
from views.forms import register_form
import models.register
import models.user
from views.utils import get_nav_bar
import hashlib
import re
import random
import views.utils

# Get html templates
render = web.template.render('templates/')


class Register:

    def GET(self):
        """
        Get the registration form

            :return: A page with the registration form
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.register(nav, register_form, "")

    def POST(self):
        """
        Handle input data and register new user in database

            :return: Main page
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()
        register = register_form()
        if not register.validates():
            return render.register(nav, register, "All fields must be valid.")
        # Check if user exists
        if models.user.get_user_id_by_name(data.username):
            return render.register(nav, register, "Invalid user, already exists.")
        salt = str(random.randint(0,10**10-1))
        string_hash = views.utils.hash_string(data.password,salt)
        mail_verified = str(random.randint(0,10**10-1))

        models.register.set_user(data.username, 
            string_hash, salt, mail_verified,
            data.full_name, data.company, data.email, data.street_address, 
            data.city, data.state, data.postal_code, data.country)
        try:    
            web.sendmail('Beelance@molde.idi.ntnu.no', data.email, 'verification', mail_verified)
        except:
            print(mail_verified)
        raise web.seeother("/verify")

