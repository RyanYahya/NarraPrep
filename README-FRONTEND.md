# NARRAPREP Frontend

This is a simple Streamlit frontend for interacting with the NARRAPREP API.

## Features

- Browse and filter questions by category and difficulty
- Add new questions with multiple-choice options
- Manage users and their permissions
- Create and manage quizzes
- Take quizzes and view results
- View user statistics

## Setup

### Prerequisites

- Python 3.8 or higher
- NARRAPREP backend running (see main README.md)

### Installation

1. Activate the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages (already done if you followed the main setup):
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the `frontend` directory with the following content:
```
API_URL=http://localhost:8000
```

### Running the Frontend

Make sure the backend is running first:
```bash
uvicorn main:app --reload
```

Then, in a new terminal, run the frontend:
```bash
python frontend/run.py
```

Or directly with Streamlit:
```bash
streamlit run frontend/app.py
```

The frontend will be available at http://localhost:8501.

## Usage

### Questions Management
- Browse questions with filtering by category, difficulty, etc.
- View question details, including options and correct answers
- Add new questions with multiple options

### User Management
- View all users (admin only)
- Create new users with different roles

### Quizzes Management
- Browse quizzes with filtering
- Create new quizzes by selecting questions
- Configure quiz settings like time limits and visibility

### Taking Quizzes
- Select a quiz to attempt
- Answer questions one by one
- View results after completion

## Testing

For development/testing, the frontend provides a simplified authentication system with a preset admin user. In a production environment, this would be replaced with proper Firebase Authentication.

## Additional Configuration

You can modify the following files for customization:
- `frontend/config.py`: API endpoints and configuration settings
- `frontend/api.py`: API client for communicating with the backend 