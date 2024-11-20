def create_summary_pdf(text_file_path, pdf_file_path):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    
    # Use a built-in font (e.g., Helvetica or Times)
    pdf.set_font("Helvetica", size=12)
    
    with open(text_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, txt="Summary", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=12)
    for line in lines:
        pdf.multi_cell(0, 10, line)
    
    pdf.output(pdf_file_path)
    print(f"Summary PDF created at: {pdf_file_path}")
