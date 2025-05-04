"""
Repository for attempt-related database operations with Firestore.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from firebase_admin import firestore
from fastapi import HTTPException

from app.models.attempt import Attempt, AttemptCreate, AttemptUpdate
from app.services.firebase_service import get_firestore_db
from app.repositories.questions import QuestionRepository
from app.repositories.quizzes import QuizRepository
from app.repositories.users import UserRepository

class AttemptRepository:
    """Repository for attempt-related operations."""

    def __init__(self):
        self.db = get_firestore_db()
        self.collection = self.db.collection('attempts')
        self.question_repo = QuestionRepository()
        self.quiz_repo = QuizRepository()
        self.user_repo = UserRepository()

    async def get_all_by_user(self, user_id: str, limit: int = 100) -> List[Attempt]:
        """
        Get all attempts for a specific user.
        
        Args:
            user_id: The ID of the user
            limit: Maximum number of attempts to return
            
        Returns:
            List of Attempt objects
        """
        query = self.collection.where("user_id", "==", user_id).order_by("started_at", direction=firestore.Query.DESCENDING)
        docs = query.limit(limit).get()
        
        attempts = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            attempts.append(Attempt.model_validate(doc_data))
            
        return attempts

    async def get_all_by_quiz(self, quiz_id: str, limit: int = 100) -> List[Attempt]:
        """
        Get all attempts for a specific quiz.
        
        Args:
            quiz_id: The ID of the quiz
            limit: Maximum number of attempts to return
            
        Returns:
            List of Attempt objects
        """
        query = self.collection.where("quiz_id", "==", quiz_id).order_by("started_at", direction=firestore.Query.DESCENDING)
        docs = query.limit(limit).get()
        
        attempts = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            attempts.append(Attempt.model_validate(doc_data))
            
        return attempts

    async def get_by_id(self, attempt_id: str) -> Attempt:
        """
        Get an attempt by ID.
        
        Args:
            attempt_id: The ID of the attempt
            
        Returns:
            Attempt object
            
        Raises:
            HTTPException: If attempt not found
        """
        doc = self.collection.document(attempt_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Attempt not found")
            
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        
        return Attempt.model_validate(doc_data)

    async def create(self, attempt: AttemptCreate, user_id: str) -> Attempt:
        """
        Create a new attempt.
        
        Args:
            attempt: AttemptCreate object
            user_id: The ID of the user creating the attempt
            
        Returns:
            Created Attempt object
        """
        # Convert Pydantic model to dict
        attempt_dict = attempt.model_dump()
        
        # Add user ID and timestamps
        now = datetime.now()
        attempt_dict["user_id"] = user_id
        attempt_dict["started_at"] = now
        
        # Initialize scoring fields
        attempt_dict["score"] = 0
        attempt_dict["max_score"] = 0
        attempt_dict["percentage"] = 0.0
        attempt_dict["time_taken_seconds"] = 0
        
        # Get quiz to set max score
        try:
            quiz = await self.quiz_repo.get_by_id(attempt.quiz_id)
            attempt_dict["max_score"] = quiz.total_questions
        except Exception:
            # If quiz not found, set max_score to 0
            pass
        
        # Add to Firestore
        doc_ref = self.collection.document()
        doc_ref.set(attempt_dict)
        
        # Return created attempt
        return await self.get_by_id(doc_ref.id)

    async def update(self, attempt_id: str, attempt_data: AttemptUpdate, user_id: str) -> Attempt:
        """
        Update an attempt.
        
        Args:
            attempt_id: The ID of the attempt to update
            attempt_data: AttemptUpdate object
            user_id: The ID of the user updating the attempt
            
        Returns:
            Updated Attempt object
            
        Raises:
            HTTPException: If attempt not found or user doesn't have permission
        """
        # Check if attempt exists and user has permission
        current_attempt = await self.get_by_id(attempt_id)
        
        if current_attempt.user_id != user_id:
            raise HTTPException(status_code=403, detail="You don't have permission to update this attempt")
        
        # Prepare update data
        update_data = attempt_data.model_dump(exclude_unset=True)
        
        # If attempt is being completed, calculate score
        if update_data.get("completed_at") or update_data.get("answers"):
            # Get the latest data
            attempt = await self.get_by_id(attempt_id)
            
            # Calculate score if answers are provided
            if update_data.get("answers"):
                correct_answers = sum(1 for answer in update_data["answers"] if answer["is_correct"])
                update_data["score"] = correct_answers
                
                # Calculate percentage
                if attempt.max_score > 0:
                    update_data["percentage"] = round((correct_answers / attempt.max_score) * 100, 2)
                
                # Update user stats for each answered question
                for answer in update_data["answers"]:
                    if "question_id" in answer:
                        # Get question to get category
                        try:
                            question = await self.question_repo.get_by_id(answer["question_id"])
                            await self.user_repo.update_stats(
                                user_id=user_id,
                                question_id=answer["question_id"],
                                category=question.category.value,
                                is_correct=answer["is_correct"]
                            )
                        except Exception:
                            # If question not found, skip updating stats
                            pass
            
            # Calculate time taken if completed
            if update_data.get("completed_at"):
                start_time = attempt.started_at
                end_time = update_data["completed_at"]
                update_data["time_taken_seconds"] = int((end_time - start_time).total_seconds())
        
        # Update the document
        doc_ref = self.collection.document(attempt_id)
        doc_ref.update(update_data)
        
        # Return updated attempt
        return await self.get_by_id(attempt_id)

    async def delete(self, attempt_id: str, user_id: str) -> bool:
        """
        Delete an attempt.
        
        Args:
            attempt_id: The ID of the attempt to delete
            user_id: The ID of the user deleting the attempt
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If attempt not found or user doesn't have permission
        """
        # Check if attempt exists and user has permission
        attempt = await self.get_by_id(attempt_id)
        
        if attempt.user_id != user_id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this attempt")
        
        # Hard delete
        doc_ref = self.collection.document(attempt_id)
        doc_ref.delete()
        
        return True 