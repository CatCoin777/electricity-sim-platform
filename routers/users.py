# routers/users.py

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from schemas.auths import UserOut
from security import decode_access_token
from mock_data.mock_users import mock_users
from typing import Optional, Dict, Any
from mock_data.file_storage import get_bids, list_scenarios

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


@router.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme)):
    """Get user profile information"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "username": user.get("username"),
        "full_name": user.get("full_name"),
        "email": user.get("email", ""),
        "role": user.get("role")
    }


@router.put("/profile")
async def update_profile(profile_data: Dict[str, Any], token: str = Depends(oauth2_scheme)):
    """Update user profile information"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    user = mock_users.get(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update allowed fields
    if "full_name" in profile_data:
        user["full_name"] = profile_data["full_name"]
    if "email" in profile_data:
        user["email"] = profile_data["email"]
    
    return {"message": "Profile updated successfully", "user": user}


@router.get("/statistics")
async def get_user_statistics(token: str = Depends(oauth2_scheme)):
    """Get user statistics"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    username = payload.get("sub")
    
    # Calculate statistics
    total_bids = 0
    accepted_bids = 0
    total_revenue = 0
    participated_scenarios = set()
    
    # Get all scenarios and bids
    scenarios = list_scenarios()
    for scenario_id, scenario in scenarios.items():
        bids_dict = get_bids(scenario_id)
        user_bids = []
        for bid_id, bid in bids_dict.items():
            if bid.get("participant_id") == username:
                user_bids.append(bid)
        
        if user_bids:
            participated_scenarios.add(scenario_id)
            total_bids += len(user_bids)
            
            # Count accepted bids and revenue
            for bid in user_bids:
                if bid.get("status") == "accepted":
                    accepted_bids += 1
                    total_revenue += bid.get("revenue", 0)
    
    return {
        "totalBids": total_bids,
        "acceptedBids": accepted_bids,
        "totalRevenue": total_revenue,
        "participatedScenarios": len(participated_scenarios)
    }


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
