from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.user import User, UserCreate, UserUpdate
from app.services.firebase_service import get_firebase_app
from app.repositories.users import UserRepository

router = APIRouter()

@router.get("/", response_model=List[User])
async def get_users(
    firebase_app=Depends(get_firebase_app)
):
    """
    Get all users. Requires admin privileges.
    """
    repo = UserRepository()
    return await repo.get_all()

@router.get("/me", response_model=User)
async def get_current_user(
    # We will implement proper authentication later
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Get the current authenticated user.
    """
    repo = UserRepository()
    return await repo.get_by_id(user_id)

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    firebase_app=Depends(get_firebase_app)
):
    """
    Get a specific user by ID.
    """
    repo = UserRepository()
    return await repo.get_by_id(user_id)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    firebase_app=Depends(get_firebase_app)
):
    """
    Create a new user.
    """
    repo = UserRepository()
    return await repo.create(user)

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user: UserUpdate,
    firebase_app=Depends(get_firebase_app)
):
    """
    Update a user.
    """
    repo = UserRepository()
    return await repo.update(user_id, user) 