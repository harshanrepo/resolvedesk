from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class MasterTable(Base):
    __tablename__ = "master_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tag_code = Column(String, unique=True, nullable=False)
    values = relationship("MasterListTable",back_populates="master",cascade="all, delete")


class MasterListTable(Base):
    __tablename__ = "master_list_table"

    id = Column(Integer, primary_key=True, index=True)
    tag_code = Column(String,ForeignKey("master_table.tag_code"),nullable=False)
    value = Column(String, nullable=False)
    master = relationship("MasterTable",back_populates="values")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(Integer,ForeignKey("master_list_table.id"),nullable=False)
    role = relationship("MasterListTable")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority_id = Column(Integer,ForeignKey("master_list_table.id"),nullable=False)
    status_id = Column(Integer,ForeignKey("master_list_table.id"),nullable=False)
    created_by = Column(Integer,ForeignKey("users.id"),nullable=False)
    assigned_to = Column(Integer,ForeignKey("users.id"),nullable=True)
    created_at = Column(DateTime,default=datetime.utcno)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    creator = relationship("User",foreign_keys=[created_by])
    assignee = relationship("User",foreign_keys=[assigned_to])
    priority = relationship("MasterListTable",foreign_keys=[priority_id])
    status = relationship("MasterListTable",foreign_keys=[status_id])
    comments = relationship("Comment",back_populates="ticket",cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer,ForeignKey("tickets.id"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
    ticket = relationship("Ticket",back_populates="comments")
    user = relationship("User")