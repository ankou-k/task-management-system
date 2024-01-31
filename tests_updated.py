from management_utils import DB_Utils
import unittest
from construct_db import *
from InputHandling import InputHandler

class MySession():
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session(expire_on_commit=True)

class TestStringMethods(unittest.TestCase):

    cur = MySession()
    
    
    # Testing signup functionality:

    def test_create_user(self):
        '''
        Test that a user can be created
        '''
        username = "username"
        password = "password"
        result = DB_Utils.create_user(self.cur.session, username, password)
        assert result > 0
        
    def test_create_user_fail(self):
        '''
        Test that wrong username or password is caught
        '''
        username = ""
        #password = "password"
        result = InputHandler.signup_username_condition(self.cur.session, username)
        #result = DB_Utils.create_user(self.cur.session, username, password)
        assert result == True # True = rerun while loop for another username as current is invalid
    
    
    # Testing project functionality:
    
    def test_create_project_success(self):
        '''
        Test that user can create project
        '''
        user_id = 1
        name = "project"
        description = "description"

        result = DB_Utils.create_project(self.cur.session, user_id, name, description)
        result_output_text = result[0]
        assert result_output_text == "success\n" 

    def test_create_project_fail(self):
        '''
        Test that user cannot create project with empty name
        '''
        user_id = 1
        name = ""
        description = "description"

        result = DB_Utils.create_project(self.cur.session, user_id, name, description)
        result_output_text = result[0]
        assert result_output_text == "failure: project needs name\n"

    def test_change_project_name_success(self):
        '''
        Test that user can change project name.
        NOTE: there may already be project with id 1, in which case that project's name will be changed.
        This still sufficiently tests functionality.
        '''
        # create project
        user_id = 1
        name = "project"
        description = "description"
        DB_Utils.create_project(self.cur.session, user_id, name, description)

        project_id = 1
        name = "new name"
        result = DB_Utils.change_project_name(self.cur.session, project_id, name)
        assert result == "success\n"

    def test_change_project_name_fail_1(self):
        '''
        Test that user cannot change project name to empty name.
        NOTE: there may already be project with id 1, in which case that project's name will be changed.
        This still sufficiently tests functionality.
        '''
        # create project
        user_id = 1
        name = "project"
        description = "description"
        DB_Utils.create_project(self.cur.session, user_id, name, description)

        project_id = 1
        name = ""

        result = DB_Utils.change_project_name(self.cur.session, project_id, name)
        assert result == "failure: project needs name\n"

    def test_change_project_name_fail_2(self):
        '''
        Test that user cannot change project name that does not exist
        '''
        project_id = 100
        name = "name"

        result = DB_Utils.change_project_name(self.cur.session, project_id, name)
        assert result == "This project id does not exist\n"

    def test_add_project_member(self):
        '''
        Test that can add project member. 
        NOTE: there may already be user with id 1 and 2, in which case project will be added to those users.
        This still sufficiently tests functionality.
        '''
        # create user
        username = "unicorn"
        password = "password"

        # create user
        DB_Utils.create_user(self.cur.session, username, password)

        # create project
        user_id = 1
        name = "project"
        description = "description"
        DB_Utils.create_project(self.cur.session, user_id, name, description)

        # create second user
        DB_Utils.create_user(self.cur.session, username+"2", password)

        # add member to project
        project_id = 1
        user_id = 2

        result = DB_Utils.add_project_member(self.cur.session, user_id, project_id)
        assert result == "Added user successfully\n"

    def test_get_projects(self):
        '''
        Test that user can get all projects related to them - both admin and non-admin. Should return 2 or more projects
        '''
        # create user
        username = "unicorn"
        password = "password"
        DB_Utils.create_user(self.cur.session, username, password)

        # create project
        user_id = 1
        name = "project"
        description = "description"
        DB_Utils.create_project(self.cur.session, user_id, name, description)

        # create second user
        DB_Utils.create_user(self.cur.session, username+"2", password)

        # add user 2 to project 1
        project_id = 1
        user_id = 2
        DB_Utils.add_project_member(self.cur.session, user_id, project_id)

        # create another project with user 2 as admin
        DB_Utils.create_project(self.cur.session, user_id, name, description)

        result = DB_Utils.get_projects(self.cur.session, user_id)
        assert len(result) > 1

    def test_get_projects_admin(self):
        '''
        Test that user can get all projects they created.
        '''
        user_id = 100
        result = DB_Utils.get_projects_admin(self.cur.session, user_id)
        assert result == []

    def test_change_project_name_success(self):
        '''
        Test that user can change project name.
        NOTE: there may already be project with id 1, in which case that project's name will be changed.
        This still sufficiently tests functionality.
        '''
        # create project
        user_id = 1
        name = "project"
        description = "description"
        DB_Utils.create_project(self.cur.session, user_id, name, description)

        project_id = 1
        new_description = "new description"
        result = DB_Utils.change_project_description(self.cur.session, project_id, new_description)
        assert result == "success\n"


    
if __name__ == '__main__':
    unittest.main()
