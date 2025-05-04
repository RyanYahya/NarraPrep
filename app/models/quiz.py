from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

from app.models.question import Category, Difficulty


class QuizQuestionRef(BaseModel):
    """Reference to a question within a quiz."""
    question_id: str
    order: int


class QuizBase(BaseModel):
    """Base quiz model."""
    title: str
    description: str
    category: Optional[Category] = None
    difficulty: Optional[Difficulty] = None
    time_limit_minutes: Optional[int] = None
    tags: List[str] = []
    is_public: bool = True


class QuizCreate(QuizBase):
    """Model for creating a new quiz."""
    questions: List[QuizQuestionRef]


class QuizUpdate(BaseModel):
    """Model for updating an existing quiz."""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[Category] = None
    difficulty: Optional[Difficulty] = None
    time_limit_minutes: Optional[int] = None
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None
    questions: Optional[List[QuizQuestionRef]] = None
    active: Optional[bool] = None


class Quiz(QuizBase):
    """Full quiz model with all fields."""
    id: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    questions: List[QuizQuestionRef]
    total_questions: int
    active: bool = True
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 