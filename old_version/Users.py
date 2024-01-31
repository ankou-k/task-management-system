from typing import List

class AllUsers:
    '''
    This class is responsible for storing all the User objects.
    '''
    _instance = None
    def __new__(cls):
        '''
        This method creates a single of the class AllUsers, and makes it 
        so that this class can be used as a dictionary of all the users
        Parameters:
            instance of the class
        Returns:
            instance of the class
        '''
        if cls._instance is None:
            cls._instance = super(AllUsers, cls).__new__(cls)
            cls._instance.users = {}
        return cls._instance

    def add_user(self, user):
        '''
        This method adds a user to the list of users.
        Parameters:
            user: User object
        '''
        if isinstance(user, User):
            self.users[user.username] = user

    def get_users(self):
        '''
        This method returns a list of user objects.
        Returns:
            list of User objects
        '''
        return self.users
    
class User:
    '''
    This class represents a user which has properties and methods needed for
    the user to interact with the system.
    Attributes:
        - username
        - password
        - user's tasks
        - user's projects
        - user's noifications
    '''
    def __init__(self, username: str, password: str):
        '''
        This is the constructor to initialize a new user.
        Parameters:
            username: str
            password: str      
        '''
        self.username = username
        self.password = password
        self.tasks = {}
        self.projects = {}
        self.notifications = []
        AllUsers().add_user(self)
    
    def add_notification(self, project_or_task: str, ID: int, message: str):
        '''
        This method adds a notification to the user's list of notifications.
        Parameters:
            project_or_task: str
            ID: int
            message: str
        '''
        self.notifications.append([project_or_task, ID, message])

    def notifications_length(self):
        '''
        This method returns the amount of notifications the user has
        Returns:
            int - amount of notifications     
        '''
        return len(self.notifications)
    
    def read_notification(self):
        '''
        This method returns the first notification from the list of the 
        user's notification if the user has notifications. If the user
        does not have any notifications, the method returns a string indicating that.
        Returns:
            string
        '''
        if len(self.notifications) > 0:
            return self.notifications.pop(0)
        else:
            return "You have no new notifications.\n"
    
    def tasks_length(self):
        '''
        This method returns the amount of tasks the user has
        Returns:
            int - amount of tasks    
        '''
        return len(self.tasks)
    
    def projects_length(self):
        '''
        This method returns the amount of projects the user has
        Returns:
            int - amount of projects   
        '''
        return len(self.projects)
    
    def view_tasks(self):
        '''
        This method prints all of the user's tasks, or returns a string
        if there are no tasks.
        Returns:
            str
        '''
        if len(self.tasks) > 0:
            for task in self.tasks.values():
                print(f"Name: {self.task.name} ID: {self.task.task_id}\n")
        else:
            return "You have no tasks.\n"
    
    def view_projects(self):
        '''
        This method prints all of the user's projects, or returns a string
        if there are no projects.
        Returns:
            str
        '''
        if len(self.projects) > 0:
            for project in self.projects.values():
                print(f"Name: {self.project.name} ID: {self.project.project_id}\n")
        else:
            return "You have no projects.\n"
    
    def add_to_project(self, project):
        '''
        This method adds a new project to the user's dictionary of projects
        Parameters:
            project: Project
        '''
        self.projects[project.project_id] = project
    
    def add_to_task(self, task):
        '''
        This method adds a new project to the user's dictionary of tasks
        Parameters:
            task: Task
        '''
        self.tasks[task.task_id] = task

    def __str__(self):
        '''
        This method defines how a user object is represented when printed.
        '''
        return self.username