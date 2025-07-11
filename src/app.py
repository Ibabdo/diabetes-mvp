import streamlit as st
import pandas as pd
from advice_engine import get_advice
from report_generator import generate_report
import logging

# Setup
logging.basicConfig(level=logging.INFO)
st.set_page_config(page_title="Diabetes Prevention", layout="wide")

# Session state
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'consent' not in st.session_state:
    st.session_state.consent = False

# Consent flow
if not st.session_state.consent:
    st.title("Data Consent")
    if st.checkbox("I consent to anonymous data storage for diabetes prevention"):
        st.session_state.consent = True
        st.experimental_rerun()
    else:
        st.warning("Consent required to proceed")
        st.stop()

# Main UI
# Find the form section (around line 20-30)
# REPLACE the existing form with:
with st.form("health_form"):
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.patient_data['name'] = st.text_input("Full Name")
        st.session_state.patient_data['age'] = st.number_input("Age", 18, 100, 45)
        st.session_state.patient_data['weight'] = st.number_input("Weight (kg)", 30, 300, 70)
        st.session_state.patient_data['bp'] = st.text_input("Blood Pressure (e.g. 120/80)")
        
    with col2:
        st.session_state.patient_data['hba1c'] = st.slider("HbA1c (mmol/mol)", 20, 150, 50)
        st.session_state.patient_data['ethnicity'] = st.selectbox("Ethnicity", 
            ["White", "South Asian", "Black African", "Mixed/Other"])
        st.session_state.patient_data['activity'] = st.selectbox("Weekly Activity", 
            ["<30 mins", "30-150 mins", "150+ mins"])
    
    st.session_state.patient_data['meds'] = st.text_area("Current Medications")
    st.session_state.patient_data['smoker'] = st.checkbox("Current smoker")
    st.session_state.patient_data['family_history'] = st.checkbox("Family history of diabetes")
    
    if st.form_submit_button("Save Data"):
        st.success("Data saved!")

elif page == "Get Advice":
    st.title("Personalized Advice")
    if st.button("Generate Advice"):
        advice = get_advice(st.session_state.patient_data)
        st.info(advice)

elif page == "GP Report":
    st.title("Medical Report")
    if st.button("Generate PDF Report"):
        pdf_path = generate_report(st.session_state.patient_data)
        with open(pdf_path, "rb") as f:
            st.download_button("Download Report", f, "diabetes_report.pdf")
        st.success("Report generated!")
