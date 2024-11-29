from fpdf import FPDF
import os

async def get_pdf(text: str):
    # Define the output directory for PDFs
    output_dir = os.getenv("PDF_OUTPUT_FOLDER", "pdf_outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Create a filename for the PDF
    pdf_filename = os.path.join(output_dir, "output.pdf")

    # Initialize FPDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split text into manageable chunks (e.g., lines)
    lines = text.split("\n")
    for line in lines:
        pdf.cell(0, 10, txt=line, ln=True)

    # Save the PDF
    pdf.output(pdf_filename)

    # Log or return the path for further use
    return pdf_filename
