# routers/auth.py

from fastapi import APIRouter, HTTPException, Body
from schemas.auths import UserIn, UserOut, TokenOut, UserRegister
from mock_data.mock_users import mock_users, add_mock_user
from security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenOut)
async def login(user_in: UserIn):
    user = mock_users.get(user_in.username)
    if not user or user["hashed_password"] != user_in.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 自动识别用户角色，不需要前端传递
    user_role = user["role"]

    token = create_access_token({"sub": user["username"], "role": user_role})
    return {"access_token": token, "token_type": "bearer", "role": user_role}


@router.post("/register", response_model=UserOut)
async def register(user_data: UserRegister):
    if user_data.username in mock_users:
        raise HTTPException(status_code=400, detail="用户名已存在")

    new_user = {
        "username": user_data.username,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "hashed_password": user_data.password
    }
    add_mock_user(new_user)
    return new_user
