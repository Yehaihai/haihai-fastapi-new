from fastapi import APIRouter, HTTPException, Body
from app.api.depends import SessionDep, CurrentUser
from app.crud.TodoCRUD import TodoCRUD
from app.models.table import Todo


router = APIRouter()

@router.get("/all", summary="获取当前用户的所有todo",
            description="获取当前用户的所有todo")
def get_all_todo(session: SessionDep, current_user: CurrentUser):
    # 使用TodoCRUD查询当前用户所有未删除的todo
    todo_crud = TodoCRUD(session)
    todos = todo_crud.get_all_todos(current_user.id)
    return todos

# 创建新的todo对象
@router.post("/add", summary="添加一个todo",
            description="添加一个todo")
def add_todo(session: SessionDep, current_user: CurrentUser, text: str = Body(embed=True)):
    # 使用TodoCRUD创建新的todo对象
    todo_crud = TodoCRUD(session)
    new_todo = todo_crud.create_todo(text, current_user.id)
    return {"message": "添加todo成功", "todo": new_todo}

# 删除一个todo
@router.delete("/", summary="删除一个todo",
               description="通过ID删除一个todo")
def delete_todo(session: SessionDep, todo_id: str = Body(embed=True)):
    # 使用TodoCRUD删除todo
    todo_crud = TodoCRUD(session)
    todo = todo_crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo不存在")
    
    success = todo_crud.delete_todo(todo_id)
    if success:
        return {"message": "删除todo成功"}
    else:
        raise HTTPException(status_code=500, detail="删除todo失败")

# 查询已完成的 todo
@router.get("/completed", summary="获取已完成的todo",
            description="获取所有已完成的todo")
def get_completed_todos(session: SessionDep, current_user: CurrentUser):
    # 使用TodoCRUD查询所有已完成且未删除的todo
    todo_crud = TodoCRUD(session)
    completed_todos = todo_crud.get_completed_todos(current_user.id)
    return completed_todos

# 查询未完成的 todo
@router.get("/uncompleted", summary="获取未完成的todo",
            description="获取所有未完成的todo")
def get_uncompleted_todos(session: SessionDep, current_user: CurrentUser):
    # 使用TodoCRUD查询所有未完成且未删除的todo
    todo_crud = TodoCRUD(session)
    uncompleted_todos = todo_crud.get_uncompleted_todos(current_user.id)
    return uncompleted_todos

# 完成一个todo
@router.put("/complete", summary="完成一个todo",
            description="将一个todo标记为已完成")
def complete_todo(session: SessionDep, current_user: CurrentUser, todo_id: str = Body(embed=True)):
    # 使用TodoCRUD查询和更新todo
    todo_crud = TodoCRUD(session)
    todo = todo_crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo不存在")
    
    # 验证todo是否属于当前用户
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作此todo")
    
    updated_todo = todo_crud.complete_todo(todo_id)
    if updated_todo:
        return {"message": "完成todo成功"}
    else:
        raise HTTPException(status_code=500, detail="完成todo失败")
