from docx import Document

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ' '.join([para.text for para in doc.paragraphs])
    return text