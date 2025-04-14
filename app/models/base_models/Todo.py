from .Base import TableBase
from sqlmodel import SQLModel, Field

class TodoBase(TableBase):
    """待办事项基础模型类"""
    
    text: str = Field(
        nullable=False,  # 不允许为空
        index=True,      # 创建索引
        description="待办事项内容"  
    )
    
    completed: bool = Field(
        default=False,   # 默认值为False
        nullable=False,  # 不允许为空
        description="是否完成"  # 字段描述
    )



