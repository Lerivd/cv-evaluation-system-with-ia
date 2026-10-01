import PyPDF2
from io import BytesIO

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_file) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
            full_text = []

            for i, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    full_text.append(f"\n--- PAGE {i} ---\n")
                    full_text.append(page_text.strip() + "\n")
            
            result = "".join(full_text).strip()

            if not result:
                return "Error: The PDF appears to be empty or contains only images."
            
            return result
        except Exception as e:
            return f"Error processing PDF file: {str(e)}"

def extraer_texto_pdf(archivo_pdf):
    return PDFProcessor.extract_text(archivo_pdf)