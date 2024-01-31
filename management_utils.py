from sqlalchemy.orm import sessionmaker

# Import the Session object and engine from your construct_db.py file
from construct_db import *

class DB_Utils():

    def create_user(session, username, password):
        user = User(username=username, password=password)

        # Add the user to the database
        session.add(user)
        session.commit()

        # Get user's id
        return user.id

    def get_user_id(session, username):
        users = session.query(User).filter_by(username=username).all()

        if len(users) == 0:
            return 0
        
        return users[0].id

    def create_project(session, user_id, name, description):
        '''
        This method adds a project item to the database
        Parameters:
            creator: User
            name: str
            description: str      
        '''

        if name == None or len(name) == 0:
            return(["failure: project needs name\n", -1])

        # Create a Project object
        project = Project(name=name, description=description, admin_id=user_id)

        # Add the project to the database
        session.add(project)
        session.commit()

        # Put project into ProjectAssignments table
        project_assignment = ProjectAssignment(project_id=project.id, user_id=user_id)
        session.add(project_assignment)
        session.commit()

        return(["success\n", project.id])


    def get_projects(session, user_id):
        '''
        This method returns a dictionary of project objects.
        Returns:
            list of objects
        '''
        result = session.query(ProjectAssignment).filter_by(user_id=user_id).all()
        projects = []
        for item in result:
            project = session.query(Project).get(item.project_id)
            projects.append(
                {'id': project.id,
                'name': project.name,
                'description': project.description
                })
        return projects

    def get_projects_admin(session, user_id):

        result = session.query(Project).filter_by(admin_id=user_id).all()
        projects = []
        for item in result:
            projects.append(
                {'id': item.id,
                'name': item.name,
                'description': item.description
                })
        return projects

    def change_project_name(session, project_id, new_name):
        '''
        This method changes the name of the project to the new_name.
        Parameters:
            new_name: str
        '''
        if new_name == None or len(new_name) == 0:
            return "failure: project needs name\n"

        #project = session.query(Project).get(project_id)
        projects = session.query(Project).filter_by(id=project_id).all()
        if len(projects) > 0:
            projects[0].name = new_name
            session.commit()
            return "success\n"
        else:
            return "This project id does not exist\n"

    def change_project_description(session, project_id, new_description):
        '''
        This method changes the description of the project to the new_description.
        Parameters:
            new_description: str
        '''
        project = session.query(Project).get(project_id)

        if project:
            project.description = new_description
            session.commit()
            return "success\n"
        else:
            return "This project id does not exist\n"

    def invite_member(session, sender_id, sender_user, recipient_user, project_id=None, task_id=None):
        '''
        This method invites the member with a specified username to join the project.
        Parameters:
            username: str
        '''
        recipients = session.query(User).filter_by(username=recipient_user).all()

        if len(recipients) == 0:
            return "this username does not exist\n"
        
        recipient = recipients[0]

        if sender_id == recipient.id:
            return "You cannot invite yourself.\n"

        status = "pending"
        project = None
        task = None
        if project_id:
            project = session.query(Project).get(project_id)
        elif task_id:
            task = session.query(Task).get(task_id)

        # check if project or task item have been found
        if project:
            message = f"You have been invited to join Project: {project.name} by {sender_user}\n"
            notif = Message(sender_id = sender_id, recipient_id=recipient.id, project_id=project_id, message=message, status=status)
        elif task:
            message = f"You have been invited to join Task: {task.name} by {sender_user}\n"
            notif = Message(sender_id = sender_id, recipient_id=recipient.id, task_id=task_id, message=message, status=status)
        else:
            return "The project or task does not exist\n"
        
        session.add(notif)
        session.commit()
        return "Sent successfully\n"
        
    def remove_project_member(session, request_id, username, project_id):
        '''
        This method removes the member with a specified username from the sepcified project, if the requester is the admin.
        Parameters:
            username: str
        '''
        users = session.query(User).filter_by(username=username).all()
        if len(users) == 0:
            return "This username does not exist\n"
        user = users[0]

        project = session.query(Project).get(project_id)

        if not project:
            return "The project does not exist\n"

        if project.admin_id != request_id:
            return "You are not the admin of the project and are not allowed to remove members\n"
        
        if project.admin_id == user.id:
            return "You are the admin of the project, you are not allowed to remove yourself.\n"
        
        project_assignment = session.query(ProjectAssignment).filter_by(project_id=project_id, user_id=user.id).all()[0]
        session.delete(project_assignment)
        session.commit()
        return "Removed user successfully\n"

    def add_project_member(session, user_id, project_id):
        '''
        This method adds the user to a project.
        Parameters:
            user_id: int
            project_id: int
        '''
        project_assignment = ProjectAssignment(project_id=project_id, user_id=user_id)
        session.add(project_assignment)
        session.commit()
        return "Added user successfully\n"
    
    def get_tasks(session, user_id):
        '''
        This method returns a dictionary of task objects.
        Returns:
            list of objects
        '''
        result = session.query(TaskAssignment).filter_by(user_id=user_id).all()
        tasks = []
        for item in result:
            task = session.query(Task).get(item.task_id)
            tasks.append(
                {'id': task.id,
                'name': task.name,
                'description': task.description,
                'project_id': task.project_id,
                'priority': task.priority,
                'deadline': task.deadline
                })
        return tasks
    
    def get_tasks_admin(session, user_id):
        '''
        This method returns a dictionary of task objects.
        Returns:
            list of objects
        '''
        result = session.query(Task).filter_by(admin_id=user_id).all()
        tasks = []
        for item in result:
            tasks.append(
                {'id': item.id,
                'name': item.name,
                'description': item.description,
                'project_id': item.project_id,
                'priority': item.priority,
                'deadline': item.deadline
                })
        return tasks
    
    def create_task(session, user_id, name, description, priority, project_id=None, deadline=None):
        '''
        This method adds a project item to the database
        Parameters:
            creator: User
            name: str
            description: str      
        ''' 

        # Create a Task object
        task = Task(name=name, description=description, admin_id=user_id, priority=priority, project_id=project_id, deadline=deadline)

        # Add the project to the database
        session.add(task)
        session.commit()

        # Put project into TaskAssignments table
        task_assignment = TaskAssignment(task_id=task.id, user_id=user_id)
        session.add(task_assignment)
        session.commit()
        return task.id

    def change_task_name(session, task_id, new_name):
        '''
        This method changes the name of the project to the new_name.
        Parameters:
            new_name: str
        '''
        task = session.query(Task).get(task_id)
        if task:
            task.name = new_name
        session.commit()

    def change_task_description(session, task_id, new_description):
        '''
        This method changes the name of the project to the new_name.
        Parameters:
            new_name: str
        '''
        task = session.query(Task).get(task_id)
        if task:
            task.description = new_description
        session.commit()

    def change_task_priority(session, task_id, new_priority):
        '''
        This method changes the name of the project to the new_name.
        Parameters:
            new_name: str
        '''
        task = session.query(Task).get(task_id)
        if task:
            task.priority = new_priority
        session.commit()
    
    def change_task_deadline(session, task_id, new_deadline):
        '''
        This method changes the name of the project to the new_name.
        Parameters:
            new_name: str
        '''
        task = session.query(Task).get(task_id)
        if task:
            task.deadline = new_deadline
        session.commit()

    def remove_task_member(session, request_id, username, task_id):
        '''
        This method removes the member with a specified username from the sepcified task, if the requester is the admin.
        Parameters:
            username: str
        '''
        users = session.query(User).filter_by(username=username).all()
        if len(users)==0:
            return "This username does not exist\n"
        user = users[0]
        task = session.query(Task).get(task_id)

        if not task:
            return "The task does not exist\n"

        if task.admin_id != request_id:
            return "You are not the admin of the project and are not allowed to remove members\n"
        
        task_assignment = session.query(TaskAssignment).filter_by(task_id=task_id, user_id=user.id).all()[0]
        session.delete(task_assignment)
        session.commit()
        return "Removed user successfully\n"

    def add_task_member(session, user_id, task_id):
        '''
        This method adds the user to a project.
        Parameters:
            user_id: int
            project_id: int
        '''
        task_assignment = TaskAssignment(task_id=task_id, user_id=user_id)
        session.add(task_assignment)
        session.commit()
        return "Added user successfully\n"

    def read_notifications(session, user_id):
        '''
        This method gets all the user's notifications.
        Parameters:
            user_id: int
        '''
        result = session.query(Message).filter_by(recipient_id=user_id, status="pending").one()
        if result.project_id:
                #project notification
                id = result.project_id
                project = True
        else:
                #task notification
                id = result.task_id
                project = False
            
        notif = {'id': result.id,
                'sender': result.name,
                'project': project,
                'item_id': id,
                'message': result.message,
                'status': result.status
            }
        return notif
    
    def get_notifications(session, user_id): 
        result = session.query(Message).filter_by(recipient_id=user_id, status="pending").all()
        notifications = []
        for notif in result:
            if notif.project_id:
                #project notification
                id = notif.project_id
                project = True
            else:
                #task notification
                id = notif.task_id
                project = False

            sender = session.query(User).get(notif.sender_id)
            
            notifications.append(
                {'id': notif.id,
                'sender': sender.username,
                'project': project,
                'item_id': id,
                'message': notif.message,
                'status': notif.status
                })
        return notifications
    
    def delete_invitation(session, message_id):
        message = session.query(Message).get(message_id)
        if message:
            session.delete(message)
        # commit (or flush)
        session.commit()

    def notifications_length(session, user_id):
        '''
        This method returns the amount of notifications the user has
        Returns:
            int - amount of notifications     
        '''
        return len(session.query(Message).filter_by(recipient_id=user_id, status="pending").all())            
    
    def change_invitation_status(session, message_id, new_status):
        
        message = session.query(Message).get(message_id)
        message.status = new_status

        session.commit()

    def delete_project(session, user_id, project_id):
        # check that project exists
        project = session.query(Project).get(project_id)

        if not project:
            return "The project does not exist.\n"
        
        # check that user is the admin of the project
        if project.admin_id != user_id:
            return "You are not the admin of the task and are not allowed to delete it.\n"

        # remove project from Projects
        session.delete(project)

        # remove project_assignments from Project_Assignments
        project_assignment = session.query(ProjectAssignment).filter_by(project_id=project_id).all()
        for assignment in project_assignment:
            session.delete(assignment)
        session.commit()

        # delete the tasks associated with that project
        project_tasks = session.query(Task).filter_by(project_id=project_id).all()
        for task in project_tasks:
            session.delete(task)
        session.commit()

        return "Removed project successfully\n"


    def delete_task(session, user_id, task_id):
        # check that task exists
        task = session.query(Task).get(task_id)

        if not task:
            return "The task does not exist\n"

        # check that user is the admin of the project
        if task.admin_id != user_id:
            return "You are not the admin of the task and are not allowed to delete it.\n"

        # remove task from Tasks table
        session.delete(task)

        # remove task_assignments from Task_Assignments
        task_assignment = session.query(TaskAssignment).filter_by(task_id=task_id).all()
        for assignment in task_assignment:
            session.delete(assignment)
        session.commit()

        return "Removed task successfully\n"
