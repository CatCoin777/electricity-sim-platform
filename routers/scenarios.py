# routers/scenarios.py

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from security import decode_access_token
from mock_data.file_storage import list_scenarios, get_scenario, save_scenario
from mock_data.mock_users import mock_users
from typing import List, Dict, Any
import json
from datetime import datetime

router = APIRouter(prefix="/api/scenarios", tags=["Scenarios"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("/")
def get_scenarios(token: str = Depends(oauth2_scheme)):
    """Get all scenarios"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    scenarios = list_scenarios()
    return list(scenarios.values())


@router.get("/{scenario_id}")
def get_scenario_by_id(scenario_id: str, token: str = Depends(oauth2_scheme)):
    """Get specific scenario by ID"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return scenario


@router.post("/")
def create_scenario(scenario_data: Dict[str, Any], token: str = Depends(oauth2_scheme)):
    """Create a new scenario (teacher only)"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create scenarios")
    
    # Generate scenario ID
    scenario_id = f"scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Add default fields
    scenario_data.update({
        "id": scenario_id,
        "created_at": datetime.now().isoformat(),
        "status": "pending",
        "participants": [],
        "created_by": payload.get("sub")
    })
    
    save_scenario(scenario_id, scenario_data)
    return scenario_data


@router.post("/{scenario_id}/join")
def join_scenario(scenario_id: str, token: str = Depends(oauth2_scheme)):
    """Join a scenario"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    if scenario.get("status") != "active":
        raise HTTPException(status_code=400, detail="Scenario is not active")
    
    user_id = payload.get("sub")
    participants = scenario.get("participants", [])
    
    if user_id not in participants:
        participants.append(user_id)
        scenario["participants"] = participants
        save_scenario(scenario_id, scenario)
    
    return {"message": "Successfully joined scenario"}


@router.post("/{scenario_id}/start")
def start_scenario(scenario_id: str, token: str = Depends(oauth2_scheme)):
    """Start a scenario (teacher only)"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can start scenarios")
    
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario["status"] = "active"
    scenario["started_at"] = datetime.now().isoformat()
    save_scenario(scenario_id, scenario)
    
    return {"message": "Scenario started successfully"}


@router.post("/{scenario_id}/end")
def end_scenario(scenario_id: str, token: str = Depends(oauth2_scheme)):
    """End a scenario (teacher only)"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can end scenarios")
    
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    scenario["status"] = "completed"
    scenario["ended_at"] = datetime.now().isoformat()
    save_scenario(scenario_id, scenario)
    
    return {"message": "Scenario ended successfully"}


@router.delete("/{scenario_id}")
def delete_scenario(scenario_id: str, token: str = Depends(oauth2_scheme)):
    """Delete a scenario (teacher only)"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete scenarios")
    
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    # Delete scenario (implement in file_storage)
    from mock_data.file_storage import delete_scenario as delete_scenario_file
    delete_scenario_file(scenario_id)
    
    return {"message": "Scenario deleted successfully"} 