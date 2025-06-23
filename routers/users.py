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
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserOut)
async def update_me(
        token: str = Depends(oauth2_scheme),
        new_name: Optional[str] = Body(None),
        new_password: Optional[str] = Body(None)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if new_name:
        user["full_name"] = new_name
    if new_password:
        user["hashed_password"] = new_password
    return user


@router.put("/change-password")
async def change_password(
    current_password: str = Body(...),
    new_password: str = Body(...),
    token: str = Depends(oauth2_scheme)
):
    """Change user password"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify current password
    if user["hashed_password"] != current_password:
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Update password
    user["hashed_password"] = new_password
    return {"message": "Password changed successfully"}


@router.put("/update-profile")
async def update_profile(
    full_name: str = Body(...),
    token: str = Depends(oauth2_scheme)
):
    """Update user profile information"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update profile
    user["full_name"] = full_name
    return {"message": "Profile updated successfully", "user": user}
