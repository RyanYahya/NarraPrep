# NARRAPREP

A medical MCQ gamified test preparation platform. This repository contains the backend API built with FastAPI.

## Overview

NARRAPREP helps medical students prepare for exams through gamified multiple-choice questions. The system is built with:

- FastAPI backend
- Firebase for database and authentication
- Python 3.8+

## Setup

### Prerequisites

- Python 3.8 or higher
- Firebase account with a project set up

### Firebase Setup

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Select your project (narraprep)
3. In the project settings, go to the "Service accounts" tab
4. Click "Generate new private key" to download your service account credentials
5. Save the JSON file as `firebase-credentials.json` in the project root

Your credentials file should never be committed to version control. It's already in the .gitignore file.

### Environment Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create a `.env` file based on the example below:
```
# API Configuration
WORKERS=4

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
```

### Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

API documentation will be available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Connecting Frontend to Backend

The backend provides a configuration endpoint that returns the Firebase web configuration:
```
GET /api/v1/config/firebase
```

This endpoint returns the Firebase configuration needed for your frontend application to connect to Firebase.

## Project Structure

```
.
├── app/
│   ├── api/                  # API routes
│   │   ├── endpoints/        # API endpoint modules
│   │   └── router.py         # Main API router
│   ├── core/                 # Core application code
│   │   ├── config.py         # Configuration settings
│   │   └── firebase_config.py # Firebase configuration
│   ├── models/               # Pydantic data models
│   │   └── question.py       # Question models
│   └── services/             # Business logic services
│       └── firebase_service.py  # Firebase integration
├── main.py                   # Application entry point
├── requirements.txt          # Project dependencies
└── .env                      # Environment variables (create from example)
``` 