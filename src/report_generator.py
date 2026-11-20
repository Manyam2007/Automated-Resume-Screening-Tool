
import csv
from pathlib import Path

from text_cleaner import clean_text
from resume_reader import read_resume
from skill_extractor import extract_skills
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
RESUME_DIR = BASE_DIR / "resumes"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

JD_FILE = DATA_DIR / "job_description.txt"
SKILLS_FILE = DATA_DIR / "required_skills.txt"


def generate_report():

    OUTPUT_DIR.mkdir(exist_ok=True)

    job_description = clean_text(
        JD_FILE.read_text(encoding="utf-8")
    )

    required_skills = [
        skill.strip().lower()
        for skill in SKILLS_FILE.read_text(encoding="utf-8").splitlines()
        if skill.strip()
    ]

    resume_files = list(RESUME_DIR.glob("*.pdf"))
    resume_files += list(RESUME_DIR.glob("*.docx"))

    if not resume_files:
        print("No resumes found!")
        return

    candidates = []

    for file in resume_files:
        text = read_resume(file)

        if not text.strip():
            continue

        cleaned_text = clean_text(text)

        candidate_skills = extract_skills(cleaned_text)

        matched = [
            skill for skill in required_skills
            if skill in candidate_skills
        ]

        missing = [
            skill for skill in required_skills
            if skill not in candidate_skills
        ]

        skill_score = (
            len(matched) / len(required_skills) * 100
            if required_skills else 0
        )

        candidates.append({
            "name": file.name,
            "text": cleaned_text,
            "matched": matched,
            "missing": missing,
            "skill_score": round(skill_score, 2)
        })

    if not candidates:
        print("No readable resumes found!")
        return

    documents = [job_description] + [
        candidate["text"] for candidate in candidates
    ]

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(
        matrix[0:1], matrix[1:]
    )[0]

    for candidate, score in zip(candidates, similarity_scores):
        candidate["similarity_score"] = round(float(score) * 100, 2)

        candidate["overall_score"] = round(
            0.5 * candidate["similarity_score"]
            + 0.5 * candidate["skill_score"],
            2
        )

    candidates.sort(
        key=lambda candidate: candidate["overall_score"],
        reverse=True
    )

    report_file = OUTPUT_DIR / "resume_screening_report.csv"

    with open(report_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Rank",
            "Resume Name",
            "Similarity Score",
            "Skill Match Score",
            "Overall Score",
            "Matched Skills",
            "Missing Skills"
        ])

        for rank, candidate in enumerate(candidates, start=1):
            writer.writerow([
                rank,
                candidate["name"],
                candidate["similarity_score"],
                candidate["skill_score"],
                candidate["overall_score"],
                ", ".join(candidate["matched"]),
                ", ".join(candidate["missing"])
            ])

    print("\n===== FINAL RESUME SCREENING REPORT =====")

    for rank, candidate in enumerate(candidates, start=1):
        print(f"\nRank: {rank}")
        print("Resume:", candidate["name"])
        print("Similarity:", candidate["similarity_score"], "%")
        print("Skill Match:", candidate["skill_score"], "%")
        print("Overall Score:", candidate["overall_score"], "%")

    print("\nCSV report saved at:", report_file)


if __name__ == "__main__":
    generate_report()
