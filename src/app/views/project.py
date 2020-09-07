import web
import models.project
from views.utils import get_nav_bar
from views.forms import project_form
import os
from shlex import quote
from time import sleep
import random

# Get html templates
render = web.template.render('templates/')


class Project:

    def GET(self):
        """
        Show info about a single project

            :return: Project info page
        """
    
        # Get session
        session = web.ctx.session
        # Get navbar
        nav = get_nav_bar(session)

        data = web.input(projectid=0)

        #anti csrf
        r = str(random.randint(0,10**10-1))
        anti_csrf = web.form.Form(web.form.Hidden("anti_csrf", value=r))
        models.user.set_anti_csrf(session.username, r)

        try:
            permissions = models.project.get_user_permissions(str(session.userid), data.projectid)
        except:
            permissions = [0,0,0]

        categories = models.project.get_categories()

        if data.projectid:
            project = models.project.get_project_by_id(data.projectid)
            tasks = models.project.get_tasks_by_project_id(data.projectid)
        else:
            project = [[]]
            tasks = [[]]
        render = web.template.render('templates/', globals={'get_task_files':models.project.get_task_files, 'session':session})
        return render.project(nav, project_form, project, tasks,permissions, categories, anti_csrf)

    def POST(self):
        # Get session
        session = web.ctx.session
        data = web.input(myfile={}, deliver=None, accepted=None, declined=None, projectid=0)
        fileitem = data['myfile']

         #anti csrf
        if data.anti_csrf != models.user.get_anti_csrf(session.username):
            raise web.seeother("/logout")
                
        permissions = models.project.get_user_permissions(str(session.userid), data.projectid)
        categories = models.project.get_categories()
        tasks = models.project.get_tasks_by_project_id(data.projectid)

        # Upload file (if present)
        try:
            if fileitem.filename:
                # Check if user has write permission
                if not permissions[1]:
                    raise web.seeother(('/project?projectid=' + data.projectid))

                fn = fileitem.filename

                #Check file name extension
                if not fn.lower().endswith(('.exe', '.pif', '.jar', '.bat', '.cmd', '.js', '.lnk')):
                    # Create the project directory if it doesnt exist
                    path = 'static/project' + data.projectid
                    if not os.path.isdir(path):
                        # command = 'mkdir ' + path
                        command = 'mkdir {}'.format(quote(path))
                        # print(command, flush=True)
                        os.popen(command)
                        sleep(0.2)
                    path = path + '/task' + data.taskid
                    if not os.path.isdir(path):
                        # command = 'mkdir ' + path
                        command = 'mkdir {}'.format(quote(path))
                        # print(command, flush=True)
                        os.popen(command)
                        sleep(0.2)
                    open(path + '/' + fn, 'wb').write(fileitem.file.read())
                    models.project.set_task_file(data.taskid, (path + "/" + fn))
        except:
            # Throws exception if no file present
            pass

        # Determine status of the targeted task
        all_tasks_accepted = True
        task_waiting = False
        task_delivered = False
        for task in tasks:
            if task[0] == int(data.taskid):  
                if(task[5] == "waiting for delivery" or task[5] == "declined"):
                    task_waiting = True
                if(task[5] == 'accepted'):
                    task_delivered = True

        # Deliver task
        if data.deliver and not task_delivered:
            models.project.update_task_status(data.taskid, "delivered")
        
        # Accept task delivery
        elif data.accepted:
            models.project.update_task_status(data.taskid, "accepted")

            # If all tasks are accepted then update project status to finished
            all_tasks_accepted = True
            tasks = models.project.get_tasks_by_project_id(data.projectid)
            for task in tasks:
                if task[5] != "accepted":
                    all_tasks_accepted = False
            if all_tasks_accepted:
                models.project.update_project_status(str(data.projectid), "finished")

        # Decline task delivery
        elif data.declined:
            models.project.update_task_status(data.taskid, "declined")
        
        raise web.seeother(('/project?projectid=' + data.projectid))

