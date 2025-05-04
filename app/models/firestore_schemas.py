"""
Firestore database schema definitions.
These represent the structure of documents in each collection.
"""

# Questions Collection Schema
QUESTION_SCHEMA = {
    "text": str,  # The question text
    "explanation": str,  # Explanation of the answer
    "category": str,  # e.g., "anatomy", "physiology", etc.
    "difficulty": str,  # "easy", "medium", "hard"
    "tags": list,  # List of tags for filtering/searching
    "options": [
        {
            "id": str,  # Option identifier
            "content": str,  # Option text
            "is_correct": bool,  # Whether this is the correct answer
            "explanation": str,  # Optional explanation for this specific option
        }
    ],
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "image_url": str,  # Optional URL to an image for the question
    "active": bool,  # Whether the question is active or archived
}

# Users Collection Schema
USER_SCHEMA = {
    "email": str,
    "display_name": str,
    "created_at": "timestamp",
    "last_login": "timestamp",
    "profile_image_url": str,
    "role": str,  # "student", "admin", etc.
    "stats": {
        "total_questions_attempted": int,
        "correct_answers": int,
        "accuracy": float,
        "streak": int,  # Current daily streak
        "longest_streak": int,
        "xp": int,  # Experience points
        "level": int,
    },
    "category_stats": {
        # Category-specific statistics
        "anatomy": {
            "attempted": int,
            "correct": int,
            "accuracy": float,
        },
        # Other categories...
    },
    "settings": {
        "daily_goal": int,
        "notification_preferences": dict,
        "theme": str,
    }
}

# Quizzes Collection Schema
QUIZ_SCHEMA = {
    "title": str,
    "description": str,
    "created_by": str,  # User ID
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "is_public": bool,
    "category": str,
    "tags": list,
    "difficulty": str,
    "time_limit_minutes": int,  # Optional time limit
    "questions": [
        {
            "question_id": str,  # Reference to question document
            "order": int,  # Order in the quiz
        }
    ],
    "total_questions": int,
    "active": bool,
}

# Attempts Collection Schema
ATTEMPT_SCHEMA = {
    "user_id": str,
    "quiz_id": str,
    "started_at": "timestamp",
    "completed_at": "timestamp",
    "time_taken_seconds": int,
    "score": int,
    "max_score": int,
    "percentage": float,
    "answers": [
        {
            "question_id": str,
            "selected_option_id": str,
            "is_correct": bool,
            "time_taken_seconds": int,  # Time spent on this question
        }
    ],
    "review_later": [str],  # List of question IDs to review later
} 