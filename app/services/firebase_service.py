import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from functools import lru_cache
from fastapi import HTTPException

from app.core.config import settings
from app.core.firebase_config import FIREBASE_PROJECT_ID, FIREBASE_DATABASE_URL, FIREBASE_STORAGE_BUCKET

@lru_cache()
def get_firebase_app():
    """
    Initialize and return Firebase app with caching for performance.
    """
    try:
        # Check if app is already initialized
        if not firebase_admin._apps:
            # Check if credentials file exists
            cred = None
            if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            else:
                # If no credentials file, try to create one from environment variables if available
                service_account_info = os.getenv("FIREBASE_SERVICE_ACCOUNT")
                if service_account_info:
                    try:
                        service_account_dict = json.loads(service_account_info)
                        cred = credentials.Certificate(service_account_dict)
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"Failed to parse service account info: {str(e)}")
                
                # If still no credentials, create application default credentials 
                # This works in GCP/Firebase hosting environments
                if not cred:
                    try:
                        cred = credentials.ApplicationDefault()
                    except Exception as e:
                        print(f"Failed to get application default credentials: {str(e)}")
                        return None
            
            # Initialize Firebase app
            firebase_options = {
                'projectId': FIREBASE_PROJECT_ID,
                'storageBucket': FIREBASE_STORAGE_BUCKET
            }
            
            # Add database URL if available
            if FIREBASE_DATABASE_URL:
                firebase_options['databaseURL'] = FIREBASE_DATABASE_URL
                
            firebase_app = firebase_admin.initialize_app(cred, firebase_options)
            return firebase_app
        else:
            # Return existing app
            return firebase_admin.get_app()
    except Exception as e:
        # Log error but don't fail app startup - just return None
        print(f"Firebase initialization error: {str(e)}")
        return None

def get_firestore_db():
    """
    Get Firestore database client.
    """
    app = get_firebase_app()
    if not app:
        raise HTTPException(status_code=500, detail="Firebase not initialized")
    return firestore.client(app) 