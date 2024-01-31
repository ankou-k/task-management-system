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

class Current():
    def __init__(self):
        self.user = None
        Session = sessionmaker(bind=engine)
        self.session = Session()

def login(current: Current):
    """
    This function allows user to login.
    """
    print("/login\n")
    login_username = InputHandler.Handler(current.session,
        "Username inputted does not exist. Try again.\n",
        "Please input your username below.\n"
        "If you'd like to move to signup, input: SU\n"
        "Username: ",
        "login_username")
    
    # if the return of login_username is "SU" it means user chose to sign up
    # redirect to sign up
    if login_username == "SU":
        #signup()
        return "SU"
    else:
        # validate user password by calling input handler
        login_password = InputHandler.Handler(current.session,
            "Password is incorrect. Try again.\n",
            "Please input your password below.\n"
            "If you'd like to move to signup, input: SU\n"
            "Password: ",
            "login_password",
            login_username)
        # user chose to sign up, redirect to sign up
        if login_password == "SU":
            #signup()
            return "SU"
        
        #sign up successfull, redirect to home
        else:
            current.user = Person(current.session, login_username, login_password, "login")
            #home(user)
            return "HOME"


def signup(current:Current):
    '''
    This function allows user to sign up.
    '''
    print("/signup\n")
    signup_username = InputHandler.Handler(current.session, 
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
        #login()
        return "LI"
    else:
        # validate password
        signup_password = InputHandler.Handler(current.session,
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
            #login()
            return "LI"
        # user creation successful, redirect to home
        else:
            user = Person(current.session, signup_username, signup_password, "signup")
            current.user = user
            #home(new_user)
            return "HOME"
        

def home(current: Current):
    '''
    This function displays the home menu, where the user can select what they want to do
    Parameters:
        user: Person object
    '''
    # display username
    print("/home\n"
          f"User: {current.user.username}\n")
    
    # handler to select valid option of what user wants to do
    navigation = InputHandler.Handler(current.session,
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
            #tasks(user)
            return "TASK"
        case "2":
            #projects(user)
            return "PROJ"
        case "3":
            #notifications(user)
            return "NOTIF"
        case "4":
            #main()
            return "LO"


def notifications(current: Current):
    '''
    This function allows user to view notifications for project and task invitations
    and accept or deny them.
    Parameters:
        user: Person object
    '''
    user = current.user
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
        project_task_acceptance = InputHandler.Handler(current.session,
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
                print("test 1")
            else:
                user.add_task_member(current_notification['item_id'])
                print("test 2")
        else:
            user.change_invitation_status(current_notification['id'], "declined")
            print("test 3")

    # print out message that all notifications are read
    print(user.get_notifications())
    # go to home screen
    return "HOME"

def tasks(current: Current):
    '''
    This function displays the task navigation menu, where the user can select to
    view tasks sorted by deadline or by priority, edit tasks, and create tasks.
    Parameters:
        user: Person object
    '''
    user = current.user
    # handler to select valid option of what user wants to do
    task_navigation = InputHandler.Handler(current.session, 
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
            #tasks(user)
            return "TASK"
        # view tasks by deadline
        case "2":
            user.view_tasks()
            #tasks(user)
            return "TASK"
        # edit tasks
        case "3":
            if user.tasks_length != 0:
                user.view_tasks()

                # user selects which task to edit
                task_edit_navigation = InputHandler.Handler(current.session,
                    "Please input a valid input of a number below.\n",
                    "Which task would you like to edit:\n"
                    "Input B to go back.\n"
                    "Input: ",
                    "task_edit_navigation"
                )

                # go back to task page
                match task_edit_navigation:
                    case "B":
                        #tasks(user)
                        return "TASK"
                    case _:
                        #tasks(user)
                        return "TASK"
            else:
                user.view_tasks()
                #tasks(user)
                return "TASK"
        case "4":
            # allow user to create a task
            task_creation = InputHandler.Handler(current.session,
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
                    #tasks(user)
                    return "TASK"
                case _:
                    print("Task Created successfully\n")
                    #tasks(user)
                    return "TASK"
        case "5":
            #home(user)
            return "HOME"
        

def projects(current: Current):
    '''
    This function displays the project navigation menu, where the user can select to
    view projects, edit projects, and create projects.
    Parameters:
        user: Person object
    '''
    user = current.user
    # handler to select valid option of what user wants to do
    project_navigation = InputHandler.Handler(current.session,
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
            #projects(user)
            return "PROJ"
        # edit projects
        case "2":
            if user.admin_projects_length() != 0:
                user.view_projects()

                # user chooses which project to edit
                project_edit_navigation = InputHandler.Handler(current.session,
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
                        #projects(user)
                        return "PROJ"
                    case _:
                        # user chooses how to edit the project
                        project_edit_navigation2 = InputHandler.Handler(current.session,
                            "Please input a valid input of 1, 2, 3, 4, 5, or 6 below.\n",
                            "What would you like to edit within the project:\n"
                            "1: Edit Project Name\n"
                            "2: Edit Project Description\n"
                            "3: Add Member\n"
                            "4: Remove Member\n"
                            "5: Delete Project\n"
                            "6: Back\n"
                            "Input: ",
                            "project_edit_navigation2"
                        )
                        match project_edit_navigation2:
                            case "1":
                                # user chooses a new name for the project
                                project_name_edit = InputHandler.Handler(current.session,
                                    "Please input a valid input of a name below.\n",
                                    "What would you like the new name of the project to be:\n"
                                    "Input B to go back.\n"
                                    "Input: ",
                                    "project_name_edit"
                                )
                                # based on user input, either go back or update the name and go back
                                match project_name_edit:
                                    case "B":
                                        #projects(user)
                                        return "PROJ"
                                    case _:
                                        user.change_project_name(int(project_edit_navigation), project_name_edit)
                                        print("Project name successfully changed\n")
                                        #projects(user)
                                        return "PROJ"
                            case "2":
                                # user chooses a new description for the project
                                project_description_edit = InputHandler.Handler(current.session,
                                    "Please input a valid input of a description below.\n",
                                    "What would you like the new description of the project to be:\n"
                                    "Input B to go back.\n"
                                    "Input: ",
                                    "project_description_edit"
                                )
                                # based on user input, either go back or update the description and go back
                                match project_description_edit:
                                    case "B":
                                        #projects(user)
                                        return "PROJ"
                                    case _:
                                        user.change_project_description(int(project_edit_navigation), project_description_edit)
                                        print("Project description successfully changed\n")
                                        #projects(user)
                                        return "PROJ"
                            case "3":
                                # user chooses a user to invite to the project
                                project_invite = InputHandler.Handler(current.session,
                                    "Please input a valid input of a name below.\n",
                                    "What user would you like to invite to the project:\n"
                                    "Input B to go back.\n"
                                    "Input: ",
                                    "project_invite"
                                )
                                # based on user input, either go back or invite the user and go back
                                match project_invite:
                                    case "B":
                                        #projects(user)
                                        return "PROJ"
                                    case _:
                                        user.invite_member(project_invite, int(project_edit_navigation))
                                        #projects(user)
                                        return "PROJ"
                            case "4":
                                # user chooses a user to remove from the project
                                project_remove = InputHandler.Handler(current.session,
                                    "Please input a valid input of a name below.\n",
                                    "What user would you like to remove from the project:\n"
                                    "Input B to go back.\n"
                                    "Input: ",
                                    "project_remove"
                                )
                                # based on user input, either go back or remove the user and go back
                                match project_remove:
                                    case "B":
                                        #projects(user)
                                        return "PROJ"
                                    case _:
                                        user.remove_project_member(project_remove, int(project_edit_navigation))
                                        #projects(user)
                                        return "PROJ"
                            case "5":
                                # user chooses to delete the project
                                project_delete = InputHandler.Handler(current.session,
                                    "Please input the project name below.\n",
                                    "Input the project name to delete the project:\n"
                                    "Input B to go back.\n"
                                    "Input: ",
                                    "project_delete",
                                    project_edit_navigation
                                )
                                # based on user input, either go back or delete the project
                                match project_delete:
                                    case "B":
                                        #projects(user)
                                        return "PROJ"
                                    case _:
                                        user.delete_project(int(project_edit_navigation))
                                        #projects(user)
                                        return "PROJ"
                            case "6":
                                # go back
                                #projects(user)
                                return "PROJ"
            else:
                # if user is not admin to any project, they cannot edit any, sends user back
                print("You are admin in no projects.\n")
                #projects(user)
                return "PROJ"
        # create project
        case "3":
            project_creation = InputHandler.Handler(current.session,
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
                    #projects(user)
                    return "PROJ"
                case _:
                    print("Project Created successfully\n")
                    #projects(user)
                    return "PROJ"
        # go home
        case "4":
            #home(user)
            return "HOME"

def welcome(current: Current):
    current.user = None

    print("/index\n")
    print("Welcome to Group 17's Task Management system!\n"
          "To navigate, input the number cooresponding to\n"
          "a possible output.\n")
    
    # call input handler to obtain valid input
    entry_method = InputHandler.Handler(current.session,
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
            return "LI"
        # signup
        case "2":
            return "SU"
        # user chose to exit
        case "3":
            return "EXIT"


def navigation(current): 
    exit = False 
    result = welcome(current)

    # continue navigating
    while not exit:
        if result == "EXIT":
            exit = True

        elif result == "SU":
            result = signup(current)

        elif result == "LI":
            result = login(current)

        elif result == "LO":
            result = welcome(current)

        elif result == "HOME":
            result = home(current)

        elif result == "TASK":
            result = tasks(current)

        elif result == "PROJ":
            result = projects(current)

        elif result == "NOTIF":
            result = notifications(current)

        else:
            print("error: invalid result in navigation()")
            exit = True

    if result == "EXIT":
        print("Have a nice day!")
    return result

    #projects, tasks, notifications, home, login, signup

def main():
    '''
    This function is the starting point of the program. It allows the user to 
    log into their account or sign up as a new user.
    '''
    current = Current()
    navigation(current)
    current.session.close()

if __name__ == "__main__":
    main()