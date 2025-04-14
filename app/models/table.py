
from sqlmodel import SQLModel
from app.models.base_models.SMSCodeRecordBase import SMSCodeRecordBase
from app.models.base_models.UserBase import UserBase
from app.models.base_models.Todo import TodoBase
from sqlmodel import Field, Relationship
from uuid import UUID  # 添加UUID导入

# 用户表
class User(UserBase, table=True):
    # 建立与 Todo 表的一对多关系
    todos: list["Todo"] = Relationship(back_populates="user")


# 短信发送记录
class SMSCodeRecord(SMSCodeRecordBase, table=True):
    pass


# 待办事项表
class Todo(TodoBase, table=True):
    # 建立与 User 表的多对一关系
    user_id: UUID = Field(foreign_key="user.id")  # 修改类型为UUID
    user: User = Relationship(back_populates="todos")
