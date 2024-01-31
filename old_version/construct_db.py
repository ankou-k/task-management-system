import datetime
from sqlalchemy import create_engine,  Column, Integer, String, DateTime, ForeignKey, select
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    admin_id = Column(Integer, ForeignKey('users.id'))

    admin = relationship('User', backref='projects')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    project_id = Column(Integer, ForeignKey('projects.id'))
    priority = Column(Integer)
    deadline = Column(DateTime)
    admin_id = Column(Integer, ForeignKey('users.id'))

    admin = relationship('User', backref='tasks')
    project = relationship('Project', backref='tasks')

class ProjectAssignment(Base):
    __tablename__ = 'project_assignments'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    project = relationship('Project', backref='assignments')
    user = relationship('User', backref='project_assignments')

class TaskAssignment(Base):
    __tablename__ = 'task_assignments'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    task = relationship('Task', backref='assignments')
    user = relationship('User', backref='task_assignments')

class Message(Base):
    '''
    id (primary key)
    sender_id (foreign key to the users table, referencing the user who sent the invitation)
    recipient_id (foreign key to the users table, referencing the user who received the invitation)
    project_id (foreign key to the projects table, referencing the project related to the invitation)
    task_id (foreign key to the tasks table, referencing the task related to the invitation)
    message (a text column storing the actual invitation message)
    status (a string column storing the status of the invitation, e.g. "pending", "accepted", "declined")
    '''
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    message = Column(String, nullable=False)
    status = Column(String, nullable=False)

    sender = relationship('User', foreign_keys=[sender_id])
    recipient = relationship('User', foreign_keys=[recipient_id])
    project = relationship('Project', foreign_keys=[project_id])
    task = relationship('Task', foreign_keys=[task_id])
'''
Create an engine and a connection to SQLite database
sqlite Windows:
path = "sqlite:///C:\\path\\to\\foo.db"
'''
path = 'sqlite:///C:\\Users\\Alex\\CodingRoot\\cisc327_quality_assurance\\Labs\\management_system.db'
engine = create_engine(path)

# remove all previous tables and data
Base.metadata.drop_all(engine)

# create tables and data
Base.metadata.create_all(engine)

# Use the database by creating a session and interacting with the tables using the SQLAlchemy models
#Session = sessionmaker(bind=engine)
#session = Session()

'''
user = User(username='john', password='hello_world')
session.add(user)
session.commit()

project = Project(name='My First Project', admin=user)
session.add(project)
session.commit()

#session.close()
'''

'''This will create a new user with the username john and a new project with the name My First Project assigned to that user.

When you use backref='assignments', you're telling SQLAlchemy to create a relationship between the Task table and the TaskAssignment table, where each task has multiple assignments (i.e., many-to-many relationship). The backref argument specifies the name of the relationship on the Task side. In this case, it's assignments. This means that you can access the assignments for a task using the task.assignments attribute.

On the other hand, when you use foreign_keys=[task_id], you're telling SQLAlchemy to create a relationship between the Message table and the Task table, where each message is related to a single task (i.e., one-to-many relationship). The foreign_keys argument specifies the column(s) on the Task table that should be used to establish the relationship. In this case, it's the task_id column. This means that you can access the task related to a message using the message.task attribute.

In summary:

    backref='assignments' creates a many-to-many relationship between Task and TaskAssignment, allowing you to access assignments for a task.
    foreign_keys=[task_id] creates a one-to-many relationship between Message and Task, allowing you to access the task related to a message.

In the context of the Message class, we used foreign_keys=[task_id] because each message is related to a single task, and we want to access the task object using the message.task attribute. If we had used backref='assignments', it would imply that each message has multiple tasks, which is not the case in this scenario. 
'''
