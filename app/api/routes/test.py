from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/test01", summary="测试路由",
            description="第一次写api路由")
def test_01():
    return {"message": "测试路由成功"}