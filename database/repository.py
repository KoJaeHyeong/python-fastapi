from typing import List

from database.connection import get_db
from database.orm import Todo, User
from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session


class TodoRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_todos_list(self) -> List[Todo]:
        return list(self.db.scalars(select(Todo)))

    def get_todo_by_id(self, todo_id: int) -> Todo | None:
        return self.db.scalar(select(Todo).where(Todo.id == todo_id))

    def create_new_todo(self, todo: Todo):
        self.db.add(instance=todo)  # 메모리에 임시 올려져 있는 상태
        print(f"todo1: {todo}")
        self.db.commit()  # 이 시점에서 DB 저장
        print(f"todo2: {todo}")
        self.db.refresh(instance=todo)

        return todo

    def update_todo_done(self, todo: Todo) -> Todo:
        self.db.add(instance=todo)  # 메모리에 임시 올려져 있는 상태
        self.db.commit()  # 이 시점에서 DB 저장
        self.db.refresh(instance=todo)

        return todo

    def delete_todo_by_id(self, todo_id: int) -> None:
        self.db.execute(delete(Todo).where(Todo.id == todo_id))
        self.db.commit()

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get_user_by_username(self, username: str)-> User | None:
        return self.db.scalar(select(User).where(User.username == username))

    def create_user(self, user: User) -> User:
        self.db.add(instance=user)
        self.db.commit()
        self.db.refresh(instance=user)

        return user

    def create_user_email(self, email: str, id: int) -> None:
        self.db.execute(update(User).where(User.id == id).values(email=email))
        self.db.commit()
