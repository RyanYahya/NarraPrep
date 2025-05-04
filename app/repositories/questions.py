"""
Repository for question-related database operations with Firestore.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from firebase_admin import firestore
from fastapi import HTTPException

from app.models.question import Question, QuestionCreate, Category, Difficulty
from app.services.firebase_service import get_firestore_db

class QuestionRepository:
    """Repository for question-related operations."""

    def __init__(self):
        self.db = get_firestore_db()
        self.collection = self.db.collection('questions')

    async def get_all(
        self, 
        limit: int = 100, 
        category: Optional[Category] = None,
        difficulty: Optional[Difficulty] = None,
        tags: Optional[List[str]] = None
    ) -> List[Question]:
        """
        Get all questions with optional filtering.
        
        Args:
            limit: Maximum number of questions to return
            category: Filter by category
            difficulty: Filter by difficulty
            tags: Filter by tags
            
        Returns:
            List of Question objects
        """
        query = self.collection.where("active", "==", True)
        
        if category:
            query = query.where("category", "==", category.value)
            
        if difficulty:
            query = query.where("difficulty", "==", difficulty.value)
            
        # Filter by tags - Firestore requires special handling for array contains
        if tags and len(tags) == 1:
            query = query.where("tags", "array_contains", tags[0])
        
        # Get the documents
        docs = query.limit(limit).get()
        
        # Convert to Question objects
        questions = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            questions.append(Question.model_validate(doc_data))
            
        return questions

    async def get_by_id(self, question_id: str) -> Question:
        """
        Get a question by ID.
        
        Args:
            question_id: The ID of the question
            
        Returns:
            Question object
            
        Raises:
            HTTPException: If question not found
        """
        doc = self.collection.document(question_id).get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Question not found")
            
        doc_data = doc.to_dict()
        doc_data["id"] = doc.id
        
        return Question.model_validate(doc_data)

    async def create(self, question: QuestionCreate) -> Question:
        """
        Create a new question.
        
        Args:
            question: QuestionCreate object
            
        Returns:
            Created Question object
        """
        # Convert Pydantic model to dict
        question_dict = question.model_dump()
        
        # Convert enum values to strings
        if isinstance(question_dict.get("category"), Category):
            question_dict["category"] = question_dict["category"].value
            
        if isinstance(question_dict.get("difficulty"), Difficulty):
            question_dict["difficulty"] = question_dict["difficulty"].value
        
        # Add timestamps and active flag
        now = datetime.now()
        question_dict["created_at"] = now
        question_dict["updated_at"] = now
        question_dict["active"] = True
        
        # Generate IDs for options
        for option in question_dict.get("options", []):
            if not option.get("id"):
                option["id"] = str(uuid.uuid4())
        
        # Add to Firestore
        doc_ref = self.collection.document()
        doc_ref.set(question_dict)
        
        # Return created question
        created_question = await self.get_by_id(doc_ref.id)
        return created_question

    async def update(self, question_id: str, question_data: Dict[str, Any]) -> Question:
        """
        Update a question.
        
        Args:
            question_id: The ID of the question to update
            question_data: Dict with fields to update
            
        Returns:
            Updated Question object
            
        Raises:
            HTTPException: If question not found
        """
        # Check if question exists
        doc_ref = self.collection.document(question_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Prepare update data
        update_data = question_data.copy()
        
        # Convert enum values to strings
        if isinstance(update_data.get("category"), Category):
            update_data["category"] = update_data["category"].value
            
        if isinstance(update_data.get("difficulty"), Difficulty):
            update_data["difficulty"] = update_data["difficulty"].value
        
        # Add updated timestamp
        update_data["updated_at"] = datetime.now()
        
        # Update the document
        doc_ref.update(update_data)
        
        # Return updated question
        return await self.get_by_id(question_id)

    async def delete(self, question_id: str) -> bool:
        """
        Soft delete a question by setting active=False.
        
        Args:
            question_id: The ID of the question to delete
            
        Returns:
            True if successful
            
        Raises:
            HTTPException: If question not found
        """
        # Check if question exists
        doc_ref = self.collection.document(question_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Soft delete by setting active=False
        doc_ref.update({
            "active": False,
            "updated_at": datetime.now()
        })
        
        return True 