
import re


# List of technical skills
SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "sql",
    "mysql",
    "mongodb",
    "excel",
    "power bi",
    "tableau",
    "pandas",
    "numpy",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "data analysis",
    "data science",
    "flask",
    "django",
    "fastapi",
    "react",
    "node.js",
    "git",
    "github",
    "aws",
    "azure",
    "docker"
]


def extract_skills(text):

    # Convert text to lowercase
    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        # Match complete skill names
        pattern = r'(?<![a-z0-9])' + re.escape(skill) + r'(?![a-z0-9])'

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# Test the function
if __name__ == "__main__":

    sample_resume = """
    I know Python, Java, SQL and HTML.
    I have experience in Machine Learning.
    I have also worked with Pandas and NumPy.
    """

    skills = extract_skills(sample_resume)

    print("Skills Found in Resume:")

    for skill in skills:
        print("-", skill)

    print("\nTotal Skills:", len(skills))
