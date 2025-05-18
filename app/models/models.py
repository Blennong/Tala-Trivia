# app/models/models.py
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    trivias = relationship("Trivia", back_populates="creator")
    attempts = relationship("Attempt", back_populates="user")
    
    assigned_trivias_association = relationship("TriviaUser", back_populates="user", cascade="all, delete")
    assigned_trivias = relationship("Trivia", secondary="trivia_users", back_populates="assigned_users")

class Question(Base):
    __tablename__ = "questions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String, nullable=False)
    category = Column(String)
    difficulty = Column(String)
    correct_answer = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    answers = relationship("Answer", back_populates="question")
    trivia_questions = relationship("TriviaQuestion", back_populates="question", cascade="all, delete")

class Trivia(Base):
    __tablename__ = "trivias"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", back_populates="trivias")
    attempts = relationship("Attempt", back_populates="trivia")
    trivia_questions = relationship("TriviaQuestion", back_populates="trivia", cascade="all, delete")

    assigned_users_association = relationship("TriviaUser", back_populates="trivia", cascade="all, delete")
    assigned_users = relationship("User", secondary="trivia_users", back_populates="assigned_trivias")

class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    trivia_id = Column(UUID(as_uuid=True), ForeignKey("trivias.id"), nullable=False)
    score = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="attempts")
    trivia = relationship("Trivia", back_populates="attempts")
    answers = relationship("Answer", back_populates="attempt")

class Answer(Base):
    __tablename__ = "answers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attempt_id = Column(UUID(as_uuid=True), ForeignKey("attempts.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    selected = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    attempt = relationship("Attempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")

class TriviaQuestion(Base):
    __tablename__ = "trivia_questions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trivia_id = Column(UUID(as_uuid=True), ForeignKey("trivias.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)

    trivia = relationship("Trivia", back_populates="trivia_questions")
    question = relationship("Question", back_populates="trivia_questions")

class TriviaUser(Base):
    __tablename__ = "trivia_users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trivia_id = Column(UUID(as_uuid=True), ForeignKey("trivias.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)

    trivia = relationship("Trivia", backref="trivia_users")
    user = relationship("User", backref="trivia_users")