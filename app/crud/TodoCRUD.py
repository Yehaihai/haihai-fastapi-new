from typing import Optional, List
from sqlmodel import Session, select
from app.models.table import Todo


class TodoCRUD:
    def __init__(self, session: Session):
        self.session = session

    def get_todo(self, todo_id: str) -> Todo | None:
        """根据ID获取todo"""
        return self.session.get(Todo, todo_id)

    def get_all_todos(self, user_id: str) -> List[Todo]:
        """获取用户的所有未删除todo"""
        return self.session.exec(
            select(Todo).where(
                Todo.user_id == user_id,
                Todo.is_deleted == False
            )
        ).all()

    def get_completed_todos(self, user_id: str) -> List[Todo]:
        """获取用户的所有已完成且未删除todo"""
        return self.session.exec(
            select(Todo).where(
                Todo.user_id == user_id,
                Todo.completed == True,
                Todo.is_deleted == False
            )
        ).all()

    def get_uncompleted_todos(self, user_id: str) -> List[Todo]:
        """获取用户的所有未完成且未删除todo"""
        return self.session.exec(
            select(Todo).where(
                Todo.user_id == user_id,
                Todo.completed == False,
                Todo.is_deleted == False
            )
        ).all()

    def create_todo(self, text: str, user_id: str) -> Todo:
        """创建新的todo"""
        new_todo = Todo(
            text=text,
            completed=False,
            user_id=user_id
        )
        self.session.add(new_todo)
        self.session.commit()
        self.session.refresh(new_todo)
        return new_todo

    def delete_todo(self, todo_id: str) -> bool:
        """软删除todo"""
        todo = self.get_todo(todo_id)
        if not todo:
            return False
        
        todo.is_deleted = True
        self.session.add(todo)
        self.session.commit()
        return True

    def complete_todo(self, todo_id: str) -> Optional[Todo]:
        """将todo标记为已完成"""
        todo = self.get_todo(todo_id)
        if not todo:
            return None
        
        todo.completed = True
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo