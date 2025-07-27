from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    native_language = Column(String)

    progress = relationship("UserProgress", back_populates="owner")


class UserProgress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_language = Column(String, index=True)
    comprehension_level = Column(Integer, default=1)
    vocabulary_level = Column(Integer, default=1)
    grammar_level = Column(Integer, default=1)
    overall_progress = Column(Float, default=0.0)

    owner = relationship("User", back_populates="progress")


class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class LessonSubject(Base):
    __tablename__ = "lesson_subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
