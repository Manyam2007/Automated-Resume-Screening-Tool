
from pathlib import Path

from resume_reader import read_resume
from skill_extractor import extract_skills

# Get project folder
BASE_DIR = Path(__file__).resolve().parent.parent

RESUME_DIR = BASE_DIR / "resumes"
SKILLS_FILE = BASE_DIR / "data" / "required_skills.txt"


def match_skills():

    # Read required skills
    required_skills = [
        skill.strip().lower()
        for skill in SKILLS_FILE.read_text(encoding="utf-8").splitlines()
        if skill.strip()
    ]

    # Find PDF and DOCX resumes
    resume_files = list(RESUME_DIR.glob("*.pdf"))
    resume_files += list(RESUME_DIR.glob("*.docx"))

    if not resume_files:
        print("No resumes found!")
        return

    print("\n===== SKILL MATCHING RESULTS =====")

    for file in resume_files:

        # Extract resume text
        resume_text = read_resume(file)

        # Extract candidate skills
        candidate_skills = extract_skills(resume_text)

        # Find matching and missing skills
        matched = [
            skill for skill in required_skills
            if skill in candidate_skills
        ]

        missing = [
            skill for skill in required_skills
            if skill not in candidate_skills
        ]

        # Calculate skill coverage
        percentage = (len(matched) / len(required_skills)) * 100

        print("\nResume:", file.name)
        print("Matched Skills:", matched)
        print("Missing Skills:", missing)
        print("Skill Match:", round(percentage, 2), "%")


if __name__ == "__main__":
    match_skills()
