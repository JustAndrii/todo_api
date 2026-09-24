from sqlalchemy import Column, Integer, String,DateTime,ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String,nullable=False,unique=True)
    hashed_password = Column(String,nullable=False)
    created = Column(DateTime, default=datetime.datetime.now)

    tasks = relationship("Task", back_populates="user")



class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    completed = Column(Boolean, default=False, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates='tasks')