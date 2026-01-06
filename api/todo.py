from typing import List

from database.orm import Todo, User
from database.repository import TodoRepository, UserRepository
from fastapi import APIRouter, Body, Depends, HTTPException
from schema.request import CreateTodoRequest
from schema.response import TodoListSchema, TodoSchema
from security import get_access_token
from service.user import UserService

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", status_code=200)
def get_todos(
    access_token: str = Depends(get_access_token),
    order: str | None = None, todo_repo: TodoRepository = Depends(), user_service: UserService = Depends(), user_repo: UserRepository = Depends()
) -> TodoListSchema:

    username: str = user_service.verify_jwt(access_token=access_token)

    user: User | None = user_repo.get_user_by_username(username=username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    todos: List[Todo] = user.todos

    if order and order.upper() == "DESC":
        return TodoListSchema(todos=[TodoSchema.from_orm(todo) for todo in todos[::-1]])

    return TodoListSchema(todos=[TodoSchema.from_orm(todo) for todo in todos])


@router.get("/{todo_id}", status_code=200)
def get_todo(todo_id: int, todo_repo: TodoRepository = Depends()) -> TodoSchema:
    todo: Todo | None = todo_repo.get_todo_by_id(todo_id)

    if todo:
        return TodoSchema.from_orm(todo)

    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("", status_code=201)
def create_todo(
    req: CreateTodoRequest, todo_repo: TodoRepository = Depends()
) -> TodoSchema:
    todo: Todo = Todo.create(request=req)
    new_todo: Todo = todo_repo.create_new_todo(todo=todo)

    return TodoSchema.from_orm(new_todo)


@router.patch("/{todo_id}", status_code=200)
def update_todo(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    todo_repo: TodoRepository = Depends(),
) -> TodoSchema:
    todo: Todo | None = todo_repo.get_todo_by_id(todo_id)

    if todo:
        todo.done() if is_done else todo.undone()

        todo = todo_repo.update_todo_done(todo=todo)

        return TodoSchema.from_orm(todo)

    raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, todo_repo: TodoRepository = Depends()) -> None:
    todo: Todo | None = todo_repo.get_todo_by_id(todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_repo.delete_todo_by_id(todo_id=todo_id)
