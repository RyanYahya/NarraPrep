from fastapi import APIRouter
from app.core.firebase_config import FIREBASE_WEB_CONFIG

router = APIRouter()

@router.get("/firebase")
async def get_firebase_config():
    """
    Return Firebase configuration for the frontend.
    This endpoint can be called by the frontend to get the Firebase configuration.
    """
    return FIREBASE_WEB_CONFIG 