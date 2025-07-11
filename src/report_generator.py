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
    # Add after existing code (around line 20)
    # Risk assessment section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Risk Assessment:", ln=True)
    pdf.set_font("Arial", size=12)
    
    risk_score = data.get('risk_score', 0)
    risk_level = "Low" if risk_score < 5 else "Moderate" if risk_score < 10 else "High"
    pdf.multi_cell(0, 8, f"10-year diabetes risk: {risk_score}% ({risk_level} risk)")
    
    # NICE compliance checklist
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "NICE Guideline Compliance", ln=True)
    
    checks = [
        "HbA1c tested within recommended timeframe",
        "Cardiovascular risk assessment completed",
        "Personalised advice delivered",
        "Referral to prevention services if indicated",
        "Follow-up scheduled"
    ]
    
    for check in checks:
        pdf.cell(0, 8, f"[ ] {check}", ln=True)
    
    # NHS resources
    pdf.set_font("Arial", 'I', 14)
    pdf.cell(0, 10, "NHS Support Resources:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, 
        "- Diabetes UK Helpline: 0345 123 2399\n"
        "- NHS Diabetes Prevention Programme\n"
        "- One You: www.nhs.uk/oneyou"
                  )
    # Save file
    pdf_path = "diabetes_report.pdf"
    pdf.output(pdf_path)
    return pdf_path
