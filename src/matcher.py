
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_reader import read_resume
from text_cleaner import clean_text

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RESUME_DIR = BASE_DIR / "resumes"
JD_FILE = BASE_DIR / "data" / "job_description.txt"


def match_resumes():

    # Read job description
    job_description = JD_FILE.read_text(encoding="utf-8")
    job_description = clean_text(job_description)

    resume_files = list(RESUME_DIR.glob("*.pdf"))
    resume_files += list(RESUME_DIR.glob("*.docx"))

    if not resume_files:
        print("No PDF or DOCX resumes found!")
        return

    resume_texts = []
    valid_files = []

    # Extract resume text
    for file in resume_files:
        text = read_resume(file)

        if text.strip():
            resume_texts.append(clean_text(text))
            valid_files.append(file)

    if not valid_files:
        print("No readable resume text found!")
        return

    # Combine job description and resume texts
    documents = [job_description] + resume_texts

    # Convert text into numerical vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Calculate similarity scores
    scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    # Rank resumes
    results = []

    for file, score in zip(valid_files, scores):
        percentage = round(score * 100, 2)
        results.append((file.name, percentage))

    results.sort(key=lambda item: item[1], reverse=True)

    # Display results
    print("\n===== RESUME SCREENING RESULTS =====")

    for rank, (name, score) in enumerate(results, start=1):
        print(f"{rank}. {name} - {score}% Match")

    print("\nResume matching completed!")


if __name__ == "__main__":
    match_resumes()
