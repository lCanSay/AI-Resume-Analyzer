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

    skills_keywords = [
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "ruby", "php", "typescript",
    "go", "swift", "kotlin", "r", "scala",

    # Web Development
    "html", "css", "javascript", "typescript", "react", "angular", "vue", "django", "flask",
    "node.js", "express.js", "next.js", "fastapi",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "firebase",

    # Cloud Technologies
    "aws", "amazon web services", "azure", "google cloud platform", "gcp",

    # DevOps and CI/CD
    "docker", "kubernetes", "jenkins", "gitlab", "github", "terraform",

    # Data Science and Analytics
    "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", "pytorch",
    "power bi", "tableau", "excel", "hadoop", "spark",

    # UI/UX and Design
    "figma", "sketch", "adobe xd", "photoshop", "illustrator", "invision", "wireframing", "prototyping", "ui/ux design",

    # Testing
    "selenium", "cypress", "pytest", "unittest", "postman",

    # Project Management / Collaboration
    "jira", "trello", "confluence", "monday.com",

    # Others
    "git", "rest api", "graphql", "agile", "scrum", "linux", "bash", "api development", "microservices"
]

    skills = []
    text_lower = text.lower()
    for skill in skills_keywords:
        if skill in text_lower:
            skills.append(skill)
    skills = list(set(skills))

    
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
            capture_education = False

        if any(keyword in line_lower for keyword in education_keywords):
            capture_education = True

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
