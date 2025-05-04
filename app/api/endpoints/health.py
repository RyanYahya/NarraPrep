from fastapi import APIRouter, Depends

from app.services.firebase_service import get_firebase_app

router = APIRouter()

@router.get("/")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy", "service": "NARRAPREP API"}

@router.get("/firebase")
async def firebase_health(firebase_app=Depends(get_firebase_app)):
    """
    Check Firebase connection is working.
    """
    try:
        # Just check if we can get the Firebase app
        if firebase_app:
            return {"status": "healthy", "firebase": "connected"}
        return {"status": "unhealthy", "firebase": "not connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)} 