from Users import AllUsers
from Tasks import Task
from Projects import Project
import re
import datetime
from construct_db import *

class InputHandler:
    '''
    This class handles all input-validation of interacting with the user through the cli.
    The class is used by main.py
    '''
    def Handler(error_message: str, input_message: str, condition: str, add_info=None):
        '''
        This function is responsible for calling the necessary methods to make sure that the input is valid. It needs an error message, 
        a prompt message, a condition name, and an optional user parameter in order to obtain valid input.
        Parameters:
            error_message: str
            input_message: str
            condition: str 
            user: User object
        Returns:
            input_value: str
        '''
        input_value = ""
        first_entry = True

        # this loops until the while_condition function returns true, which would signify that user input is valid
        while InputHandler.while_condition(condition, input_value, add_info):

            # check if entering this loop for the first time, if no then print error message for invalid input
            if not first_entry:
                print(error_message)
            
            # read in user input
            input_value = input(input_message)
            first_entry = False
            print()

        # return the valid user input
        return input_value
    
    def while_condition(condition, input_check, add_info=None):
        '''
        This function calls the relevant method based on the condition string, passing in the user input into it.
        It then returns whether the input met the condition and hence does not need to rerun test (false) 
        or did not meet the condition and needs to rerun (true)
        Parameters:
            condition: str
            input_check: str
            user: User object
        Returns:
            boolean - false if condition is met and loop can end, true otherwise
        '''
        match condition:
                # check for entry menu selection being valid
                case "entry_method":
                    return InputHandler.entry_method_condition(input_check)
                # check for existing username
                case "login_username":
                    return InputHandler.login_username_condition(input_check)
                # check for correct password
                case "login_password":
                    return InputHandler.login_password_condition(add_info, input_check)
                # check for non-taken username
                case "signup_username":
                    return InputHandler.signup_username_condition(input_check)
                # check for valid password
                case "signup_password":
                    return InputHandler.signup_password_condition(input_check)
                # check for home menu selection being valid
                case "home_navigation":
                    return InputHandler.home_navigation_condition(input_check)
                # check for project acceptance selection being valid
                case "project_task_acceptance":
                    return InputHandler.project_task_acceptance_condition(input_check)
                # check for task menu selection being valid
                case "task_navigation":
                    return InputHandler.task_navigation_condition(input_check)
                # check for which task to edit input is valid
                case "task_edit_navigation":
                    return InputHandler.task_edit_navigation_condition(input_check)
                # check that project creation input is valid
                case "task_creation":
                    return InputHandler.task_creation_condition(add_info, input_check)
                # check for project menu selection being valid
                case "project_navigation":
                    return InputHandler.project_navigation_condition(input_check)
                # check for which project to edit input is valid
                case "project_edit_navigation":
                    return InputHandler.project_edit_navigation_condition(add_info, input_check)
                case "project_edit_navigation2":
                    return InputHandler.project_edit_navigation_condition2(input_check)
                case "project_name_edit":
                    return InputHandler.project_name_edit_condition(input_check)
                case "project_description_edit":
                    return InputHandler.project_description_edit_condition(input_check)
                # check that project creation input is valid
                case "project_creation":
                    return InputHandler.project_creation_condition(add_info, input_check)
    
    def entry_method_condition(entry_method):
        '''
        This method checks that the input for the entry menu selection is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        return entry_method not in ("1", "2", "3")

    def login_username_condition(login_username):
        '''
        This method checks for existing username,
        returns True if not non-existant, False if exists.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''

        user_exists = False
        Session = sessionmaker(bind=engine)
        session = Session()
        stmt = select(User).where(User.username == login_username)
        results = session.execute(stmt)
        try:
            row = results.one()
            user_exists = True
        except:
            user_exists = False
        session.close()

        return (not user_exists) and (login_username != "SU")
    
    def login_password_condition(username, login_password):
        '''
        This method checks for correct password to associated username,
        returns True if not correct, False otherwise.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''

        Session = sessionmaker(bind=engine)
        session = Session()
        stmt = select(User).where(User.username == username)
        results = session.execute(stmt)
        row = results.one()
        session.close()

        return (row[0].password != login_password) and (login_password != "SU")
    
    def signup_username_condition(signup_username):
        '''
        This method checks for unique new username,
        returns True if not valid, False otherwise.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        regex_signup_username = r'^[A-Za-z0-9]{3,20}$'
        
        user_exists = False
        Session = sessionmaker(bind=engine)
        session = Session()
        stmt = select(User).where(User.username == signup_username)
        results = session.execute(stmt)
        try:
            row = results.one()
            user_exists = True
        except:
            user_exists = False
        session.close()
        
        return (not re.match(regex_signup_username, signup_username) or user_exists) and (signup_username != "LI")
    
    def signup_password_condition(signup_password):
        '''
        This method checks for valid password,
        returns True if not valid, False otherwise.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        regex_signup_password = r'^[A-Za-z0-9-_.!@#$%^&*()]{8,30}$'
        return (not re.match(regex_signup_password, signup_password)) and (signup_password != "LI")
    
    def home_navigation_condition(home_navigation):
        '''
        This method checks that the input for the home menu selection is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        return home_navigation not in ("1", "2", "3", "4")
    
    def project_task_acceptance_condition(project_task_acceptance):
        '''
        This method checks that the input for the project acceptance menu selection is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        return project_task_acceptance not in ("1", "2")
    
    def task_navigation_condition(task_navigation):
        '''
        This method checks that the input for the task menu selection is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        return task_navigation not in ("1", "2", "3", "4", "5")
    
    def task_edit_navigation_condition(task_edit_navigation):
        '''
        This method checks that the input for which task to edit is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        return (task_edit_navigation not in ("1", "2", "3", "4", "5")) and (task_edit_navigation != "B")
    
    def task_creation_condition(username, task_creation):
        '''
        This method checks that the input for project creation is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        task_creation = task_creation.split(',')
        task_creation = [task_part.strip() for task_part in task_creation]
        valid_task_creation = False

        # check if task creation information is of correct types 
        if isinstance(task_creation[0], str) and len(task_creation[0]) > 0 \
        and isinstance(task_creation[1], str) and len(task_creation[1]) > 0 \
        and task_creation[2].isdigit() and task_creation[3].isdigit() and \
        1 <= int(task_creation[3]) <= 7:
            valid_task_creation = True

        # attempt to get all the details and create a task, if fail then return unsucessful task creation
        if valid_task_creation:
            try:
                year, month, day = map(int, task_creation[-1].split('-'))
                date = datetime.date(year, month, day)
                task = Task(user, task_creation[0], task_creation[1],
                int(task_creation[2]), int(task_creation[3]), date)
            except:
                valid_task_creation = False
        return not valid_task_creation and (task_creation != "B")
    
    def project_navigation_condition(project_navigation):
        '''
        This method checks that the input for the project menu selection is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        return project_navigation not in ("1", "2", "3", "4")
    
    def project_edit_navigation_condition(user, project_edit_navigation):
        '''
        This method checks that the input for which project to edit is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        return (project_edit_navigation not in user.admin_project_IDs()) and (project_edit_navigation != "B")
    
    def project_edit_navigation_condition2(project_edit_navigation2):
        return project_edit_navigation2 not in ("1", "2", "3", "4", "5")
    
    def project_name_edit_condition(project_name_edit):
        return project_name_edit is ""
    
    def project_description_edit_condition(project_description_edit):
        return project_description_edit is ""
   
    def project_creation_condition(user, project_creation):
        '''
        This method checks that the input for project creation is valid,
        returns True if not valid, False if valid.
        Parameters:
            entry_method: str
        Returns:
            bool
        '''
        valid_project_creation = False
        if project_creation != "B":
            try:
                project_creation = project_creation.split(',')
                project_creation = [project_part.strip() for project_part in project_creation]
                # check if project creation information is of correct types 
                if isinstance(project_creation[0], str) and len(project_creation[0]) > 0 \
                and isinstance(project_creation[1], str) and len(project_creation[1]) > 0:
                    valid_project_creation = True
                # attempt to create a project, if fail then return unsucessful task creation
                if valid_project_creation:
                    user.create_project(project_creation[0], project_creation[1])
            except:
                pass
        return not valid_project_creation and (project_creation != "B")