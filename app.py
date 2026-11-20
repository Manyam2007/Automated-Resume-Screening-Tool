
import streamlit as st
import pandas as pd
import sys
import tempfile
import csv

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Project paths
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from resume_reader import read_resume
from text_cleaner import clean_text
from skill_extractor import extract_skills


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="AI Resume Screening Tool",
    page_icon="📄",
    layout="wide"
)


# ---------------- CUSTOM DASHBOARD DESIGN ----------------

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fc;
}

h1 {
    color: #172554;
    text-align: center;
    font-weight: bold;
}

h2, h3 {
    color: #1e3a8a;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
}

.stButton button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.title("📄 Automated Resume Screening Tool")

st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "AI-Assisted Resume Analysis and Candidate Ranking System"
    "</p>",
    unsafe_allow_html=True
)

st.divider()


# ---------------- SIDEBAR ----------------

st.sidebar.title("🎯 Navigation")

st.sidebar.info(
    "This application compares resumes with job descriptions "
    "using TF-IDF, Cosine Similarity and skill matching."
)

st.sidebar.markdown("### Project Features")

st.sidebar.write("📂 Resume Upload")
st.sidebar.write("🔍 Resume Analysis")
st.sidebar.write("🧠 Skill Extraction")
st.sidebar.write("📊 Candidate Ranking")
st.sidebar.write("📥 CSV Report")


# ---------------- INPUT SECTION ----------------

st.header("📝 Job Description")

job_description = st.text_area(
    "Paste the job description below:",
    height=180,
    placeholder="Enter job title, required skills and qualifications..."
)

st.header("📂 Upload Resumes")

uploaded_files = st.file_uploader(
    "Upload PDF or DOCX resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


# ---------------- SCREENING FUNCTION ----------------

if st.button("🚀 Screen Resumes"):

    if not job_description.strip():

        st.warning("Please enter a job description.")

    elif not uploaded_files:

        st.warning("Please upload at least one resume.")

    else:

        required_skills = extract_skills(job_description)

        if not required_skills:
            st.warning(
                "No recognized skills found. Add skills such as Python, "
                "Java, SQL or Machine Learning to the job description."
            )
            st.stop()

        candidates = []

        with st.spinner("Analyzing resumes..."):

            for uploaded_file in uploaded_files:

                suffix = Path(uploaded_file.name).suffix.lower()

                with tempfile.NamedTemporaryFile(
                    suffix=suffix,
                    delete=False
                ) as temp_file:

                    temp_file.write(uploaded_file.getvalue())
                    temp_path = Path(temp_file.name)

                try:
                    resume_text = read_resume(temp_path)
                finally:
                    temp_path.unlink(missing_ok=True)

                if not resume_text.strip():
                    continue

                cleaned_resume = clean_text(resume_text)
                cleaned_jd = clean_text(job_description)

                candidate_skills = extract_skills(resume_text)

                matched = [
                    skill for skill in required_skills
                    if skill in candidate_skills
                ]

                missing = [
                    skill for skill in required_skills
                    if skill not in candidate_skills
                ]

                skill_score = (
                    len(matched) / len(required_skills)
                ) * 100

                vectorizer = TfidfVectorizer()

                matrix = vectorizer.fit_transform([
                    cleaned_jd,
                    cleaned_resume
                ])

                similarity = cosine_similarity(
                    matrix[0:1],
                    matrix[1:]
                )[0][0] * 100

                overall = (
                    0.5 * similarity + 0.5 * skill_score
                )

                candidates.append({

                    "Resume": uploaded_file.name,

                    "Similarity Score": round(similarity, 2),

                    "Skill Match Score": round(skill_score, 2),

                    "Overall Score": round(overall, 2),

                    "Matched Skills": ", ".join(matched),

                    "Missing Skills": ", ".join(missing)

                })


        # ---------------- RESULTS SECTION ----------------

        if not candidates:

            st.error(
                "Unable to extract readable text from the uploaded resumes."
            )

        else:

            candidates.sort(
                key=lambda x: x["Overall Score"],
                reverse=True
            )

            st.success("Resume screening completed successfully!")

            st.divider()

            # Summary cards

            st.header("📊 Screening Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Resumes",
                len(candidates)
            )

            col2.metric(
                "Required Skills",
                len(required_skills)
            )

            col3.metric(
                "Highest Score",
                f"{candidates[0]['Overall Score']}%"
            )

            st.divider()

            # Candidate chart

            st.header("📈 Candidate Score Comparison")

            chart_data = pd.DataFrame(candidates)

            st.bar_chart(
                chart_data,
                x="Resume",
                y="Overall Score"
            )

            st.divider()

            # Candidate table

            st.header("🏆 Candidate Ranking")

            st.dataframe(
                chart_data,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # Detailed candidate information

            st.header("🔍 Candidate Skill Analysis")

            for rank, candidate in enumerate(candidates, start=1):

                with st.expander(
                    f"Rank {rank} - {candidate['Resume']}"
                ):

                    st.metric(
                        "Overall Score",
                        f"{candidate['Overall Score']}%"
                    )

                    st.write(
                        "**Similarity Score:**",
                        f"{candidate['Similarity Score']}%"
                    )

                    st.write(
                        "**Skill Match Score:**",
                        f"{candidate['Skill Match Score']}%"
                    )

                    st.write(
                        "**Matched Skills:**",
                        candidate["Matched Skills"] or "None"
                    )

                    st.write(
                        "**Missing Skills:**",
                        candidate["Missing Skills"] or "None"
                    )

            st.divider()

            # CSV download

            st.header("📥 Download Report")

            csv_data = chart_data.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Resume Screening Report",
                data=csv_data,
                file_name="resume_screening_report.csv",
                mime="text/csv"
            )

            st.info(
                "Note: Scores measure text similarity and listed skill "
                "coverage only. They do not prove actual candidate ability. "
                "Use human review and do not make hiring decisions solely "
                "from automated scores."
            )


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "Automated Resume Screening Tool | Python | Machine Learning | NLP"
    "</p>",
    unsafe_allow_html=True
)
