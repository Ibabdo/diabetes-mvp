from fpdf import FPDF
from datetime import date

def generate_report(data, advice, risk_score):
    pdf = FPDF()
    pdf.add_page()
    
    # NHS Header
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 94, 184)  # NHS blue
    pdf.cell(0, 10, "NHS Diabetes Prevention Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Generated: {date.today().strftime('%d/%m/%Y')}", ln=True, align='C')
    pdf.line(10, 30, 200, 30)
    
    # Patient Details
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 15, "Patient Information", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(40, 8, "Name:", ln=0)
    pdf.cell(0, 8, data.get('name', ''), ln=True)
    pdf.cell(40, 8, "Date of Birth:", ln=0)
    pdf.cell(0, 8, f"Age: {data.get('age', '')}", ln=True)
    pdf.cell(40, 8, "Ethnic Group:", ln=0)
    pdf.cell(0, 8, data.get('ethnicity', ''), ln=True)
    
    # Clinical Summary
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Clinical Summary", ln=True)
    pdf.set_font("Arial", size=12)
    
    # Risk Score
    risk_level = "High" if risk_score >= 20 else "Medium" if risk_score >= 10 else "Low"
    pdf.cell(60, 8, "10-Year Diabetes Risk:", ln=0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, f"{risk_score}% ({risk_level} Risk)", ln=True)
    pdf.set_font("Arial", size=12)
    
    # Key Metrics Table
    pdf.cell(0, 8, "Clinical Parameters:", ln=True)
    col_width = 45
    pdf.cell(col_width, 8, "HbA1c", border=1)
    pdf.cell(col_width, 8, "Blood Pressure", border=1)
    pdf.cell(col_width, 8, "Weight", border=1)
    pdf.cell(col_width, 8, "Activity", border=1, ln=True)
    
    pdf.cell(col_width, 8, f"{data.get('hba1c', '')} mmol/mol", border=1)
    pdf.cell(col_width, 8, data.get('bp', ''), border=1)
    pdf.cell(col_width, 8, f"{data.get('weight', '')} kg", border=1)
    pdf.cell(col_width, 8, data.get('activity', ''), border=1, ln=True)
    
    # Recommendations
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Clinical Recommendations", ln=True)
    pdf.set_font("Arial", size=12)
    
    for i, rec in enumerate(advice["recommendations"]):
        pdf.cell(10, 8, f"{i+1}.", ln=0)
        pdf.multi_cell(0, 8, rec)
    
    # NHS Resources
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "NHS Support Resources", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, """
    - NHS Diabetes Prevention Programme: https://preventing-diabetes.co.uk/
    - Diabetes UK Helpline: 0345 123 2399
    - NHS Weight Management Services
    - Active 10 Walking Tracker App
    """)
    
    # Save file
    pdf_path = "nhs_diabetes_report.pdf"
    pdf.output(pdf_path)
    return pdf_path
