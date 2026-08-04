from app.services.keyword import find_matched_and_missing_keywords, find_missing_sections
from app.utils.constants import MIN_WORD_COUNT, MAX_WORD_COUNT


def calculate_ats_score(resume_text):
    """
    Calculates an ATS-friendliness score (0-100) based on:
    - Keyword match percentage        (up to 60 points)
    - Section completeness            (up to 25 points)
    - Resume length health            (up to 15 points)

    Returns a dictionary with the full breakdown.
    """
    if not resume_text:
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "missing_sections": [],
            "word_count": 0,
            "feedback": ["Resume text could not be read. Please upload a valid file."]
        }

    matched_keywords, missing_keywords = find_matched_and_missing_keywords(resume_text)
    missing_sections = find_missing_sections(resume_text)
    word_count = len(resume_text.split())

    # ---- 1. Keyword score (max 60 points) ----
    total_keywords = len(matched_keywords) + len(missing_keywords)
    keyword_ratio = len(matched_keywords) / total_keywords if total_keywords else 0
    keyword_score = round(keyword_ratio * 60)

    # ---- 2. Section completeness score (max 25 points) ----
    total_sections = 7  # from EXPECTED_SECTIONS
    sections_present = total_sections - len(missing_sections)
    section_score = round((sections_present / total_sections) * 25)

    # ---- 3. Length health score (max 15 points) ----
    if MIN_WORD_COUNT <= word_count <= MAX_WORD_COUNT:
        length_score = 15
    elif word_count < MIN_WORD_COUNT:
        length_score = round((word_count / MIN_WORD_COUNT) * 15)
    else:
        # Penalize slightly for very long resumes
        length_score = 10

    total_score = keyword_score + section_score + length_score
    total_score = min(total_score, 100)  # safety cap

    # ---- Feedback messages ----
    feedback = []

    if keyword_ratio < 0.3:
        feedback.append("Your resume is missing many relevant skill keywords. Consider adding more industry-specific terms.")
    elif keyword_ratio < 0.6:
        feedback.append("Your resume has a moderate keyword match. Adding more relevant skills could improve your ATS score.")
    else:
        feedback.append("Great keyword coverage! Your resume includes a strong set of relevant terms.")

    if missing_sections:
        feedback.append(f"Consider adding these missing sections: {', '.join(missing_sections)}.")

    if word_count < MIN_WORD_COUNT:
        feedback.append("Your resume seems too short. Add more detail about your experience and projects.")
    elif word_count > MAX_WORD_COUNT:
        feedback.append("Your resume is quite long. Consider trimming it for better readability.")

    return {
        "score": total_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "missing_sections": missing_sections,
        "word_count": word_count,
        "feedback": feedback,
    }