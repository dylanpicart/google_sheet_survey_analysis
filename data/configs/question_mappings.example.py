# data/configs/question_mappings.example.py

YOUNGER_QUESTION_MAPPING = {
    "Fake Question 1": "Standardized Q1",
    "Fake Question 2": "Standardized Q2"
}

OLDER_QUESTION_MAPPING = {
    "Fake Question 3": "Standardized Q3"
}

QCON_MAP = {
    "Q1": "General Safety",
    "Q2": "General Trust"
}

RESCON_MAPPING = {
    "Strongly Disagree": "Disagree",
    "Strongly Agree": "Agree"
}

EN_SP_MAPPING = {
    "Satisfied?": "¿Está satisfecho?"
}

ANSWER_MAPPING = {
    "Sí": "Yes",
    "No": "No"
}

def build_lookup(mapping):
    # Dummy function for import compatibility
    return {}

def audit_and_clean_columns(questions, lookup):
    # Dummy function for import compatibility
    return {q: {"canonical": None, "reason": "Dummy", "suggestions": []} for q in questions}
