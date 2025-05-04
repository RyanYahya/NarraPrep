from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from datetime import datetime

from app.models.attempt import Attempt, AttemptCreate, AttemptUpdate
from app.services.firebase_service import get_firebase_app
from app.repositories.attempts import AttemptRepository

router = APIRouter()

@router.get("/user/{user_id}", response_model=List[Attempt])
async def get_user_attempts(
    user_id: str,
    limit: int = Query(100, ge=1, le=100),
    firebase_app=Depends(get_firebase_app)
):
    """
    Get all attempts for a specific user.
    """
    repo = AttemptRepository()
    attempts = await repo.get_all_by_user(user_id, limit)
    return attempts

@router.get("/quiz/{quiz_id}", response_model=List[Attempt])
async def get_quiz_attempts(
    quiz_id: str,
    limit: int = Query(100, ge=1, le=100),
    firebase_app=Depends(get_firebase_app)
):
    """
    Get all attempts for a specific quiz.
    """
    repo = AttemptRepository()
    attempts = await repo.get_all_by_quiz(quiz_id, limit)
    return attempts

@router.get("/{attempt_id}", response_model=Attempt)
async def get_attempt(
    attempt_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Get a specific attempt by ID.
    """
    repo = AttemptRepository()
    return await repo.get_by_id(attempt_id)

@router.post("/", response_model=Attempt, status_code=status.HTTP_201_CREATED)
async def create_attempt(
    attempt: AttemptCreate,
    # We will implement proper authentication later
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Create a new attempt (start a quiz).
    """
    repo = AttemptRepository()
    return await repo.create(attempt, user_id)

@router.put("/{attempt_id}", response_model=Attempt)
async def update_attempt(
    attempt_id: str,
    attempt: AttemptUpdate,
    # We will implement proper authentication later
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Update an attempt (add answers, mark questions for review, complete quiz).
    """
    repo = AttemptRepository()
    
    # If completing the attempt, add completion timestamp
    if attempt.completed_at is None and any(key in attempt.model_dump(exclude_unset=True) for key in ["answers"]):
        completed_data = attempt.model_copy()
        completed_data.completed_at = datetime.now()
        return await repo.update(attempt_id, completed_data, user_id)
    
    return await repo.update(attempt_id, attempt, user_id)

@router.delete("/{attempt_id}")
async def delete_attempt(
    attempt_id: str,
    # We will implement proper authentication later
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Delete an attempt.
    """
    repo = AttemptRepository()
    await repo.delete(attempt_id, user_id)
    return {"message": "Attempt deleted successfully"} 