# Common technical & soft skills that ATS systems typically scan for.
# This is a general-purpose list — will be replaceable by job-description-based
# keywords in the future upgrade.
SKILL_KEYWORDS = [
    # Programming & Technical
    "python", "java", "javascript", "c++", "c#", "sql", "html", "css",
    "react", "node.js", "flask", "django", "git", "github", "api",
    "machine learning", "data analysis", "data structures", "algorithms",
    "object oriented programming", "database", "cloud", "aws", "docker",

    # Soft / Professional Skills
    "communication", "leadership", "teamwork", "problem solving",
    "project management", "time management", "critical thinking",
    "collaboration", "adaptability", "analytical",

    # Tools
    "microsoft office", "excel", "powerpoint", "word", "figma",
    "photoshop", "jira", "slack",
]

# Section headers a well-structured resume should typically contain
EXPECTED_SECTIONS = [
    "experience", "education", "skills", "projects",
    "summary", "objective", "certifications",
]

# Strong action verbs that improve resume impact (used for suggestions, not scoring yet)
ACTION_VERBS = [
    "developed", "designed", "created", "managed", "led", "built",
    "implemented", "achieved", "improved", "optimized", "analyzed",
    "coordinated", "delivered", "launched", "increased", "reduced",
]

# Minimum/maximum word count considered "healthy" for an ATS-friendly resume
MIN_WORD_COUNT = 150
MAX_WORD_COUNT = 1000
# Maps a canonical skill keyword to its common abbreviations/alternate forms.
# If ANY of these alternate forms appear in the resume, the canonical keyword
# is considered "matched".
SKILL_SYNONYMS = {
    "object oriented programming": ["oop"],
    "machine learning": ["ml"],
    "javascript": ["js"],
    "artificial intelligence": ["ai"],
    "data structures": ["ds"],
    "database": ["db", "mysql", "postgresql", "mongodb", "sqlite"],
    "sql": ["mysql", "postgresql", "sqlite", "structured query language"],
    "microsoft office": ["ms office", "office365", "office 365"],
    "user interface": ["ui"],
    "user experience": ["ux"],
    "application programming interface": ["api"],
    "continuous integration": ["ci/cd", "ci cd"],
    "version control": ["git", "github", "gitlab"],
}