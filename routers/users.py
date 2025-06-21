# routers/users.py

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from schemas.auths import UserOut
from security import decode_access_token
from mock_data.mock_users import mock_users
from typing import Optional

router = APIRouter(prefix="/api/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("/me", response_model=UserOut)
async def get_me(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效令牌")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/me", response_model=UserOut)
async def update_me(
        token: str = Depends(oauth2_scheme),
        new_name: Optional[str] = Body(None),
        new_password: Optional[str] = Body(None)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效令牌")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if new_name:
        user["full_name"] = new_name
    if new_password:
        user["hashed_password"] = new_password
    return user
