from Users import User, AllUsers
from Projects import Project
from Tasks import Task
from InputHandling import InputHandler

from Person import Person
from construct_db import *
'''
Task Management System
-----------------------
Overall program intention:
    This program is a task management system. It allows users to create, manage, and track tasks and projects. 
Input and output info:
    This program takes input through the cli and outputs info into the cli.
How the program is intended to be run: 
    Run this python file (main.py), and interact with the program using the cli
'''

def login():
    """
    This function allows user to login.
    """
    print("/login\n")
    login_username = InputHandler.Handler(
        "Username inputted does not exist. Try again.\n",
        "Please input your username below.\n"
        "If you'd like to move to signup, input: SU\n"
        "Username: ",
        "login_username")
    
    # if the return of login_username is "SU" it means user chose to sign up
    # redirect to sign up
    if login_username == "SU":
        signup()
    else:
        # validate user password by calling input handler
        login_password = InputHandler.Handler(
            "Password is incorrect. Try again.\n",
            "Please input your password below.\n"
            "If you'd like to move to signup, input: SU\n"
            "Password: ",
            "login_password",
            login_username)
        # user chose to sign up, redirect to sign up
        if login_password == "SU":
            signup()
        #sign up successfull, redirect to home
        else:
            Session = sessionmaker(bind=engine)
            session = Session()
            user = Person(session, login_username, login_password, "login")
            session.close()
            home(user)


def signup():
    '''
    This function allows user to sign up.
    '''
    print("/signup\n")
    signup_username = InputHandler.Handler(
        "Your chosen username was invalid or taken, "
        "make sure it confirms to the requirements below.\n",
        "Please input your new username below.\n"
        "Your username must be between 3-20 characters,\n"
        "and must not have any special characters.\n"
        "If you'd like to move to login, input: LI\n"
        "Username: ",
        "signup_username")
    
    # user chose to login, redirect to login
    if signup_username == "LI":
        login()
    else:
        # validate password
        signup_password = InputHandler.Handler(
            "Your password was invalid, "
            "make sure it confirms to the requirements below.\n",
            "Please input your new password below:\n"
            "Your password must be between 8-30 characters.\n"
            "You may use letters numbers, and these\n"
            "special characters: -_.!@#$%^&*()\n"
            "If you'd like to move to login, input: LI\n"
            "Password: ",
            "signup_password")
        
        # user chose to login, redirect to login
        if signup_password == "LI":
            login()
        # user creation successful, redirect to home
        else:
            Session = sessionmaker(bind=engine)
            session = Session()
            new_user = Person(session, signup_username, signup_password, "signup")
            session.close()
            home(new_user)
        

def home(user):
    '''
    This function displays the home menu, where the user can select what they want to do
    Parameters:
        user: User object
    '''

    # display username
    print("/home\n"
          f"User: {user.username}\n")
    
    # handler to select valid option of what user wants to do
    navigation = InputHandler.Handler(
        "Please input a valid input of 1, 2, 3, or 4 below.\n",
        "Where would you like to navigate to:\n"
        "1: Tasks\n"
        "2: Projects\n"
        "3: Notifications\n"
        "4: Logout\n"
        "Input: ",
        "home_navigation"
    )
    
    # based on user input, call relevant function 
    match navigation:
        case "1":
            tasks(user)
        case "2":
            projects(user)
        case "3":
            notifications(user)
        case "4":
            main()


def notifications(user):
    '''
    This function allows user to view notifications for project and task invitations
    and accept or deny them.
    Parameters:
        user: Person object
    '''
    # get amount of notifications
    num_notifs = user.notifications_length()
    notifs = user.get_notifications()

    # look through notifications until no notifications left
    for i in range(num_notifs):
        # retreive notification
        current_notification = notifs[i]

        # display notification
        print(current_notification['message'])

        # ask user if they accept or deny invitation, handler for valid input
        project_task_acceptance = InputHandler.Handler(
        "Please input a valid input of 1 or 2 below.\n",
        "1: Accept\n"
        "2: Decline\n",
        "project_task_acceptance"
        )

        # if user accepts project invitation, add user to project
        if project_task_acceptance == "1":
            user.change_invitation_status(current_notification['id'], "accepted")
            if current_notification['project']:
                user.add_project_member(current_notification['item_id'])
            else:
                user.add_task_member(current_notification['item_id'])
        else:
            user.change_invitation_status(current_notification['id'], "declined")
    # print out message that all notifications are read
    print(user.get_notifications())
    # go to home screen
    home(user)


