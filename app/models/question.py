from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class OptionType(str, Enum):
    """Type of question option."""
    TEXT = "text"
    IMAGE = "image"


class Option(BaseModel):
    """Model for a question option."""
    id: str
    content: str
    option_type: OptionType = OptionType.TEXT
    is_correct: bool


class Difficulty(str, Enum):
    """Difficulty level of a question."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Category(str, Enum):
    """Medical category of a question."""
    ANATOMY = "anatomy"
    PHYSIOLOGY = "physiology"
    PATHOLOGY = "pathology"
    PHARMACOLOGY = "pharmacology"
    MICROBIOLOGY = "microbiology"
    GENERAL = "general"


class QuestionBase(BaseModel):
    """Base fields for a medical MCQ question."""
    text: str
    explanation: Optional[str] = None
    category: Category = Category.GENERAL
    difficulty: Difficulty = Difficulty.MEDIUM
    tags: List[str] = []


class QuestionCreate(QuestionBase):
    """Model for creating a new question with options."""
    options: List[Option]


class Question(QuestionBase):
    """Model for a complete question with ID and metadata."""
    id: str
    options: List[Option]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 