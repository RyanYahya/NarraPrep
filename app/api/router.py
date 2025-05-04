from fastapi import APIRouter

from app.api.endpoints import health, questions, config, users, quizzes, attempts

api_router = APIRouter()

# Include various endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(attempts.router, prefix="/attempts", tags=["attempts"]) 