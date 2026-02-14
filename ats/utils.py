import re
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==============================
# 1️⃣ Extract Resume Text
# ==============================
def extract_resume_text(file_path):
    try:
        return extract_text(file_path)
    except Exception:
        return ""


# ==============================
# 2️⃣ Clean Text
# ==============================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)      # remove special chars
    text = re.sub(r'\s+', ' ', text)     # remove extra spaces
    return text.strip()


# ==============================
# 3️⃣ Important Skill Database
# ==============================
SKILLS_DB = [
    "python", "django", "flask",
    "html", "css", "javascript",
    "react", "sql", "mysql",
    "postgresql", "rest api",
    "machine learning", "data analysis",
    "git", "docker", "aws"
]


# ==============================
# 4️⃣ TF-IDF Similarity Score
# ==============================
def calculate_similarity(resume_text, job_description):
    documents = [resume_text, job_description]

    tfidf = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),      # unigram + bigram
        max_features=5000
    )

    tfidf_matrix = tfidf.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return float(similarity[0][0]) * 100


# ==============================
# 5️⃣ Skill Match Score
# ==============================
def calculate_skill_score(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    required_skills = []
    matched_skills = []

    for skill in SKILLS_DB:
        if skill in job_description:
            required_skills.append(skill)
            if skill in resume_text:
                matched_skills.append(skill)

    if not required_skills:
        return 0, [], []

    skill_score = (len(matched_skills) / len(required_skills)) * 100

    return skill_score, matched_skills, list(set(required_skills) - set(matched_skills))


# ==============================
# 6️⃣ Keyword Boost (Important Terms)
# ==============================
IMPORTANT_TERMS = [
    "experience",
    "project",
    "certification",
    "internship",
    "leadership",
    "team",
]


def keyword_boost(resume_text):
    boost = 0
    resume_text = resume_text.lower()

    for word in IMPORTANT_TERMS:
        if word in resume_text:
            boost += 2   # small bonus per important word

    return min(boost, 10)   # max boost 10%


# ==============================
# 7️⃣ Final Advanced ATS Score
# ==============================
def calculate_advanced_ats(resume_text, job_description):

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    # Similarity Score
    similarity_score = calculate_similarity(resume_text, job_description)

    # Skill Score
    skill_score, matched, missing = calculate_skill_score(
        resume_text, job_description
    )

    # Keyword Boost
    boost_score = keyword_boost(resume_text)

    # Final Weighted Score
    final_score = (
        (0.6 * similarity_score) +
        (0.3 * skill_score) +
        boost_score
    )

    final_score = round(min(final_score, 100), 2)

    return {
        "final_score": final_score,
        "similarity_score": round(similarity_score, 2),
        "skill_score": round(skill_score, 2),
        "boost_score": boost_score,
        "matched_skills": matched,
        "missing_skills": missing
    }
