# routers/auth.py

from fastapi import APIRouter, HTTPException, Body
from schemas.auths import UserIn, UserOut, TokenOut
from mock_data.mock_users import mock_users, add_mock_user
from security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenOut)
async def login(user_in: UserIn):
    user = mock_users.get(user_in.username)
    if not user or user["hashed_password"] != user_in.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 验证角色是否匹配
    if user["role"] != user_in.role:
        raise HTTPException(status_code=401, detail="角色不匹配")

    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}


@router.post("/register", response_model=UserOut)
async def register(user_in: UserIn, full_name: str = Body(...), role: str = Body(...)):
    if user_in.username in mock_users:
        raise HTTPException(status_code=400, detail="用户名已存在")

    new_user = {
        "username": user_in.username,
        "full_name": full_name,
        "role": role,
        "hashed_password": user_in.password
    }
    add_mock_user(new_user)
    return new_user
