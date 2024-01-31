import datetime
from Users import AllUsers, User
from random import randint

class AllTasks:
    '''
    This class is responsible for storing all the Task objects.
    '''
    _instance = None
    def __new__(cls):
        '''
        This method creates a single of the class AllTasks, and makes it 
        so that this class can be used as a dictionary of all the tasks
        Parameters:
            instance of the class
        Returns:
            instance of the class
        '''
        if cls._instance is None:
            cls._instance = super(AllTasks, cls).__new__(cls)
            cls._instance.tasks = {}
        return cls._instance

    def add_task(self, task):
        '''
        This method adds a task to the dictionary of tasks.
        Parameters:
            task: Task object
        '''
        if isinstance(task, Task):
            self.tasks[task.task_id] = task

    def get_tasks(self):
        '''
        This method returns a dictionary of task objects.
        Returns:
            list of Task objects
        '''
        return self.tasks

class Task:
    '''
    This class represents a task which has properties and methods for 
    working with the task.
    Attributes:
        - task id
        - task name
        - task description
        - task project id
        - priority of task
        - deadline of task
        - memmbers of the task
    '''
    def __init__(self, creator: User, name: str, desription: str, project_id: int, priority: int, deadline: datetime.date):
        '''
        This method initialized all the attributes of the task to the inputs.
        Parameters:
            creator: User
            name: str
            description: str
            project_id: int
            priority: int
            deadline: datetime.date        
        '''
        self.task_id = randint(100000000000, 999999999999)
        self.name = name
        self.desription = desription
        self.project_id = project_id
        self.priority = priority
        self.deadline = deadline
        self.members = {creator.username: creator}
        AllTasks().add_task(self)

    def change_task_name(self, new_name: str):
        '''
        This method changes the name of the task to the new_name.
        Parameters:
            new_name: str
        '''
        self.name = new_name

    def change_task_description(self, new_description: str):
        '''
        This method changes the description of the task to the new_description.
        Parameters:
            new_description: str
        '''
        self.desription = new_description

    def change_task_priority(self, new_priority: int):
        '''
        This method changes the priority of the task to the new_priority.
        Parameters:
            new_priority: str
        '''
        self.priority = new_priority

    def change_task_deadline(self, new_deadline: datetime.date):
        '''
        This method changes the deadline of the task to the new_deadline.
        Parameters:
            new_deadline: str
        '''
        self.deadline = new_deadline

    def invite_member(self, username: str):
        '''
        This method invites the member with a specified username to join the task.
        Parameters:
            username: str
        '''
        user = AllUsers().get_users().get(username)
        # sends a notification to the invited user that they've been invited
        user.add_notification(
            "task",
            self.task_id,
            "You have been invited to join Task:"
            f"{self.name} under the ID: {self.task_id}\n")
        
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
        user.add_to_task(self)
        