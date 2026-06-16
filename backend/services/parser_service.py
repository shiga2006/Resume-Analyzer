import pdfplumber
from docx import Document
import re


class ResumeParser:

    @staticmethod
    def extract_pdf_text(file):

        text = ""

        try:
            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

        except Exception as e:
            raise Exception(
                f"PDF Extraction Error: {str(e)}"
            )

        return text

    @staticmethod
    def extract_docx_text(file):

        text = ""

        try:

            document = Document(file)

            paragraphs = []

            for para in document.paragraphs:

                if para.text.strip():

                    paragraphs.append(
                        para.text.strip()
                    )

            text = "\n".join(paragraphs)

        except Exception as e:

            raise Exception(
                f"DOCX Extraction Error: {str(e)}"
            )

        return text

    @staticmethod
    def clean_text(text):

        if not text:
            return ""

        text = re.sub(
            r'\s+',
            ' ',
            text
        )

        text = re.sub(
            r'\n+',
            '\n',
            text
        )

        text = text.strip()

        return text

    @staticmethod
    def extract_text(file):

        filename = file.filename.lower()

        if filename.endswith(".pdf"):

            text = ResumeParser.extract_pdf_text(
                file
            )

        elif filename.endswith(".docx"):

            text = ResumeParser.extract_docx_text(
                file
            )

        else:

            raise Exception(
                "Unsupported file format. Use PDF or DOCX."
            )

        return ResumeParser.clean_text(text)