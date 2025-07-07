from fpdf import FPDF

def generate_report(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Diabetes Prevention Report", ln=True, align='C')
    
    # Patient info
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Patient: {data.get('name', '')}", ln=True)
    pdf.cell(0, 10, f"HbA1c: {data.get('hba1c', '')} mmol/mol", ln=True)
    
    # Simple advice
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Clinical Recommendations:", ln=True)
    pdf.set_font("Arial", size=12)
    
    hba1c = data.get('hba1c', 0)
    if hba1c > 64:
        pdf.multi_cell(0, 8, "- Urgent GP referral required\n- Medication review needed")
    elif hba1c > 53:
        pdf.multi_cell(0, 8, "- Increase physical activity\n- Dietary modifications recommended")
    else:
        pdf.multi_cell(0, 8, "- Maintain healthy lifestyle\n- Annual monitoring sufficient")
    
    # Save file
    pdf_path = "diabetes_report.pdf"
    pdf.output(pdf_path)
    return pdf_path
