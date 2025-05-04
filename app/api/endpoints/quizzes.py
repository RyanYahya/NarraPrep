from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional

from app.models.quiz import Quiz, QuizCreate, QuizUpdate, Category, Difficulty
from app.services.firebase_service import get_firebase_app
from app.repositories.quizzes import QuizRepository

router = APIRouter()

@router.get("/", response_model=List[Quiz])
async def get_quizzes(
    limit: int = Query(100, ge=1, le=100),
    category: Optional[Category] = None,
    difficulty: Optional[Difficulty] = None,
    tags: Optional[List[str]] = Query(None),
    only_public: bool = True,
    firebase_app=Depends(get_firebase_app)
):
    """
    Get list of quizzes with optional filtering.
    """
    repo = QuizRepository()
    quizzes = await repo.get_all(
        limit=limit,
        category=category,
        difficulty=difficulty,
        tags=tags,
        only_public=only_public
    )
    return quizzes

@router.get("/user/{user_id}", response_model=List[Quiz])
async def get_user_quizzes(
    user_id: str,
    limit: int = Query(100, ge=1, le=100),
    include_private: bool = True,
    firebase_app=Depends(get_firebase_app)
):
    """
    Get quizzes created by a specific user.
    """
    repo = QuizRepository()
    quizzes = await repo.get_by_user(
        user_id=user_id,
        limit=limit,
        include_private=include_private
    )
    return quizzes

@router.get("/{quiz_id}", response_model=Quiz)
async def get_quiz(
    quiz_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Get a specific quiz by ID.
    """
    repo = QuizRepository()
    return await repo.get_by_id(quiz_id)

@router.post("/", response_model=Quiz, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    quiz: QuizCreate,
    # We will implement proper authentication later
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Create a new quiz.
    """
    repo = QuizRepository()
    return await repo.create(quiz, user_id)

@router.put("/{quiz_id}", response_model=Quiz)
async def update_quiz(
    quiz_id: str,
    quiz: QuizUpdate,
    # We will implement proper authentication later
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Update an existing quiz.
    """
    repo = QuizRepository()
    return await repo.update(quiz_id, quiz, user_id)

@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    # We will implement proper authentication later
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Delete a quiz (soft delete).
    """
    repo = QuizRepository()
    await repo.delete(quiz_id, user_id)
    return {"message": "Quiz deleted successfully"} 