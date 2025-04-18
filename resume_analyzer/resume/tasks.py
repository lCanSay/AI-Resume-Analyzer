from celery import shared_task
from .models import Resume
from .utils import extract_text_from_pdf, extract_text_from_docx, extract_resume_data

@shared_task
def parse_resume_file(resume_id):
    from time import sleep
    print(f"Started parsing resume ID: {resume_id}")
    try:
        resume = Resume.objects.get(id=resume_id)
        file = resume.file

        print(f"File path: {file.name}")
        ext = file.name.split('.')[-1].lower()
        
        if ext == 'pdf':
            text = extract_text_from_pdf(file)
        elif ext == 'docx':
            text = extract_text_from_docx(file)
        else:
            print("Unsupported format")
            return {"error": "Unsupported file format"}

        print("Extracted text length:", len(text))
        print("Extracted text:", text[:300])

        parsed_data = extract_resume_data(text)
        print("Parsed data:", parsed_data)

        resume.parsed_data = parsed_data
        resume.save()
        print(f"Resume {resume.id} parsed and saved.")
        return {"status": "parsed", "resume_id": resume.id}

    except Resume.DoesNotExist:
        print("Resume not found")
        return {"error": "Resume not found"}

