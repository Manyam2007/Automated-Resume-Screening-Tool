
import pdfplumber
from docx import Document
from pathlib import Path


def extract_pdf_text(file_path):
    """Extract text from a PDF resume."""

    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


def extract_docx_text(file_path):
    """Extract text from a DOCX resume."""

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def read_resume(file_path):
    """Read PDF or DOCX resume."""

    file_path = Path(file_path)

    if not file_path.exists():
        print("Error: File not found!")
        return ""

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    else:
        print("Unsupported file format!")
        return ""


# Test the program
if __name__ == "__main__":

    print("RESUME READER")

    resume_path = input("Enter resume file path: ")

    extracted_text = read_resume(resume_path)

    print("\nExtracted Resume Text:")
    print("----------------------")
    print(extracted_text)

    print("\nResume extraction completed!")
