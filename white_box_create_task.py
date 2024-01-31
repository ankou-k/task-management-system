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
    def test_create_task_1(self, mock_handler):
        '''
        White box test case 1
        '''
        #setup 
        # create user
        username1 = "Andrew"
        password = "12345678"
        self.cur.user = Person(self.cur.session, username1, password, "signup")
        
        # Create a task
        mock_handler.side_effect = ["4", "Task1, A Task, 0, 0, 2023-12-12"]
        result = tasks(self.cur)
        
        assert result == "TASK"

    @patch('main.InputHandler.Handler')
    def test_create_task_2(self, mock_handler):
        '''
        White box test case 2
        '''
        #setup 
        # create user
        username1 = "Nick"
        password = "87654321"
        user = Person(self.cur.session, username1, password, "signup")
        
        # Cancel create task
        mock_handler.side_effect = ["4", "B"]
        result = tasks(self.cur)
        
        assert result == "TASK"
    
if __name__ == '__main__':
    unittest.main()