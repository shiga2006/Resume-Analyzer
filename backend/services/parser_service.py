import re
import pdfplumber
from docx import Document

class ResumeParser:
    """PDF/DOCX Resume parsing engine with regex text extraction and section segmentation."""

    @staticmethod
    def extract_pdf_text(file_stream) -> str:
        text = ""
        try:
            with pdfplumber.open(file_stream) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"PDF Extraction Error: {str(e)}")
        return text

    @staticmethod
    def extract_docx_text(file_stream) -> str:
        text = ""
        try:
            document = Document(file_stream)
            paragraphs = [para.text.strip() for para in document.paragraphs if para.text.strip()]
            text = "\n".join(paragraphs)
        except Exception as e:
            raise Exception(f"DOCX Extraction Error: {str(e)}")
        return text

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Remove unusual unicode control characters while preserving lines
        text = re.sub(r'[\r\t\f\v]', ' ', text)
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n', text)
        return text.strip()

    @staticmethod
    def extract_contact_info(text: str) -> dict:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        phone_pattern = r'\(?\+?\d{1,4}\)?[\s.-]?\(?\d{2,5}\)?[\s.-]?\d{3,5}[\s.-]?\d{3,5}'
        linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+'
        github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+'

        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        linkedins = re.findall(linkedin_pattern, text)
        githubs = re.findall(github_pattern, text)

        return {
            "email": emails[0] if emails else None,
            "phone": phones[0] if phones else None,
            "linkedin": linkedins[0] if linkedins else None,
            "github": githubs[0] if githubs else None
        }

    @staticmethod
    def segment_sections(text: str) -> dict:
        """Categorize raw text into standard resume sections."""
        headers = {
            "summary": r"(?:summary|objective|profile|about me)",
            "skills": r"(?:skills|technical skills|core competencies|technologies|tools)",
            "experience": r"(?:experience|work experience|employment history|professional experience)",
            "education": r"(?:education|academic background|qualifications)",
            "projects": r"(?:projects|personal projects|key projects)",
            "certifications": r"(?:certifications|certificates|licenses|courses)"
        }

        sections = {key: "" for key in headers.keys()}
        sections["other"] = ""

        lines = text.split("\n")
        current_section = "other"

        for line in lines:
            line_clean = line.strip().lower()
            header_matched = False
            for sec_name, pattern in headers.items():
                if re.match(rf"^{pattern}[\:\s]*$", line_clean) or line_clean.startswith(sec_name):
                    current_section = sec_name
                    header_matched = True
                    break

            if not header_matched:
                sections[current_section] += line + "\n"

        return {k: v.strip() for k, v in sections.items() if v.strip()}

    @classmethod
    def parse_file(cls, file_bytes: bytes, filename: str) -> dict:
        import io
        file_stream = io.BytesIO(file_bytes)
        filename_lower = filename.lower()

        if filename_lower.endswith(".pdf"):
            raw_text = cls.extract_pdf_text(file_stream)
        elif filename_lower.endswith(".docx"):
            raw_text = cls.extract_docx_text(file_stream)
        else:
            raise ValueError("Unsupported file format. Please upload PDF or DOCX.")

        cleaned_text = cls.clean_text(raw_text)
        contact_info = cls.extract_contact_info(cleaned_text)
        sections = cls.segment_sections(cleaned_text)

        word_count = len(cleaned_text.split())

        return {
            "raw_text": cleaned_text,
            "word_count": word_count,
            "contact_info": contact_info,
            "sections": sections
        }