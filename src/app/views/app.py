import os
import web
from views.utils import get_nav_bar
from views.login import Login
from views.logout import Logout
from views.register import Register
from views.new_project import New_project
from views.open_projects import Open_projects
from views.authenticator import Authenticator
from views.project import Project
from views.index import Index
from views.apply import Apply
from views.verify import Verify
from views.reset import Reset


web.config.debug = False
# Connect to smtp server, enables web.sendmail()
try:
    smtp_server = os.getenv("smtp_server") + ":25"
    web.config.smtp_server = smtp_server 
except:
    smtp_server = "molde.idi.ntnu.no:25"
    web.config.smtp_server = smtp_server

# Example use of the smtp server, insert username
# web.sendmail("beelance@ntnu.no", "<username>@stud.ntnu.no", "Hello", "Grz, the beelance app is running")

# Define application routes
urls = (
    '/', 'Index',
    '/login', 'Login',
    '/logout', 'Logout',
    '/register', 'Register',
    '/new_project', 'New_project',
    '/open_projects', 'Open_projects',
    '/project', 'Project',
    '/apply', 'Apply',
    '/verify', 'Verify',
    '/reset', 'Reset',
    '/authenticator', 'Authenticator',
)
                              
# Initialize application using the web py framework
app = web.application(urls, globals())

# Get html templates
render = web.template.render('templates/')

# Set session timeout
web.config.session_parameters['timeout'] = 150000

# Workaround to use sessions with reloader (debugger) http://webpy.org/cookbook/session_with_reloader
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

# Add session to global variables
render._add_global(session, 'session')

# Make the session available cross modules through webctx
def session_hook():
    web.ctx.session = session
    web.template.Template.globals['session'] = session

app.add_processor(web.loadhook(session_hook))

app = app.wsgifunc()


