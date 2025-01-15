import os
import re
from parsers.pdf_parser import extract_text_from_pdf  # Ensure this import works


def extract_keywords_from_description(description):
    # Extract keywords, excluding common stop words
    words = re.findall(r'\b\w+\b', description.lower())
    stop_words = set(["the", "and", "in", "to", "of", "a", "with", "for", "on", "as", "at", "by"])
    return [word for word in words if word not in stop_words]


def calculate_score(resume_text, job_description_keywords):
    # Count how many keywords are present in the resume
    matches = sum(
        1 for keyword in job_description_keywords
        if re.search(rf'\b{keyword}\b', resume_text, re.IGNORECASE)
    )
    # Calculate the percentage (out of 100)
    max_score = len(job_description_keywords)  # Total possible matches
    return (matches / max_score) * 100 if max_score > 0 else 0



def rank_resumes(resume_folder, job_description):
    job_keywords = extract_keywords_from_description(job_description)
    ranked_resumes = []  # List to store results

    for file in os.listdir(resume_folder):
        file_path = os.path.join(resume_folder, file)

        if file.endswith('.pdf'):
            try:
                text = extract_text_from_pdf(file_path)
            except Exception as e:
                print(f"Error processing {file}: {e}")
                text = None
        else:
            continue  # Skip non-PDF files

        if text:
            score = calculate_score(text, job_keywords)
            ranked_resumes.append({'filename': file, 'score': score})
        else:
            print(f"No text extracted from {file}")

    # Sort resumes by score in descending order
    return sorted(ranked_resumes, key=lambda x: x['score'], reverse=True)
