# routers/admin.py

from fastapi import APIRouter, HTTPException
from schemas.simulation import ScenarioCreateRequest
from mock_data.file_storage import get_scenario, save_scenario

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/scenario/create")
def create_scenario(req: ScenarioCreateRequest):
    if get_scenario(req.scenario_id):
        raise HTTPException(status_code=400, detail="Scenario already exists")
    save_scenario(req.scenario_id, req.dict())
    return {"message": "Scenario created"}
