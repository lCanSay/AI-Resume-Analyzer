import fitz
import docx
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    file.seek(0)
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])



def extract_resume_data(text):
    doc = nlp(text)

    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

    phones = re.findall(r'\+?\d[\d\-\s\(\)]{9,}\d', text)
    phones = [phone for phone in phones if len(re.sub(r'\D', '', phone)) >= 10]

    skills_keywords = ["python", "java", "sql", "django", "react", "aws", "git"]
    skills = [token.text.lower() for token in doc if token.text.lower() in skills_keywords]
    
    experience_years = 0
    exp_patterns = re.findall(r'(\d+)\s*(\+)?\s*(years|year) of experience', text.lower())
    if exp_patterns:
        experience_years = max(int(match[0]) for match in exp_patterns)

    education = []
    education_keywords = ["bachelor", "master", "b.sc", "m.sc", "phd", "university", "college", "school", "degree"]
    stop_keywords = ["experience", "work experience", "professional experience"]

    capture_education = False
    for line in text.splitlines():
        line_lower = line.lower().strip()

        if any(word in line_lower for word in stop_keywords):
            capture_education = False  # stop capturing education once experience section starts

        if any(keyword in line_lower for keyword in education_keywords):
            capture_education = True  # start capturing education

        if capture_education and line.strip():
            education.append(line.strip())

    return {
        "emails": list(set(emails)),
        "phones": list(set(phones)),
        "skills": list(set(skills)),
        "education": education,
        "experience_years": experience_years,
        "word_count": len(text.split()),
    }
