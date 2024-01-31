from main import *
from Person import Person
import unittest
from construct_db import *
from unittest.mock import patch

class Current():
    def __init__(self) -> None:
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.user = None

class TestStringMethods(unittest.TestCase):

    cur = Current()

    @patch('main.InputHandler.Handler')
    def test_notifs_1(self, mock_handler):
        '''
        White box test case 1
        '''
        #setup 
        # create inviter
        username1 = "pineapple1"
        password = "fruitiness"
        inviter = Person(self.cur.session, username1, password, "signup")

        # create project to invite to
        project_id = inviter.create_project("Pineapple project", "pineapples work on this")

        # create 2nd user
        username2 = "pineapple2"
        self.cur.user = Person(self.cur.session, username2, password, "signup")

        # invite 2nd user
        inviter.invite_member(username2, project_id=project_id)

        mock_handler.return_value = "1"
        result = notifications(self.cur)
        
        assert result == "HOME"

    @patch('main.InputHandler.Handler')
    def test_notifs_2(self, mock_handler):
        '''
        White box test case 2
        '''
        # create inviter
        username1 = "orange1"
        password = "fruitiness"
        inviter = Person(self.cur.session, username1, password, "signup")

        # create project to invite to
        task_id = inviter.create_task("Orange task", "oranges work on this", 6)

        # create 2nd user
        username2 = "oranges2"
        self.cur.user = Person(self.cur.session, username2, password, "signup")

        # invite 2nd user
        inviter.invite_member(username2, task_id=task_id)

        mock_handler.return_value = "1"
        result = notifications(self.cur)
        
        assert result == "HOME"

    @patch('main.InputHandler.Handler')
    def test_notifs_3(self, mock_handler):
        '''
        White box test case 3
        '''
        #setup 
        # create inviter
        username1 = "grape1"
        password = "fruitiness"
        inviter = Person(self.cur.session, username1, password, "signup")

        # create project to invite to
        project_id = inviter.create_project("Grape project", "grapes work on this")

        # create 2nd user
        username2 = "grape2"
        self.cur.user = Person(self.cur.session, username2, password, "signup")

        # invite 2nd user
        inviter.invite_member(username2, project_id=project_id)

        mock_handler.return_value = "2"
        result = notifications(self.cur)
        
        assert result == "HOME"
    
if __name__ == '__main__':
    unittest.main()