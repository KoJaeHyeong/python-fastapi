import datetime

from schema.request import CreateTodoRequest
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(255), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return f"this is repr of Todo(id={self.id}, contents={self.contents}, is_done={self.is_done})"

    @classmethod  # orm객체로 변경
    def create(cls, request: CreateTodoRequest) -> Todo:
        return cls(
            contents=request.contents,
            is_done=request.is_done,
        )

    def done(self) -> Todo:
        self.is_done = True
        return self

    def undone(self) -> Todo:
        self.is_done = False
        return self


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    email = Column(String(50), nullable=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    todos = relationship("Todo", lazy="joined")

    @classmethod
    def create(cls, username: str, hashed_password: str) -> User:
        return cls(username=username, password=hashed_password)
