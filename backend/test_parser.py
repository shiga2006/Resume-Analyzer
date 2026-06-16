from services.parser_service import ResumeParser

with open(r"C:\Users\DELL-7420\Downloads\Shivashiga_A.M_JP.pdf", "rb") as file:

    text = ResumeParser.extract_pdf_text(
        file
    )

    print(text[:1000])