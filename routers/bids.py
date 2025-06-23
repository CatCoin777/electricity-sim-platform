# routers/bids.py

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from security import decode_access_token
from mock_data.file_storage import get_bids, save_bid
from mock_data.mock_users import mock_users
from typing import List, Dict, Any
import json
from datetime import datetime

router = APIRouter(prefix="/api/bids", tags=["Bids"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/submit")
def submit_bid(bid_data: Dict[str, Any], token: str = Depends(oauth2_scheme)):
    """Submit a new bid"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    
    # Add bid metadata
    bid_data.update({
        "participant_id": user_id,
        "participant_name": mock_users.get(user_id, {}).get("full_name", user_id),
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    })
    
    scenario_id = bid_data.get("scenario_id")
    if not scenario_id:
        raise HTTPException(status_code=400, detail="Scenario ID is required")
    
    # Save bid
    save_bid(scenario_id, user_id, bid_data)
    
    return {"message": "Bid submitted successfully", "bid": bid_data}


@router.get("/my-bids")
def get_my_bids(scenario_id: str = Query(None), token: str = Depends(oauth2_scheme)):
    """Get current user's bids"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    
    if scenario_id:
        # Get bids for specific scenario
        all_bids = get_bids(scenario_id)
        my_bids = []
        for bid_id, bid in all_bids.items():
            if bid.get("participant_id") == user_id:
                bid["id"] = bid_id
                my_bids.append(bid)
    else:
        # Get all user's bids across all scenarios
        from mock_data.file_storage import list_scenarios
        scenarios = list_scenarios()
        my_bids = []
        
        for scenario_id, scenario in scenarios.items():
            scenario_bids = get_bids(scenario_id)
            for bid_id, bid in scenario_bids.items():
                if bid.get("participant_id") == user_id:
                    bid["id"] = bid_id
                    bid["scenario_name"] = scenario.get("name", scenario_id)
                    my_bids.append(bid)
    
    return my_bids


@router.get("/scenario/{scenario_id}")
def get_scenario_bids(scenario_id: str, token: str = Depends(oauth2_scheme)):
    """Get all bids for a specific scenario"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    bids_dict = get_bids(scenario_id)
    bids = []
    
    # Convert dictionary to list and add participant names
    for bid_id, bid in bids_dict.items():
        bid["id"] = bid_id
        participant_id = bid.get("participant_id")
        if participant_id:
            user = mock_users.get(participant_id, {})
            bid["participant_name"] = user.get("full_name", participant_id)
        bids.append(bid)
    
    return bids 