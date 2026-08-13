from app.utils.constants import SKILL_KEYWORDS, EXPECTED_SECTIONS, SKILL_SYNONYMS


def find_matched_and_missing_keywords(resume_text):
    """
    Compares resume text against the master skill keyword list.
    A keyword is considered matched if either:
      - the exact keyword appears in the text, OR
      - one of its known synonyms/abbreviations appears in the text
    Returns two lists: matched keywords, missing keywords.
    """
    if not resume_text:
        return [], SKILL_KEYWORDS

    text_lower = resume_text.lower()

    matched = []
    missing = []

    for keyword in SKILL_KEYWORDS:
        keyword_lower = keyword.lower()
        found = keyword_lower in text_lower

        # Check synonyms/abbreviations if direct match failed
        if not found and keyword_lower in SKILL_SYNONYMS:
            for synonym in SKILL_SYNONYMS[keyword_lower]:
                if synonym.lower() in text_lower:
                    found = True
                    break

        if found:
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