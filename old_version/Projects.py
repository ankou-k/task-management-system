from Users import AllUsers, User
from random import randint

class AllProjects:
    '''
    This class is responsible for storing all the Project objects.
    '''
    _instance = None
    def __new__(cls):
        '''
        This method creates a single of the class AllProjects, and makes it 
        so that this class can be used as a dictionary of all the projects
        Parameters:
            instance of the class
        Returns:
            instance of the class
        '''
        if cls._instance is None:
            cls._instance = super(AllProjects, cls).__new__(cls)
            cls._instance.projects = {}
        return cls._instance

    def add_project(self, project):
        '''
        This method adds a project to the dictionary of projects.
        Parameters:
            project: Project object
        '''
        if isinstance(project, Project):
            self.projects[project.project_id] = project

    def get_projects(self):
        '''
        This method returns a dictionary of project objects.
        Returns:
            list of Project objects
        '''
        return self.projects

class Project:
    '''
    This class represents a project which has properties and methods for 
    working with the project.
    Attributes:
        - project id
        - project name
        - project description
        - admin of the project
        - members of the project
        - tasks of the project
    '''
    def __init__(self, creator: User, name: str, description: str):
        '''
        This method initialized all the attributes of the project to the inputs.
        Parameters:
            creator: User
            name: str
            description: str      
        '''
        self.name = name
        self.project_id = randint(100000000000, 999999999999)
        self.description = description
        self.members = {creator.username: creator}
        self.admin = creator.username
        self.tasks = {}
        AllProjects().add_project(self)

    def change_project_name(self, new_name: str):
        '''
        This method changes the name of the project to the new_name.
        Parameters:
            new_name: str
        '''
        self.name = new_name

    def change_project_description(self, new_description: str):
        '''
        This method changes the description of the project to the new_description.
        Parameters:
            new_description: str
        '''
        self.description = new_description

    def invite_member(self, username: str):
        '''
        This method invites the member with a specified username to join the project.
        Parameters:
            username: str
        '''
        user = AllUsers().get_users().get(username)
        # sends a notification to the invited user that they've been invited
        user.add_notification(
            "project",
            self.project_id,
            "You have been invited to join Project:"
            f"{self.name} under the ID: {self.project_id}\n")
        
    def remove_member(self, username: str):
        '''
        This method removes the member with a specified username.
        Parameters:
            username: str
        '''
        self.members[username] = None

    def add_member(self, user: User):
        '''
        This method adds the member with a specified username.
        Parameters:
            username: str
        '''
        self.members[user.username] = user
        user.add_to_project(self)
    