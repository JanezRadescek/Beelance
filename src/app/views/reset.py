import web
from views.forms import request_reset_form
from views.forms import reset_form
import models.user
from views.utils import get_nav_bar
import os, hmac, base64, pickle
import models.user
import random
import views.utils

# Get html templates
render = web.template.render('templates/')


class Reset():

    def GET(self):
        """
        Show the reset page
            
            :return: The reset page showing form for reseting password
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        return render.reset(nav, request_reset_form, "")

    def POST(self):
        """
        Send temporary password on mail.
            :return: The reset page showing form for reseting password
        """
        session = web.ctx.session
        nav = get_nav_bar(session)
        data = web.input()

        try:
            request_reset = request_reset_form()
            if not request_reset.validates():
                return render.reset(nav, request_reset, "All fields must be valid.")
            temp_password = str(random.randint(0,10**10-1))
            try:    
                web.sendmail('Beelance@molde.idi.ntnu.no', data.mail, 'reset password', temp_password)
            except:
                print(temp_password)
            
            salt = models.user.get_salt(data.username)
            hash_temp_password = views.utils.hash_string(temp_password, salt)
            result = models.user.set_temp_password(data.username, data.mail, hash_temp_password)
            if result:
                return render.reset(nav, reset_form, "Check mail for temporary password.")
            else:
                return render.reset(nav, request_reset_form, "Username and email does not match.")

        except:
            reset = reset_form()
            if not reset.validates():
                return render.reset(nav, reset_form, "All fields must be valid.")

            if data.new_password1 != data.new_password2:
                return render.reset(nav, reset_form, "New passwords must be the same.")
            
            salt = models.user.get_salt(data.username)
            hash_temporary_password = views.utils.hash_string(data.temporary_password, salt)
            hash_new_password = views.utils.hash_string(data.new_password1, salt)
            if models.user.change_password(data.username, hash_temporary_password, hash_new_password):
                raise web.seeother("/login")
            else:
                return render.reset(nav, reset_form, "username and/or temp pasword is not corect.")
        
        return render.reset(nav, request_reset_form, "Unknown Error")
