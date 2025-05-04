from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enum."""
    STUDENT = "student"
    ADMIN = "admin"


class UserStats(BaseModel):
    """User statistics."""
    total_questions_attempted: int = 0
    correct_answers: int = 0
    accuracy: float = 0.0
    streak: int = 0
    longest_streak: int = 0
    xp: int = 0
    level: int = 1


class CategoryStats(BaseModel):
    """Statistics for a specific category."""
    attempted: int = 0
    correct: int = 0
    accuracy: float = 0.0


class UserSettings(BaseModel):
    """User preferences and settings."""
    daily_goal: int = 10
    notification_preferences: Dict = Field(default_factory=dict)
    theme: str = "light"


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    display_name: str
    role: UserRole = UserRole.STUDENT


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str


class UserUpdate(BaseModel):
    """Model for updating an existing user."""
    display_name: Optional[str] = None
    settings: Optional[UserSettings] = None


class User(UserBase):
    """Full user model with all fields."""
    id: str
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    profile_image_url: Optional[str] = None
    stats: UserStats = Field(default_factory=UserStats)
    category_stats: Dict[str, CategoryStats] = Field(default_factory=dict)
    settings: UserSettings = Field(default_factory=UserSettings)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 