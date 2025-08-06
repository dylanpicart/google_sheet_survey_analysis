# data/configs/question_mappings.py

# Younger Survey Question Mapping
YOUNGER_QUESTION_MAPPING = {
    # Question 1
    "What's the most important thing you learned from your PWC social worker or in your PWC program this year?": ["Important Learning from PWC",],

    # Question 2
    "Thinking about this school year, to what extent do you agree with the following statements?": {
        "There is an adult/adults at my school that I can turn to for support or help.": {
            "variations": ["There is an adult/adults at my school that I can turn to for support or help.", "There are one or more adults at my school that I can turn to for support or help."],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "I feel connected to other students.": {
            "variations": ["I feel connected to other students."],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school.": {
            "variations": ["I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school."],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Adults who work at my school encourage students to have conversations around race, racism and social justice.": {
            "variations": ["Adults who work at my school encourage students to have conversations around race, racism and social justice."],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
    },

    # Question 3
    "Please tell us if you think your PWC program helped you in any of these areas": {
        "I like going to school more.": {
            "variations": ["I like going to school more."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I learned new ways to take care of myself.": {
            "variations": ["I learned new ways to take care of myself."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I feel sad or mad less often.": {
            "variations": ["I feel sad or mad less often."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "When I feel sad or mad, I can better handle my big feelings.": {
            "variations": ["When I feel sad or mad, I can better handle my big feelings."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "There are adults at my school who I can trust and ask for help.": {
            "variations": ["There are adults at my school who I can trust and ask for help."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I get along better with kids at school.": {
            "variations": ["I get along better with kids at school."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I am more confident and positive about myself.": {
            "variations": ["I am more confident and positive about myself."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I get along better with my teachers.": {
            "variations": ["I get along better with my teachers."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I found new things I like to do.": {
            "variations": ["I found new things I like to do."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I found new things I like about myself.": {
            "variations": ["I found new things I like about myself."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I know better how to ask for help when I need it.": {
            "variations": ["I know better how to ask for help when I need it."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I am better at sharing my feelings.": {
            "variations": ["I am better at sharing my feelings."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        },
        "I am happier.": {
            "variations": ["I am happier."],
            "responses": {"Yes": 0, "Maybe": 0, "No": 0}
        }
    },

    # Question 4
    "What would you like from PWC moving forward?": "Future Requests from PWC",
    "What else would you like from PWC?": "Future Requests from PWC",

    # Question 5
    "If you participated in counseling, what would you change about working with PWC?": "Counseling Feedback",

    # Question 6
    "What was your favorite part about PWC’s programs this year?": "Favorite Part of PWC Programs",
    "What did you like about PWC?": "Favorite Part of PWC Programs",

    # Question 7
    "Did you feel happier about going to school on the days when you got to see your PWC social worker?": "Happiness with Social Worker Visits",
    "Did you feel happier on days you saw your PWC social worker?": "Happiness with Social Worker Visits",

    # Question 8
    "What's the most important thing you learned from your PWC social worker or in your PWC program this year?": "Important Learning from PWC",
    "What did you learn from your PWC social worker or program?": "Important Learning from PWC",
}



# Older Survey Question Mapping
OLDER_QUESTION_MAPPING = {
    # Question 1
    "Which of the following PWC programs did you participate in this year? Choose all that apply:": {
        "variations": ["Which of the following PWC programs did you participate in this year? Choose all that apply"],
        "responses": {"Individual Counseling": 0, "Arts Programs": 0, "After School": 0, "Small Groups": 0, "Full Class or Advisory Program": 0}
    },

    # Question 2 (shared with younger)
    "Thinking about this school year, to what extent do you agree with the following statements?": {
        "I like going to school.": {
            "variations": ["I like going to school"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "There is an adult/adults at my school that I can turn to for support or help.": {
            "variations": ["There is an adult/adults at my school that I can turn to for support or help.", "There are one or more adults at my school that I can turn to for support or help."],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "I feel connected to other students.": {
            "variations": ["I feel connected to other students.", "I felt connected to my peers."],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school.": {
            "variations": ["I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school.", "Adults who work at my school encourage students to express and take pride in their full identities and to respect each other’s identities"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Adults who work at my school encourage students to have conversations around race, racism and social justice.": {
            "variations": ["Adults who work at my school encourage students to have conversations around race, racism and social justice.", "Adults who work at my school encourage students to have conversations around race and social justice."],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        }
    },

    # Question 3
    "Partnership with Children has provided or helped me this year with:": {
        "Supportive relationships with adults who care about me": {
            "variations": ["Supportive relationships with adults who care about me"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Getting internet access so I could log into remote school": {
            "variations": ["Getting internet access so I could log into remote school"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Opportunities to interact positively with my peers": {
            "variations": ["Opportunities to interact positively with my peers"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "A space to honestly share what I am feeling or thinking": {
            "variations": ["A space to honestly share what I am feeling or thinking"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Help staying motivated in school": {
            "variations": ["Help staying motivated in school"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Help dealing with and managing my emotions": {
            "variations": ["Help dealing with and managing my emotions"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Support with personal challenges in my life": {
            "variations": ["Support with personal challenges in my life"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Support with academic challenges": {
            "variations": ["Support with academic challenges"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Support with family issues": {
            "variations": ["Support with family issues"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Support in advocating for myself and asking for help when needed": {
            "variations": ["Support in advocating for myself and asking for help when needed"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Support with remote learning technology or issues (i.e. laptops, tablets, logging in)": {
            "variations": ["Support with remote learning technology or issues (i.e. laptops, tablets, logging in)"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Help for my family with obtaining food/groceries": {
            "variations": ["Help for my family with obtaining food/groceries"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        }
    },
    # "How have PWC programs helped you this year / what have the programs given you?": ["How have PWC programs helped you this year / what have the programs given you?"],
    
    # Question 4
    "Please think about if PWC helped you grow or change this year. Did you...": {
        "Learn new ways to take care of myself": {
            "variations": ["Learn new ways to take care of myself"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Learn how to better manage how I act when I have strong emotions": {
            "variations": ["Learn how to better manage how I act when I have strong emotions"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Learn how to better advocate for myself and ask for help": {
            "variations": ["Learn how to better advocate for myself and ask for help"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Learn how to better share what I am thinking and feeling": {
            "variations": ["Learn how to better share what I am thinking and feeling"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Learn how to make better decisions": {
            "variations": ["Learn how to make better decisions"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Feel sad or mad less often": {
            "variations": ["Feel sad or mad less often"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Feel more confident and positive about myself": {
            "variations": ["Feel more confident and positive about myself"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Feel happier": {
            "variations": ["Feel happier"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Improve my relationships with other students": {
            "variations": ["Improve my relationships with other students"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Improve my relationships with teachers": {
            "variations": ["Improve my relationships with teachers"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Improve my relationships with my family": {
            "variations": ["Improve my relationships with my family"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        },
        "Improve my academic performance": {
            "variations": ["Improve my academic performance"],
            "responses": {"Strongly Agree": 0, "Agree": 0, "Neither": 0, "Disagree": 0, "Strongly Disagree": 0}
        }
    },

    # Question 5
    # "In what ways can PWC best support you moving forward?": "Future Support from PWC",
    # "What can PWC do better to support you?": "Future Support from PWC",

    # Question 6
    # "What aspects of your PWC program or services would you change?": "Program Change Suggestions",
    # "If you could change anything about PWC programs, what would it be?": "Program Change Suggestions",

    # Question 7
    # "What aspects of this past school year did you find valuable and would you want to continue moving forward?": "Valuable Aspects to Continue",
    # "What from this year should PWC continue?": "Valuable Aspects to Continue",

    # Question 8
    "Do you / did you feel differently about coming to school on day with PWC programs?": ["Do you / did you feel differently about coming to school on day with PWC programs?",
                                                                                           "Do you look forward to coming to school more when it is a day with PWC programs?",
                                                                                           "Do you / did you feel more motivated to come to school on a day that you met with a PWC worker?"],
}



# English to Spanish Mapping
EN_SP_MAPPING = {"Student's Name": "Nombre", "School": "Escuela", "Grade": "Grado",
                 
                 "Please tell us if you think your PWC program helped you in any of these areas: [I like going to school more.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Me gusta más ir a la escuela.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I learned new ways to take care of myself.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Aprendí nuevas formas de cuidarme.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I feel sad or mad less often.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Me siento triste, incómodo o enojado con menos frecuencia.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [When I feel sad or mad, I can better handle my big feelings.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Cuando me siento triste o enojado, puedo manejar mejor mis emociones.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [There are adults at my school who I can trust and ask for help.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Hay adultos en mi escuela en los que puedo confiar y pedir ayuda.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I get along better with kids at school.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Me llevo mejor con mis compañeros de escuela.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I am more confident and positive about myself.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Me siento más confiado y positivo conmigo mismo.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I get along better with my teachers.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Me llevo mejor con mis profesores.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I found new things I like to do.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Encontré nuevas cosas que disfruto hacer.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I found new things I like about myself.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Encontré nuevas cosas sobre mí que me gustan.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I know better how to ask for help when I need it.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Aprendí mejores formas de pedir ayuda cuando la necesito.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I am better at sharing my feelings.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [12. Soy mejor compartiendo mis sentimientos.]",
                 "Please tell us if you think your PWC program helped you in any of these areas: [I am happier.]": "Por favor, dinos si piensas que tu programa de PWC te ayudó en alguna de estas áreas durante tu año escolar: [Soy más feliz]",
                 
                 "Thinking about this school year, to what extent do you agree with the following statements? [There is an adult/adults at my school that I can turn to for support or help.]": "Pensando en el año escolar, en qué medida estás de acuerdo con la siguiente pregunta? [Hay adultos en mi escuela a los que pied acudir si necesito]",
                 "Thinking about this school year, to what extent do you agree with the following statements? [I feel connected to other students.]": "Pensando en el año escolar, en qué medida estás de acuerdo con la siguiente pregunta? [Me siento conectado con otros estudiantes]",
                 "Thinking about this school year, to what extent do you agree with the following statements? [I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school.]": "Pensando en el año escolar, en qué medida estás de acuerdo con la siguiente pregunta? [Mi identidad, de donde vengo y lo que puedo hacer  es bienvenidos/ bien recibido en mi escuela]",
                 "Thinking about this school year, to what extent do you agree with the following statements? [Adults who work at my school encourage students to have conversations around race, racism and social justice.]": "Pensando en el año escolar, en qué medida estás de acuerdo con la siguiente pregunta? [Adultos en mi escuela motivan los estudiantes a hablar de raza, racismo y justicia social]",
                 
                 "Please think about if PWC helped you grow or change this year.  Did you... [Learn how to better manage how I act when I have strong emotions]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Aprendí cómo manejarme mejor ante fuertes emociones]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Learn how to better advocate for myself and ask for help]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Aprendí a defenderme mejor y a preguntar x ayuda/asistencia]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Learn how to better share what I am thinking and feeling]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Aprendí a compartir mis pensamientos]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Learn how to make better decisions]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Aprendí a tomar mejores decisiones]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Feel sad or mad less often]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Me siento triste o incómodo con menos frecuencia]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Feel more confident and positive about myself]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Me siento más seguro y confiando de mi mismo]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Feel happier]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Me siento más feliz que antes]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Improve my relationships with other students]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [He mejorado mi relación con otros estudiantes]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Improve my relationships with teachers]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [He mejorado mi relación con los profesores]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Improve my relationships with my family]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [He mejorado mi relación con mi familia]",
                 "Please think about if PWC helped you grow or change this year.  Did you... [Improve my academic performance]": "Por favor piensa en que medida el programa PWC te ayudó a crecer o cambiar este año. [Mejoré mi rendimiento académico]",

                 "Did you feel happier about going to school on the days when you got to see your PWC social worker?": "¿Te sentiste más feliz de ir a la escuela en los días que viste a tu trabajador social de PWC?"
                 }


ANSWER_MAPPING = {
    "sí": "Yes",
    "si": "Yes",
    "no": "No",
    "tal vez": "Maybe",
    "sí, me sentí más feliz": "Yes, I felt happier",
    "si, me sentí más feliz": "Yes, I felt happier",
    "no, me sentí igual": "No, I felt the same",
    # Add other mappings as needed (and optionally English for idempotence)
}


import re
import unicodedata
from rapidfuzz import process

def normalize(text):
    """Lowercase, remove punctuation/extra spaces, normalize unicode."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def build_lookup(mapping):
    """Recursively build normalized lookup {variant: canonical} from mapping dict."""
    lookup = {}

    def _add_variants(d):
        for canon, val in d.items():
            # If val is a dict with 'variations', add each variation
            if isinstance(val, dict) and "variations" in val:
                for v in val["variations"]:
                    lookup[normalize(v)] = canon
                continue  # No need to process further, go to next item

            # If val is a nested dict, recurse
            if isinstance(val, dict):
                _add_variants(val)
                continue

            # If val is a direct mapping, add normalized canon
            lookup[normalize(canon)] = val if isinstance(val, str) else canon

    _add_variants(mapping)
    return lookup


def map_column(raw_col, lookup, fuzzy_suggest=True, threshold=87):
    """Return (canonical, reason) or (None, suggestions) for unmapped cols."""
    norm = normalize(raw_col)
    if norm in lookup:
        return lookup[norm], 'exact/variant'
    if fuzzy_suggest:
        # Suggest possible canonical forms for manual review
        choices = list(lookup.keys())
        suggestions = process.extract(norm, choices, limit=3, score_cutoff=threshold)
        if suggestions:
            # suggestions is a list of (match_string, score, index)
            return None, [(match_str, score) for match_str, score, _ in suggestions]
    return None, []


def audit_and_clean_columns(columns, lookup):
    """Return mapping and suggestions for review (no auto-fuzzy assignments)."""
    results = {}
    for col in columns:
        mapped, reason = map_column(col, lookup)
        if mapped:
            results[col] = {'canonical': mapped, 'reason': reason}
        else:
            results[col] = {'canonical': None, 'suggestions': reason}
    return results

# Example usage in your script:
if __name__ == "__main__":
    from question_mappings import YOUNGER_QUESTION_MAPPING

    lookup = build_lookup(YOUNGER_QUESTION_MAPPING)

    # Example list of columns from your data
    columns = [
        "I feel connected to other students.",
        "There is an adult/adults at my school that I can turn to for support or help.",
        "I feld conneted to other students",  # Typo, to test suggestion
        "Adults who work at my school encourage students to have conversations around race, racism and social justice."
    ]
    results = audit_and_clean_columns(columns, lookup)
    for col, res in results.items():
        print(f"Raw: {col}")
        if res['canonical']:
            print(f"  → Canonical: {res['canonical']} [{res['reason']}]")
        else:
            print(f"  → No direct match. Suggestions:")
            for sug, score in res['suggestions']:
                print(f"      - {sug} ({score:.0f}%)")
                


QCON_MAP = {
    "Adults at my school encourage students to share and be proud of who we are, where we come from, and what we can do; and to show respect for other students (who they are, where they come from, and what they can do)": "I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school.",
    "I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school.": "I feel like my identity – who I am, where I come from, and what I can do – is welcomed at my school.",
    "Adults at my school talk with students about race and things happening in the world.": "Adults at my school talk with students about race, racism, and things happening in the world.",
    "Adults at my school talk with students about race, racism, and things happening in the world.": "Adults at my school talk with students about race, racism, and things happening in the world.",
    "A space to honestly share what I am feeling or thinking": "A space to honestly share what I am feeling or thinking",
    "Adults from Partnership with Children have provided or helped me this year with:": "Adults from Partnership with Children have provided or helped me this year with:",
    "Adults who work at my school encourage students to express and take pride in their full identities and to respect each other’s identities": "Adults who work at my school encourage students to express and take pride in their full identities and to respect each other’s identities",
    "Adults who work at my school encourage students to have conversations about race, racism and social justice": "Adults who work at my school encourage students to have conversations about race, racism, and social justice",
    "Adults who work at my school encourage students to have conversations around race and social justice.": "Adults who work at my school encourage students to have conversations about race, racism, and social justice",
    "Adults who work at my school encourage students to have conversations around race, racism and social justice.": "Adults who work at my school encourage students to have conversations about race, racism, and social justice",
    "Alone / Lonely": "Alone/Lonely",
    "Alone/Lonely": "Alone/Lonely",
    "Lonely": "Alone/Lonely",
    "Angry / Mad": "Angry/Mad",
    "Mad/Angry": "Angry/Mad",
    "Mad / Angry": "Angry/Mad",
    "Angry/Mad": "Angry/Mad",
    "Anxious": "Anxious",
    "Apathetic/Disinterested": "Apathetic/Disinterested",
    "Appreciated": "Appreciated/Cared about",
    "Appreciated/Cared about": "Appreciated/Cared about",
    "Cared about / like others care about me": "Cared about / like others care about me",
    "Creative": "Creative",
    "Feel more creative": "Creative",
    "Did not have a lot of feelings": "Did not have a lot of feelings",
    "Did you feel happier about going to school on the days when you got to see your PWC social worker?": "Did you feel happier about going to school on the days when you got to see your PWC social worker?",
    "Discouraged": "Discouraged",
    "Found new things I like about myself": "I found new things I like about myself.",
    "Found new things I like to do": "I found new things I like about myself.",
    "I found new things I like about myself.": "I found new things I like about myself.",
    "Depressed": "Depressed",
    "Feel happier": "Feel happier",
    "Feel more confident and positive about myself": "Feel more confident and positive about myself",
    "Feel sad or mad less often": "Feel sad or mad less often",
    "Frustrated": "Frustrated",
    "Getting internet access so I could log into remote school": "Getting internet access so I could log into remote school",
    "Happy": "Happy",
    "Hopeful": "Hopeful",
    "Help dealing with and managing my emotions": "Help dealing with and managing my emotions",
    "Help for my family with obtaining food/groceries": "Help for my family with obtaining food/groceries",
    "Help staying motivated in school": "Help staying motivated in school",
    "Motivated": "Help staying motivated in school",
    "Unmotivated": "Help staying motivated in school",
    "Helpless": "Helpless",
    "I feel connected to other students.": "I feel connected to other students",
    "I felt connected to my peers.": "I feel connected to other students",
    "I feel sad or mad less often.": "I feel sad or mad less often",
    "Improve my academic performance": "Improve my academic performance",
    "Make academic gains": "Improve my academic performance",
    "Improve my relationships / relationship skills with my peers": "Improve my relationships with other students",
    "Improve my relationships with other students": "Improve my relationships with other students",
    "Improve my relationships with my family": "Improve my relationships with my family",
    "Improve my relationships with teachers": "Improve my relationships with teachers",
    "Improve my self-esteem": "Improve my self-esteem",
    "Interested": "Interested",
    "I am happier.": "I am happier",
    "I am happier": "I am happier",
    "I am better at sharing my feelings.": "I am better at sharing what I’m feeling or thinking",
    "I am better at sharing what I’m feeling or thinking": "I am better at sharing what I’m feeling or thinking",
    "I know better how to ask for help when I need it.": "I know better how to ask for help when I need it",
    "I know better how to ask for help when I need it": "I know better how to ask for help when I need it",
    "I learned new ways to take care of myself.": "I learned new ways to take care of myself",
    "Learned new ways to take care of myself": "I learned new ways to take care of myself",
    "Learn how to better advocate for myself and ask for help": "Learn how to better advocate for myself and ask for help",
    "Learn how to better advocate for myself or ask for help when needed": "Learn how to better advocate for myself and ask for help",
    "Support in advocating for myself and asking for help when needed": "Learn how to better advocate for myself and ask for help",
    "Can better control my behavior when I feel unhappy or frustrated": "When I feel sad or mad, I can better handle my big feelings.",
    "When I feel sad or mad, I can better handle my big feelings.": "When I feel sad or mad, I can better handle my big feelings.",
    "Can better deal with my emotions (how I feel)": "Can better deal with my emotions (how I feel)",
    "Can better deal with my emotions": "Can better deal with my emotions (how I feel)",
    "Learn how to better control my behavior when feeling strong emotions": "Learn how to better control my behavior when feeling strong emotions",
    "Learn how to better manage how I act when I have strong emotions": "Learn how to better control my behavior when feeling strong emotions",
    "Learn how to better share what I am thinking and feeling": "Learn how to better share what I am thinking and feeling",
    "Learn how to share what I am thinking and feeling": "Learn how to better share what I am thinking and feeling",
    "Learn how to make better decisions": "Learn how to make better decisions",
    "Learn how to process my emotions so I feel better": "Learn how to process my emotions so I feel better",
    "Learn new ways to take care of myself": "Learn new ways to take care of myself",
    "Not caring about anything": "Not caring about anything",
    "Opportunities to interact positively with my peers": "Opportunities to interact positively with my peers",
    "Other": "Other",
    "Overwhelmed": "Overwhelmed",
    "Sad": "Sad",
    "Scared": "Scared",
    "Successfully navigate difficult personal or family events": "Successfully navigate difficult personal or family events",
    "Learned how to get along better with my family": "Learned how to get along better with my family",
    "Learned how to get along better with teachers": "I get along better with my teachers",
    "I get along better with my teachers.": "I get along better with my teachers",
    "Learned how to get along better with friends": "I get along better with kids at school.",
    "I get along better with kids at school.": "I get along better with kids at school.",
    "Support with academic challenges": "Support with academic challenges",
    "Support with family issues": "Support with family issues",
    "Support with personal challenges in my life": "Support with personal challenges in my life",
    "Support with remote learning technology or issues (i.e. laptops, tablets, logging in)": "Support with remote learning technology or issues (i.e. laptops, tablets, logging in)",
    "Supportive relationships with adults who care about me": "Supportive relationships with adults who care about me",
    "Thankful": "Thankful",
    "There are adults/grown-ups at my school who I can ask for help.": "There are adults at my school who I can trust and ask for help.",
    "There are adults at my school who I can trust and ask for help.": "There are adults at my school who I can trust and ask for help.",
    "There are one or more adults at my school that I can turn to for support or help.": "There are adults at my school who I can trust and ask for help.",
    "There are adults at my school I can turn to for support or help.": "There are adults at my school who I can trust and ask for help.",
    "There are adults at my school that I can turn to for support or help.": "There are adults at my school who I can trust and ask for help.",
    "Worried": "Worried",
}


RESCON_MAPPING = {
    "Agree": "Yes",
    "Strongly Agree": "Yes",      # Optional
    "Neither Agree Nor Disagree": "Maybe",
    "Neither": "Maybe",
    "Disagree": "No",
    "Strongly Disagree": "No",    # Optional
    "Yes": "Yes",
    "Maybe": "Maybe",
    "No": "No",
    "A lot of the time": "A lot of the time",
    "Sometimes": "Sometimes",
    "Not at all": "Not at all",
    "All the time": "All the time",
}