import os
import re

def calculate_score(resume_text, job_description_keywords):
    score = 0
    for keyword in job_description_keywords:
        if re.search(rf'\b{keyword}\b', resume_text, re.IGNORECASE):
            score += 1
    return score

def rank_resumes(resume_folder, job_description_keywords):
    scores = list()
    for file in os.listdir(resume_folder):
        file_path = os.path.join(resume_folder, file)
        if file.endswith('.pdf'):
            from parsers.pdf_parser import extract_text_from_pdf
            text = extract_text_from_pdf(file_path)
        elif file.endswith('.docx'):
            from parsers.docx_parser import extract_text_from_docx
            text = extract_text_from_docx(file_path)
        else:
            continue

        if text:
            score = calculate_score(text, job_description_keywords)
            scores.append((file, score))

    return sorted(scores, key=lambda x: x[1], reverse=True)