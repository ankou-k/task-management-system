# Import the Session object and engine from your construct_db.py file
from construct_db import *
from management_utils import DB_Utils

class Person():
    def __init__(self, session, username: str, password: str, login_signup: str):
        '''
        This is the constructor to initialize a new user.
        Parameters:
            username: str
            password: str      
        '''
        self.username = username

        self.session = session

        if login_signup == "signup":
            # Create a User object
            user = User(username=username, password=password)

            # Add the user to the database
            session.add(user)
            session.commit()

            # Get user's id
            self.id = user.id
        else:
            stmt = select(User).where(User.username == username)
            results = session.execute(stmt)
            row = results.one()
            self.id = row[0].id

        # Close the Session
        session.close()

    def create_project(self, name, description):
        DB_Utils.create_project(self.session, self.id, name, description)

    def view_projects(self):
        projects = DB_Utils.get_projects(self.session, self.id)

        if len(projects) > 0:
            for project in projects:
                print(f"ID: {project['id']} Name: {project['name']} Description: {project['description']}\n")
        else:
            print("You have no projects.\n")

    def view_admin_projects(self):
        projects = DB_Utils.get_projects_admin(self.session, self.id)

        if len(projects) > 0:
            for project in projects:
                print(f"ID: {project['id']} Name: {project['name']} Description: {project['description']}\n")
        else:
            print("You have no projects that you admin.\n")

    def admin_projects_length(self):
        projects = DB_Utils.get_projects_admin(self.session, self.id)
        return len(projects)
    
    def admin_project_IDs(self):
        projects = DB_Utils.get_projects_admin(self.session, self.id)
        IDs = []
        for project in projects:
            IDs.append(str(project['id']))
        return IDs

    def change_project_name(self, project_id, new_name):
        DB_Utils.change_project_name(self.session, project_id, new_name)

    def change_project_description(self, project_id, new_description):
        DB_Utils.change_project_description(self.session, project_id, new_description)

    def invite_member(self, recipient_user, project_id=None, task_id=None):
        result = DB_Utils.invite_member(self.session, self.id, self.username, recipient_user, project_id, task_id)
        print(result)

    def remove_project_member(self, username, project_id):
        result = DB_Utils.remove_project_member(self.session, self.id, username, project_id)
        print(result)

    def add_project_member(self, project_id):
        result = DB_Utils.add_project_member(self.session, self.id, project_id)
        print(result)

    def create_task(self, name, description, priority, project_id=None, deadline=None):
        DB_Utils.create_task(self.session, self.id, name, description, priority, project_id, deadline)

    def change_task_name(self, task_id, new_name):
        DB_Utils.change_task_name(self.session, task_id, new_name)

    def change_task_description(self, task_id, new_description):
        DB_Utils.change_task_description(self.session, task_id, new_description)
    
    def change_task_priority(self, task_id, new_priority):
        DB_Utils.change_task_priority(self.session, task_id, new_priority)

    def change_task_deadline(self, task_id, new_deadline):
        DB_Utils.change_task_deadline(self.session, task_id, new_deadline)

    def add_task_member(self, task_id):
        result = DB_Utils.add_task_member(self.session, self.id, task_id)
        print(result)

    def remove_task_member(self, task_id):
        result = DB_Utils.remove_task_member(self.session, self.id, task_id)
        print(result)

    def get_notifications(self): 
        return DB_Utils.get_notifications(self.session, self.id)

    def notifications_length(self):
        return DB_Utils.notifications_length(self.session, self.id)
    
    def change_invitation_status(self, message_id, new_status):
        DB_Utils.change_invitation_status(self.session, message_id, new_status)

    def delete_project(self, project_id):
        result = DB_Utils.delete_project(self.session, self.id, project_id)
        print(result)
    
    def delete_task(self, task_id):
        result = DB_Utils.delete_task(self.session, self.id, task_id)
        print(result)


    