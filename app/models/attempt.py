from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class QuestionAnswer(BaseModel):
    """User's answer to a specific question."""
    question_id: str
    selected_option_id: str
    is_correct: bool
    time_taken_seconds: int = 0


class AttemptBase(BaseModel):
    """Base attempt model."""
    quiz_id: str
    answers: List[QuestionAnswer] = []
    review_later: List[str] = []


class AttemptCreate(AttemptBase):
    """Model for creating a new attempt."""
    pass


class AttemptUpdate(BaseModel):
    """Model for updating an existing attempt."""
    answers: Optional[List[QuestionAnswer]] = None
    review_later: Optional[List[str]] = None
    completed_at: Optional[datetime] = None


class Attempt(AttemptBase):
    """Full attempt model with all fields."""
    id: str
    user_id: str
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    time_taken_seconds: int = 0
    score: int = 0
    max_score: int = 0
    percentage: float = 0.0
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 