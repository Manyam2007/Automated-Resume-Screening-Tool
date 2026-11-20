
import re


def clean_text(text):
    """
    Clean extracted resume text.
    """

    # Convert text to lowercase
    text = text.lower()

    # Remove unnecessary special characters
    text = re.sub(r'[^a-zA-Z0-9+#.\s]', ' ', text)

    # Remove extra spaces and line breaks
    text = re.sub(r'\s+', ' ', text)

    # Remove spaces at beginning and end
    text = text.strip()

    return text


# Test the function
if __name__ == "__main__":

    sample = """
    NAME: Rahul
    SKILLS: Python, Java, SQL
    EXPERIENCE: 2 Years
    """

    cleaned = clean_text(sample)

    print("Original Text:")
    print(sample)

    print("\nCleaned Text:")
    print(cleaned)
