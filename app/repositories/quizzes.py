"""
Repository for quiz-related database operations with Firestore.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

from firebase_admin import firestore
from fastapi import HTTPException

from app.models.quiz import Quiz, QuizCreate, QuizUpdate, Category, Difficulty
from app.services.firebase_service import get_firestore_db

class QuizRepository:
    """Repository for quiz-related operations."""

    def __init__(self):
        self.db = get_firestore_db()
        self.collection = self.db.collection('quizzes')

    async def get_all(
        self, 
        limit: int = 100, 
        category: Optional[Category] = None,
        difficulty: Optional[Difficulty] = None,
        tags: Optional[List[str]] = None,
        only_public: bool = True
    ) -> List[Quiz]:
        """
        Get all quizzes with optional filtering.
        
        Args:
            limit: Maximum number of quizzes to return
            category: Filter by category
            difficulty: Filter by difficulty
            tags: Filter by tags
            only_public: Only return public quizzes
            
        Returns:
            List of Quiz objects
        """
        query = self.collection.where("active", "==", True)
        
        if only_public:
            query = query.where("is_public", "==", True)
            
        if category:
            query = query.where("category", "==", category.value)
            
        if difficulty:
            query = query.where("difficulty", "==", difficulty.value)
            
        # Filter by tags
        if tags and len(tags) == 1:
            query = query.where("tags", "array_contains", tags[0])
        
        # Get the documents
        docs = query.limit(limit).get()
        
        # Convert to Quiz objects
        quizzes = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            quizzes.append(Quiz.model_validate(doc_data))
            
        return quizzes

    async def get_by_id(self, quiz_id: str) -> Quiz:
        """
        Get a quiz by ID.
        
        Args:
            quiz_id: The ID of the quiz
            
        Returns:
            Quiz object
            
        Raises:
            HTTPException: If quiz not found
        """
        doc = self.collection.document(quiz_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Quiz not found")
            
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        
        return Quiz.model_validate(doc_data)

    async def get_by_user(
        self, 
        user_id: str, 
        limit: int = 100,
        include_private: bool = True
    ) -> List[Quiz]:
        """
        Get quizzes created by a specific user.
        
        Args:
            user_id: The ID of the user
            limit: Maximum number of quizzes to return
            include_private: Whether to include private quizzes
            
        Returns:
            List of Quiz objects
        """
        query = self.collection.where("created_by", "==", user_id).where("active", "==", True)
        
        if not include_private:
            query = query.where("is_public", "==", True)
            
        docs = query.limit(limit).get()
        
        quizzes = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            quizzes.append(Quiz.model_validate(doc_data))
            
        return quizzes

    async def create(self, quiz: QuizCreate, user_id: str) -> Quiz:
        """
        Create a new quiz.
        
        Args:
            quiz: QuizCreate object
            user_id: The ID of the user creating the quiz
            
        Returns:
            Created Quiz object
        """
        # Convert Pydantic model to dict
        quiz_dict = quiz.model_dump()
        
        # Convert enum values to strings
        if isinstance(quiz_dict.get("category"), Category):
            quiz_dict["category"] = quiz_dict["category"].value
            
        if isinstance(quiz_dict.get("difficulty"), Difficulty):
            quiz_dict["difficulty"] = quiz_dict["difficulty"].value
        
        # Add user ID and timestamps
        now = datetime.now()
        quiz_dict["created_by"] = user_id
        quiz_dict["created_at"] = now
        quiz_dict["updated_at"] = now
        quiz_dict["active"] = True
        
        # Calculate total questions
        quiz_dict["total_questions"] = len(quiz_dict.get("questions", []))
        
        # Add to Firestore
        doc_ref = self.collection.document()
        doc_ref.set(quiz_dict)
        
        # Return created quiz
        return await self.get_by_id(doc_ref.id)

    async def update(self, quiz_id: str, quiz_data: QuizUpdate, user_id: str) -> Quiz:
        """
        Update a quiz.
        
        Args:
            quiz_id: The ID of the quiz to update
            quiz_data: Dict with fields to update
            user_id: The ID of the user updating the quiz
            
        Returns:
            Updated Quiz object
            
        Raises:
            HTTPException: If quiz not found or user doesn't have permission
        """
        # Check if quiz exists and user has permission
        doc_ref = self.collection.document(quiz_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Quiz not found")
            
        quiz_data_dict = doc.to_dict()
        
        # Check if user has permission to update
        if quiz_data_dict.get("created_by") != user_id:
            raise HTTPException(status_code=403, detail="You don't have permission to update this quiz")
        
        # Prepare update data
        update_data = quiz_data.model_dump(exclude_unset=True)
        
        # Convert enum values to strings
        if isinstance(update_data.get("category"), Category):
            update_data["category"] = update_data["category"].value
            
        if isinstance(update_data.get("difficulty"), Difficulty):
            update_data["difficulty"] = update_data["difficulty"].value
        
        # Update total questions if questions were updated
        if "questions" in update_data:
            update_data["total_questions"] = len(update_data["questions"])
        
        # Add updated timestamp
        update_data["updated_at"] = datetime.now()
        
        # Update the document
        doc_ref.update(update_data)
        
        # Return updated quiz
        return await self.get_by_id(quiz_id)

    async def delete(self, quiz_id: str, user_id: str) -> bool:
        """
        Soft delete a quiz by setting active=False.
        
        Args:
            quiz_id: The ID of the quiz to delete
            user_id: The ID of the user deleting the quiz
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If quiz not found or user doesn't have permission
        """
        # Check if quiz exists and user has permission
        doc_ref = self.collection.document(quiz_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Quiz not found")
            
        quiz_data = doc.to_dict()
        
        # Check if user has permission to delete
        if quiz_data.get("created_by") != user_id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this quiz")
        
        # Soft delete by setting active=False
        doc_ref.update({
            "active": False,
            "updated_at": datetime.now()
        })
        
        return True 