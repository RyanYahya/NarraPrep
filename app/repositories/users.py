"""
Repository for user-related database operations with Firestore.
"""
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import hashlib

from firebase_admin import firestore, auth
from fastapi import HTTPException

from app.models.user import User, UserCreate, UserUpdate, UserRole
from app.services.firebase_service import get_firestore_db

class UserRepository:
    """Repository for user-related operations."""

    def __init__(self):
        self.db = get_firestore_db()
        self.collection = self.db.collection('users')

    async def get_all(self, limit: int = 100) -> List[User]:
        """
        Get all users.
        
        Args:
            limit: Maximum number of users to return
            
        Returns:
            List of User objects
        """
        docs = self.collection.limit(limit).get()
        
        users = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            users.append(User.model_validate(doc_data))
            
        return users

    async def get_by_id(self, user_id: str) -> User:
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            User object
            
        Raises:
            HTTPException: If user not found
        """
        doc = self.collection.document(user_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
            
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        
        return User.model_validate(doc_data)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            email: The email of the user
            
        Returns:
            User object or None if not found
        """
        query = self.collection.where("email", "==", email).limit(1)
        docs = query.get()
        
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            return User.model_validate(doc_data)
            
        return None

    async def create(self, user: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user: UserCreate object
            
        Returns:
            Created User object
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if email already exists
        existing_user = await self.get_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user in Firebase Auth
        try:
            firebase_user = auth.create_user(
                email=user.email,
                password=user.password,
                display_name=user.display_name
            )
            user_id = firebase_user.uid
        except auth.EmailAlreadyExistsError:
            raise HTTPException(status_code=400, detail="Email already registered in authentication system")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating user in authentication: {str(e)}")
        
        # Convert Pydantic model to dict (excluding password)
        user_dict = user.model_dump(exclude={"password"})
        
        # Convert enum values to strings
        if isinstance(user_dict.get("role"), UserRole):
            user_dict["role"] = user_dict["role"].value
        
        # Add timestamps
        now = datetime.now()
        user_dict["created_at"] = now
        user_dict["last_login"] = now
        
        # Add default stats, settings, etc.
        user_dict["stats"] = {
            "total_questions_attempted": 0,
            "correct_answers": 0,
            "accuracy": 0.0,
            "streak": 0,
            "longest_streak": 0,
            "xp": 0,
            "level": 1
        }
        
        user_dict["category_stats"] = {}
        
        user_dict["settings"] = {
            "daily_goal": 10,
            "notification_preferences": {},
            "theme": "light"
        }
        
        # Add to Firestore with Firebase Auth UID as document ID
        doc_ref = self.collection.document(user_id)
        doc_ref.set(user_dict)
        
        # Return created user
        return await self.get_by_id(user_id)

    async def update(self, user_id: str, user_data: UserUpdate) -> User:
        """
        Update a user.
        
        Args:
            user_id: The ID of the user to update
            user_data: UserUpdate object
            
        Returns:
            Updated User object
            
        Raises:
            HTTPException: If user not found
        """
        # Check if user exists
        doc_ref = self.collection.document(user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prepare update data
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Update in Firestore
        doc_ref.update(update_data)
        
        # Return updated user
        return await self.get_by_id(user_id)

    async def update_stats(self, user_id: str, question_id: str, category: str, is_correct: bool) -> User:
        """
        Update user statistics after answering a question.
        
        Args:
            user_id: The ID of the user
            question_id: The ID of the question answered
            category: The category of the question
            is_correct: Whether the answer was correct
            
        Returns:
            Updated User object
            
        Raises:
            HTTPException: If user not found
        """
        # Get current user
        user = await self.get_by_id(user_id)
        
        # Update stats
        doc_ref = self.collection.document(user_id)
        
        # Get current stats
        stats = user.stats.model_dump()
        
        # Update overall stats
        stats["total_questions_attempted"] += 1
        if is_correct:
            stats["correct_answers"] += 1
        
        # Calculate new accuracy
        if stats["total_questions_attempted"] > 0:
            stats["accuracy"] = round(stats["correct_answers"] / stats["total_questions_attempted"] * 100, 2)
        
        # Update category stats
        category_stats = user.category_stats.copy() if user.category_stats else {}
        
        if category not in category_stats:
            category_stats[category] = {"attempted": 0, "correct": 0, "accuracy": 0.0}
            
        category_stats[category]["attempted"] += 1
        if is_correct:
            category_stats[category]["correct"] += 1
            
        if category_stats[category]["attempted"] > 0:
            category_stats[category]["accuracy"] = round(
                category_stats[category]["correct"] / category_stats[category]["attempted"] * 100, 2
            )
        
        # Update in Firestore
        doc_ref.update({
            "stats": stats,
            "category_stats": category_stats
        })
        
        # Return updated user
        return await self.get_by_id(user_id) 