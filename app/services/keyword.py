from app.utils.constants import SKILL_KEYWORDS, EXPECTED_SECTIONS


def find_matched_and_missing_keywords(resume_text):
    """
    Compares resume text against the master skill keyword list.
    Returns two lists: matched keywords, missing keywords.
    """
    if not resume_text:
        return [], SKILL_KEYWORDS

    text_lower = resume_text.lower()

    matched = []
    missing = []

    for keyword in SKILL_KEYWORDS:
        if keyword.lower() in text_lower:
            matched.append(keyword)
        else:
            missing.append(keyword)

    return matched, missing


def find_missing_sections(resume_text):
    """
    Checks which standard resume sections are missing from the text.
    """
    if not resume_text:
        return EXPECTED_SECTIONS

    text_lower = resume_text.lower()
    missing_sections = [
        section for section in EXPECTED_SECTIONS
        if section not in text_lower
    ]
    return missing_sections