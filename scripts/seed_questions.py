#!/usr/bin/env python3
"""
Seed script to populate the Firestore database with initial questions.
"""
import os
import sys
import asyncio
import uuid
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, project_root)

from app.models.question import QuestionCreate, Option, Category, Difficulty, OptionType
from app.repositories.questions import QuestionRepository

# Sample questions for seeding
SAMPLE_QUESTIONS = [
    {
        "text": "Which of the following is NOT a branch of the external carotid artery?",
        "explanation": "The ophthalmic artery is a branch of the internal carotid artery, not the external carotid artery. The other options (facial, maxillary, and superficial temporal) are all branches of the external carotid artery.",
        "category": Category.ANATOMY,
        "difficulty": Difficulty.MEDIUM,
        "tags": ["head", "neck", "arteries", "carotid"],
        "options": [
            Option(id=str(uuid.uuid4()), content="Facial artery", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Maxillary artery", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Ophthalmic artery", is_correct=True, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Superficial temporal artery", is_correct=False, option_type=OptionType.TEXT),
        ]
    },
    {
        "text": "Which hormone is primarily responsible for regulating blood calcium levels by increasing calcium absorption from the intestines?",
        "explanation": "Calcitriol (1,25-dihydroxycholecalciferol), the active form of vitamin D, is primarily responsible for increasing calcium absorption from the intestines. Parathyroid hormone (PTH) increases blood calcium by stimulating bone resorption and increasing renal calcium reabsorption. Calcitonin decreases blood calcium by inhibiting bone resorption. Cortisol has minimal direct effects on calcium homeostasis.",
        "category": Category.PHYSIOLOGY,
        "difficulty": Difficulty.MEDIUM,
        "tags": ["endocrinology", "calcium", "hormones", "vitamin D"],
        "options": [
            Option(id=str(uuid.uuid4()), content="Parathyroid hormone", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Calcitriol", is_correct=True, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Calcitonin", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Cortisol", is_correct=False, option_type=OptionType.TEXT),
        ]
    },
    {
        "text": "A 67-year-old patient presents with fatigue, weight loss, and bone pain. Laboratory studies show hypercalcemia, anemia, and elevated total protein. Which of the following is the most likely diagnosis?",
        "explanation": "Multiple myeloma is characterized by the proliferation of malignant plasma cells, which produces the classic triad of hypercalcemia, anemia, and elevated total protein (due to monoclonal gammopathy). Bone pain results from lytic lesions. Chronic lymphocytic leukemia typically presents with lymphocytosis and lymphadenopathy. Paget's disease presents with bone deformities and elevated alkaline phosphatase. Metastatic breast cancer can cause hypercalcemia but would not typically cause monoclonal gammopathy.",
        "category": Category.PATHOLOGY,
        "difficulty": Difficulty.HARD,
        "tags": ["hematology", "oncology", "plasma cell disorders"],
        "options": [
            Option(id=str(uuid.uuid4()), content="Chronic lymphocytic leukemia", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Multiple myeloma", is_correct=True, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Paget's disease of bone", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Metastatic breast cancer", is_correct=False, option_type=OptionType.TEXT),
        ]
    },
    {
        "text": "Which antibiotic mechanism involves inhibition of bacterial cell wall synthesis?",
        "explanation": "Beta-lactam antibiotics (including penicillins, cephalosporins, carbapenems, and monobactams) inhibit bacterial cell wall synthesis by binding to penicillin-binding proteins (PBPs) and preventing peptidoglycan cross-linking. Aminoglycosides inhibit protein synthesis by binding to the 30S ribosomal subunit. Fluoroquinolones inhibit DNA gyrase and topoisomerase IV. Sulfonamides inhibit folic acid synthesis by inhibiting dihydropteroate synthase.",
        "category": Category.PHARMACOLOGY,
        "difficulty": Difficulty.EASY,
        "tags": ["antibiotics", "microbiology", "cell wall"],
        "options": [
            Option(id=str(uuid.uuid4()), content="Aminoglycosides", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Fluoroquinolones", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Beta-lactams", is_correct=True, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Sulfonamides", is_correct=False, option_type=OptionType.TEXT),
        ]
    },
    {
        "text": "Which of the following bacteria is NOT typically considered part of the normal human microbiota?",
        "explanation": "Clostridium tetani, which causes tetanus, is not typically found as part of the normal human microbiota. It is primarily found in soil and animal feces. Escherichia coli is a normal inhabitant of the human gut. Staphylococcus epidermidis is found on human skin. Lactobacillus species are part of the normal vaginal flora.",
        "category": Category.MICROBIOLOGY,
        "difficulty": Difficulty.MEDIUM,
        "tags": ["microbiota", "bacteria", "normal flora"],
        "options": [
            Option(id=str(uuid.uuid4()), content="Escherichia coli", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Staphylococcus epidermidis", is_correct=False, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Clostridium tetani", is_correct=True, option_type=OptionType.TEXT),
            Option(id=str(uuid.uuid4()), content="Lactobacillus species", is_correct=False, option_type=OptionType.TEXT),
        ]
    }
]

async def seed_questions():
    """
    Seed the database with sample questions.
    """
    question_repo = QuestionRepository()
    
    for question_data in SAMPLE_QUESTIONS:
        question = QuestionCreate(**question_data)
        try:
            created_question = await question_repo.create(question)
            print(f"Created question: {created_question.id} - {created_question.text[:30]}...")
        except Exception as e:
            print(f"Error creating question: {e}")

if __name__ == "__main__":
    print("Seeding questions...")
    asyncio.run(seed_questions())
    print("Done seeding questions!") 