from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, MetaData, func
)
from sqlalchemy.orm import declarative_base, relationship


metadata = MetaData(schema="financeferret")
Base = declarative_base(metadata=metadata)


class UserAccount(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    children = relationship("ChildProfile", back_populates="user")


class ChildProfile(Base):
    __tablename__ = "child_profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("financeferret.user_account.id"), nullable=False)
    child_name = Column(String(100), nullable=False)
    age = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("UserAccount", back_populates="children")
    #allocations = relationship("Allocation", back_populates="child")
    #goals = relationship("Goal", back_populates="child")

"""
class Allocation(Base):
    __tablename__ = "allocation"

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("financeferret.child_profile.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    spend = Column(Integer, nullable=False, default=0)
    save_amount = Column(Integer, nullable=False, default=0)
    share_amount = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, server_default=func.now())

    child = relationship("ChildProfile", back_populates="allocations")


class Goal(Base):
    __tablename__ = "goal"

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("financeferret.child_profile.id"), nullable=False)
    goal_name = Column(String(200), nullable=False)
    target_amount = Column(Integer, nullable=False)
    current_amount = Column(Integer, nullable=False, default=0)
    completed = Column(Boolean, nullable=False, default=False)

    child = relationship("ChildProfile", back_populates="goals")
"""