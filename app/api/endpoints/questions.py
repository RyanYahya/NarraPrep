from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.models.question import Question, QuestionCreate, Category, Difficulty
from app.services.firebase_service import get_firebase_app
from app.repositories.questions import QuestionRepository

router = APIRouter()

@router.get("/", response_model=List[Question])
async def get_questions(
    limit: int = Query(100, ge=1, le=100),
    category: Optional[Category] = None,
    difficulty: Optional[Difficulty] = None,
    tags: Optional[List[str]] = Query(None),
    firebase_app=Depends(get_firebase_app)
):
    """
    Get list of questions with optional filtering.
    """
    repo = QuestionRepository()
    questions = await repo.get_all(
        limit=limit,
        category=category,
        difficulty=difficulty,
        tags=tags
    )
    return questions

@router.get("/{question_id}", response_model=Question)
async def get_question(
    question_id: str, 
    firebase_app=Depends(get_firebase_app)
):
    """
    Get a specific question by ID.
    """
    repo = QuestionRepository()
    return await repo.get_by_id(question_id)

@router.post("/", response_model=Question, status_code=201)
async def create_question(
    question: QuestionCreate,
    firebase_app=Depends(get_firebase_app)
):
    """
    Create a new question.
    """
    repo = QuestionRepository()
    return await repo.create(question)

@router.put("/{question_id}", response_model=Question)
async def update_question(
    question_id: str,
    question: QuestionCreate,
    firebase_app=Depends(get_firebase_app)
):
    """
    Update an existing question.
    """
    repo = QuestionRepository()
    return await repo.update(question_id, question.model_dump())

@router.delete("/{question_id}")
async def delete_question(
    question_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Delete a question (soft delete).
    """
    repo = QuestionRepository()
    await repo.delete(question_id)
    return {"message": "Question deleted successfully"} 