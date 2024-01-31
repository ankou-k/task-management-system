from Person import Person
from construct_db import *

Session = sessionmaker(bind=engine)
session = Session()
user = Person(session, "hello", "passee", "signup")
user.create_project(name="My new project", description="this project is cool")
user.view_projects()
user.change_project_description(1, "changed name")
user.view_projects()

user.create_task(name="My new task", description="task", priority=1)