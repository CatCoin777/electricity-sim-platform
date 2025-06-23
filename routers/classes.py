# routers/classes.py

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from schemas.classes import (
    ClassInfo, ClassMember, ExperimentAssignment, StudentProgress
)
from mock_data.mock_users import mock_users
from security import decode_access_token
from typing import List, Dict
import json
from datetime import datetime, timedelta
import uuid
import os

router = APIRouter(prefix="/api/classes", tags=["Classes"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/")
async def create_class(
    class_data: Dict = Body(...),
    token: str = Depends(oauth2_scheme)
):
    """Create a new class (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create classes")
    
    teacher_id = payload.get("sub")
    class_id = f"class_{uuid.uuid4().hex[:8]}"
    
    class_info = {
        "class_id": class_id,
        "class_name": class_data.get("name", ""),
        "teacher_id": teacher_id,
        "students": [],
        "created_at": datetime.now().isoformat(),
        "description": class_data.get("description", ""),
        "max_students": class_data.get("max_students"),
        "academic_year": class_data.get("academic_year", "")
    }
    
    # Save class information
    save_class_info(class_info)
    
    return {
        "message": "Class created successfully",
        "class_id": class_id,
        "class_info": class_info
    }


@router.get("/")
async def get_my_classes(token: str = Depends(oauth2_scheme)):
    """Get classes for current user"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user_role = payload.get("role")
    
    all_classes = load_all_classes()
    my_classes = []
    
    if user_role == "teacher":
        # Teacher: get classes they created
        for class_id, class_info in all_classes.items():
            if class_info["teacher_id"] == user_id:
                class_info["id"] = class_id
                class_info["name"] = class_info["class_name"]  # Add name field for frontend
                class_info["student_count"] = len(class_info.get("students", []))
                my_classes.append(class_info)
    else:
        # Student: get classes they belong to
        for class_id, class_info in all_classes.items():
            if user_id in class_info.get("students", []):
                class_info["id"] = class_id
                class_info["name"] = class_info["class_name"]  # Add name field for frontend
                class_info["student_count"] = len(class_info.get("students", []))
                my_classes.append(class_info)
    
    return my_classes


@router.post("/{class_id}/add-student")
async def add_student_to_class(
    class_id: str,
    student_data: Dict = Body(...),
    token: str = Depends(oauth2_scheme)
):
    """Add a student to class (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can add students")
    
    # Get class information
    class_info = get_class_info(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check permissions
    if class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="You are not the teacher of this class")
    
    # Get student username
    student_username = student_data.get("username")
    if not student_username:
        raise HTTPException(status_code=400, detail="Student username is required")
    
    # Validate student exists
    if student_username not in mock_users or mock_users[student_username]["role"] != "student":
        raise HTTPException(status_code=404, detail="Student not found or is not a student")
    
    # Add student (avoid duplicates)
    if student_username not in class_info.get("students", []):
        if "students" not in class_info:
            class_info["students"] = []
        class_info["students"].append(student_username)
        
        # Save updates
        save_class_info(class_info)
        
        return {
            "message": "Student added successfully",
            "student_username": student_username
        }
    else:
        return {
            "message": "Student already in class",
            "student_username": student_username
        }


@router.delete("/{class_id}/remove-student/{student_id}")
async def remove_student_from_class(
    class_id: str,
    student_id: str,
    token: str = Depends(oauth2_scheme)
):
    """Remove a student from class (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can remove students")
    
    # Get class information
    class_info = get_class_info(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check permissions
    if class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="You are not the teacher of this class")
    
    # Remove student
    if student_id in class_info.get("students", []):
        class_info["students"].remove(student_id)
        
        # Save updates
        save_class_info(class_info)
        
        return {
            "message": "Student removed successfully",
            "student_id": student_id
        }
    else:
        raise HTTPException(status_code=404, detail="Student not found in class")


@router.get("/students")
async def get_all_students(token: str = Depends(oauth2_scheme)):
    """Get all students (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view all students")
    
    students = []
    for username, user in mock_users.items():
        if user["role"] == "student":
            students.append({
                "username": username,
                "full_name": user["full_name"],
                "role": user["role"]
            })
    
    return students


@router.get("/student-classes/{student_id}")
async def get_student_classes(
    student_id: str,
    token: str = Depends(oauth2_scheme)
):
    """Get classes that a student belongs to (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view student classes")
    
    all_classes = load_all_classes()
    student_classes = []
    
    for class_info in all_classes.values():
        if student_id in class_info.get("students", []):
            student_classes.append({
                "class_id": class_info["class_id"],
                "class_name": class_info["class_name"],
                "teacher_id": class_info["teacher_id"]
            })
    
    return student_classes


@router.post("/{class_id}/assign-experiment")
async def assign_experiment(
    class_id: str,
    scenario_id: str = Body(...),
    mechanism_type: str = Body("uniform_price"),
    duration_hours: int = Body(24),
    description: str = Body(None),
    token: str = Depends(oauth2_scheme)
):
    """Assign experiment to class (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can assign experiments")
    
    # Check class permissions
    class_info = get_class_info(class_id)
    if not class_info or class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="You are not the teacher of this class")
    
    # Check if scenario exists
    from mock_data.file_storage import get_scenario
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    # Create experiment assignment
    assignment_id = f"assignment_{uuid.uuid4().hex[:8]}"
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=duration_hours)
    
    assignment = ExperimentAssignment(
        assignment_id=assignment_id,
        class_id=class_id,
        scenario_id=scenario_id,
        mechanism_type=mechanism_type,
        start_time=start_time,
        end_time=end_time,
        status="active",
        description=description
    )
    
    # Save assignment
    save_experiment_assignment(assignment.dict())
    
    return {
        "message": "Experiment assigned successfully",
        "assignment_id": assignment_id,
        "assignment": assignment.dict()
    }


@router.get("/{class_id}/progress")
async def get_class_progress(
    class_id: str,
    assignment_id: str = None,
    token: str = Depends(oauth2_scheme)
):
    """Get class progress (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view class progress")
    
    # Check class permissions
    class_info = get_class_info(class_id)
    if not class_info or class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="You are not the teacher of this class")
    
    # Get experiment assignments
    assignments = get_experiment_assignments(class_id)
    if assignment_id:
        assignments = [a for a in assignments if a["assignment_id"] == assignment_id]
    
    # Calculate progress
    progress_data = []
    for assignment in assignments:
        scenario_id = assignment["scenario_id"]
        students = class_info["students"]
        
        # Get bid data
        from mock_data.file_storage import get_bids
        bid_data = get_bids(scenario_id)
        
        # Calculate progress for each student
        for student_id in students:
            submitted = student_id in bid_data
            progress = StudentProgress(
                student_id=student_id,
                scenario_id=scenario_id,
                assignment_id=assignment["assignment_id"],
                submitted=submitted,
                submitted_at=bid_data.get(student_id, {}).get("submitted_at") if submitted else None
            )
            progress_data.append(progress.dict())
    
    return {
        "class_info": class_info,
        "assignments": assignments,
        "progress": progress_data,
        "summary": {
            "total_students": len(class_info["students"]),
            "total_assignments": len(assignments),
            "submission_rate": calculate_submission_rate(progress_data)
        }
    }


@router.get("/my-assignments")
async def get_my_assignments(token: str = Depends(oauth2_scheme)):
    """Get experiment assignments for current user (Student only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "student":
        raise HTTPException(status_code=403, detail="Only students can view assignments")
    
    student_id = payload.get("sub")
    
    # Get classes the student belongs to
    all_classes = load_all_classes()
    my_classes = [cls for cls in all_classes if student_id in cls["students"]]
    
    # Get all experiment assignments
    all_assignments = []
    for class_info in my_classes:
        assignments = get_experiment_assignments(class_info["class_id"])
        for assignment in assignments:
            assignment["class_name"] = class_info["class_name"]
            all_assignments.append(assignment)
    
    return all_assignments


@router.get("/{class_id}")
async def get_class_details(
    class_id: str,
    token: str = Depends(oauth2_scheme)
):
    """Get class details"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    class_info = get_class_info(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check permissions
    user_id = payload.get("sub")
    user_role = payload.get("role")
    
    if user_role == "teacher":
        if class_info["teacher_id"] != user_id:
            raise HTTPException(status_code=403, detail="You are not the teacher of this class")
    else:
        if user_id not in class_info.get("students", []):
            raise HTTPException(status_code=403, detail="You are not a member of this class")
    
    # Add student details
    students_with_details = []
    for student_username in class_info.get("students", []):
        if student_username in mock_users:
            student_info = mock_users[student_username]
            students_with_details.append({
                "id": student_username,
                "username": student_username,
                "full_name": student_info["full_name"],
                "email": student_info.get("email", ""),
                "joined_at": class_info.get("created_at", "")
            })
    
    class_info["students"] = students_with_details
    class_info["id"] = class_id
    class_info["student_count"] = len(students_with_details)
    
    return class_info


@router.delete("/{class_id}")
async def delete_class(
    class_id: str,
    token: str = Depends(oauth2_scheme)
):
    """Delete a class (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can delete classes")
    
    class_info = get_class_info(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check permissions
    if class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="You are not the teacher of this class")
    
    # Delete class from the JSON file
    all_classes = load_all_classes()
    if class_id in all_classes:
        del all_classes[class_id]
        
        # Save updated classes back to file
        filename = "mock_data/classes.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_classes, f, ensure_ascii=False, indent=2, default=str)
    
    return {"message": "Class deleted successfully"}


@router.put("/{class_id}")
async def update_class(
    class_id: str,
    class_data: Dict = Body(...),
    token: str = Depends(oauth2_scheme)
):
    """Update a class (Teacher only)"""
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can update classes")
    
    class_info = get_class_info(class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check permissions
    if class_info["teacher_id"] != payload.get("sub"):
        raise HTTPException(status_code=403, detail="You are not the teacher of this class")
    
    # Update class information
    class_info.update({
        "class_name": class_data.get("name", class_info["class_name"]),
        "description": class_data.get("description", class_info.get("description", "")),
        "max_students": class_data.get("max_students", class_info.get("max_students")),
        "academic_year": class_data.get("academic_year", class_info.get("academic_year", ""))
    })
    
    # Save updates
    save_class_info(class_info)
    
    return {
        "message": "Class updated successfully",
        "class_info": class_info
    }


# Helper functions
def save_class_info(class_info: Dict):
    """Save class information"""
    filename = "mock_data/classes.json"
    all_classes = load_all_classes()
    all_classes[class_info["class_id"]] = class_info
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_classes, f, ensure_ascii=False, indent=2, default=str)


def load_all_classes() -> Dict:
    """Load all class information"""
    filename = "mock_data/classes.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_class_info(class_id: str) -> Dict:
    """Get class information"""
    all_classes = load_all_classes()
    return all_classes.get(class_id)


def save_experiment_assignment(assignment: Dict):
    """Save experiment assignment"""
    filename = "mock_data/assignments.json"
    all_assignments = load_all_assignments()
    all_assignments[assignment["assignment_id"]] = assignment
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_assignments, f, ensure_ascii=False, indent=2, default=str)


def load_all_assignments() -> Dict:
    """Load all experiment assignments"""
    filename = "mock_data/assignments.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_experiment_assignments(class_id: str) -> List[Dict]:
    """Get experiment assignments for a class"""
    all_assignments = load_all_assignments()
    return [a for a in all_assignments.values() if a["class_id"] == class_id]


def calculate_submission_rate(progress_data: List[Dict]) -> float:
    """Calculate submission rate"""
    if not progress_data:
        return 0.0
    
    submitted_count = sum(1 for p in progress_data if p["submitted"])
    return round(submitted_count / len(progress_data) * 100, 2) 