def tasks(user):
    '''
    This function displays the task navigation menu, where the user can select to
    view tasks sorted by deadline or by priority, edit tasks, and create tasks.
    Parameters:
        user: User object
    '''

    # handler to select valid option of what user wants to do
    task_navigation = InputHandler.Handler(
        "Please input a valid input of 1, 2, 3, 4, or 5 below.\n",
        "Where within the tasks would you like to navigate:\n"
        "1: View Tasks (storted by priority)\n"
        "2: View Tasks (sorted by deadline)\n"
        "3: Edit Task\n"
        "4: Create Task\n"
        "5: Back to Home\n"
        "Input: ",
        "task_navigation"
    )

    # basec on user choice, do action
    match task_navigation:
        # view tasks by priority
        case "1":
            user.view_tasks()
            tasks(user)
        # view tasks by deadline
        case "2":
            user.view_tasks()
            tasks(user)
        # edit tasks
        case "3":
            if user.tasks_length != 0:
                user.view_tasks()

                # user selects which task to edit
                task_edit_navigation = InputHandler.Handler(
                    "Please input a valid input of a number below.\n",
                    "Which task would you like to edit:\n"
                    "Input B to go back.\n"
                    "Input: ",
                    "task_edit_navigation"
                )

                # go back to task page
                match task_edit_navigation:
                    case "B":
                        tasks(user)
                    case _:
                        tasks(user)
            else:
                user.view_tasks()
                tasks(user)
        case "4":
            # allow user to create a task
            task_creation = InputHandler.Handler(
                "Please input a valid input as shown below.\n",
                "You must enter:\n"
                "Task Name, Task Description, Task Project ID (0 if none),\n"
                "Task Priority (1-7), and Task Deadline.\n"
                "All must be sepearted by a comma.\n"
                "Date must be in the form YYYY-MM-D\n"
                "Example: Task1, A Task, 0, 1, 2023-12-12\n"
                "Input B to go back.\n"
                "Input: ",
                "task_creation",
                user
            )

            # based on user input, either task created successfully or no task created, go back to tasks page
            match task_creation:
                case "B":
                    tasks(user)
                case _:
                    print("Task Created successfully\n")
                    tasks(user)
        case "5":
            home(user)
        

def projects(user: User):
    '''
    This function displays the project navigation menu, where the user can select to
    view projects, edit projects, and create projects.
    Parameters:
        user: User object
    '''

    # handler to select valid option of what user wants to do
    project_navigation = InputHandler.Handler(
        "Please input a valid input of 1, 2, 3, or 4 below.\n",
        "Where within the tasks would you like to navigate:\n"
        "1: View Projects\n"
        "2: Edit Project\n"
        "3: Create Project\n"
        "4: Back to Home\n"
        "Input: ",
        "project_navigation"
    )

    # basec on user choice, do action
    match project_navigation:
        # view projects
        case "1":
            user.view_projects()
            projects(user)
        # edit projects
        case "2":
            if user.admin_projects_length() != 0:
                user.view_projects()

                # user chooses which project to edit
                project_edit_navigation = InputHandler.Handler(
                    "Please input a valid input of a number below.\n",
                    "Which project would you like to edit:\n"
                    "Input B to go back.\n"
                    "Input: ",
                    "project_edit_navigation",
                    user
                )

                # go back to tasks page
                match project_edit_navigation:
                    case "B":
                        projects(user)
                    case _:
                        project_edit_navigation2 = InputHandler.Handler(
                            "Please input a valid input of 1, 2, 3, 4, or 5 below.\n",
                            "What would you like to edit within the project:\n"
                            "1: Edit Project Name\n"
                            "2: Edit Project Description\n"
                            "3: Add Member\n"
                            "4: Remove Member\n"
                            "5: Delete Project\n"
                            "Input: ",
                            "project_edit_navigation2"
                        )
                        match project_edit_navigation2:
                            case "1":
                                project_name_edit = InputHandler.Handler(
                                    "Please input a valid input of a name below.\n",
                                    "What would you like the new name of the project to be:\n"
                                    "Input B to go back.\n"
                                    "Input: ",
                                    "project_name_edit"
                                )
                                match project_name_edit:
                                    case "B":
                                        projects(user)
                                    case _:
                                        user.change_project_name(int(project_edit_navigation), project_name_edit)
                                        print("Project name successfully changed\n")
                                        projects(user)
                            case "2":
                                project_description_edit = InputHandler.Handler(
                                    "Please input a valid input of a description below.\n",
                                    "What would you like the new description of the project to be:\n"
                                    "Input B to go back.\n"
                                    "Input: ",
                                    "project_description_edit"
                                )
                                match project_description_edit:
                                    case "B":
                                        projects(user)
                                    case _:
                                        user.change_project_description(int(project_edit_navigation), project_description_edit)
                                        print("Project description successfully changed\n")
                                        projects(user)
                            case "3":
                                pass
                            case "4":
                                pass
                            case "5":
                                pass
            else:
                print("You are admin in no projects.\n")
                projects(user)
        # create project
        case "3":
            project_creation = InputHandler.Handler(
                "Please input a valid input as shown below.\n",
                "You must enter:\n"
                "Project Name and Project Description.\n"
                "They must be sepearted by a comma.\n"
                "Example: Project1, A Project\n"
                "Input B to go back.\n"
                "Input: ",
                "project_creation",
                user
            )
            # based on user input, either project created successfully or no task created, go back to tasks page
            match project_creation:
                case "B":
                    projects(user)
                case _:
                    print("Project Created successfully\n")
                    projects(user)
        # go home
        case "4":
            home(user)
            

def main():
    '''
    This function is the starting point of the program. It allows the user to 
    log into their account or sign up as a new user.
    '''

    print("/index\n")
    print("Welcome to Group 17's Task Management system!\n"
          "To navigate, input the number cooresponding to\n"
          "a possible output.\n")
    
    # call input handler to obtain valid input
    entry_method = InputHandler.Handler(
        "Please input a valid input of 1 or 2 below.\n",
        "Would you like to Login or Signup:\n"
        "1: Login\n"
        "2: Signup\n"
        "3: Exit\n"
        "Input: ",
        "entry_method")
    
    # based on user input, call relevant function 
    match entry_method:
        # login
        case "1":
            login()
        # signup
        case "2":
            signup()
        # user chose to exit
        case "3":
            print("Have a nice day!")

if __name__ == "__main__":
    main()