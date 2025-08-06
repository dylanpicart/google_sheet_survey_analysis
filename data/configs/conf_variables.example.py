# data/configs/conf_variables.example.py

school_years = [
    "sy20-21", "sy21-22", "sy22-23"
]

group_params = {
    "younger": {
        "raw_dir": "data/raw/younger/",
        "question_list": "data/processed/audit/SF_OA_Younger.csv",
        "output_dir": "data/processed/younger/"
    },
    "older": {
        "raw_dir": "data/raw/older/",
        "question_list": "data/processed/audit/SF_OA_Older.csv",
        "output_dir": "data/processed/older/"
    }
}

meta_variants = {
    "School Year": ["Year", "year"],
    "Grade": ["Grade", "Grado"],
    "Name": ["Student Name", "First and Last Name:"]
}

cols_to_drop = ["SomeSpanishCol", "OtroCol"]

complicated_path = "/dummy/path"
older_keywords = ["High School", "HS"]
SCALE_ORDERS = {
    "likert": [
        "Strongly Disagree", "Disagree", "Neither Agree nor Disagree", "Agree", "Strongly Agree"
    ]
}
TAB_NAMES = ["Form Responses", "Survey"]

