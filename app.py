import os
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from utils.keyword_matching import calculate_score, rank_resumes


def main():
    job_keywords = ['Python', 'AWS', 'Docker', 'Kubernetes', 'CI/CD']
    resume_dir = './data'
    ranked_resumes = rank_resumes(resume_dir, job_keywords)

    print("Ranked Resumes: ")
    for resume, score in ranked_resumes:
        print(f"{resume}: {score}")


if __name__ == '__main__':
    main()
