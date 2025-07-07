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
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data Input", "Get Advice", "GP Report"])

if page == "Data Input":
    st.title("Your Health Data")
    with st.form("health_form"):
        st.session_state.patient_data['name'] = st.text_input("Full Name")
        st.session_state.patient_data['hba1c'] = st.slider("HbA1c (mmol/mol)", 20, 150, 50)
        st.session_state.patient_data['weight'] = st.number_input("Weight (kg)", 30, 300, 70)
        st.session_state.patient_data['bp'] = st.text_input("Blood Pressure (e.g., 120/80)")
        st.session_state.patient_data['activity'] = st.selectbox("Activity Level", ["Low", "Medium", "High"])
        st.session_state.patient_data['meds'] = st.text_area("Current Medications")
        
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
