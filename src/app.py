import streamlit as st
import time
import logging
from advice_engine import generate_advice
from report_generator import generate_report
from clinical_rules import calculate_risk_score

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NHS color scheme
NHS_BLUE = "#005EB8"
NHS_DARK_BLUE = "#003087"

# App configuration
st.set_page_config(
    page_title="NHS Diabetes Prevention",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_nhs_styles():
    """Apply NHS branding to the app"""
    st.markdown(
        f"""
        <style>
            .main {{
                background-color: #f0f4f5;
            }}
            .sidebar .sidebar-content {{
                background-color: {NHS_DARK_BLUE} !important;
                color: white;
            }}
            h1, h2, h3 {{
                color: {NHS_BLUE};
            }}
            .stButton>button {{
                background-color: {NHS_BLUE} !important;
                color: white !important;
                border-radius: 4px;
                font-weight: bold;
            }}
            .stAlert {{
                border-left: 5px solid {NHS_BLUE};
            }}
            .risk-high {{
                color: #d5281b !important;
                font-weight: bold;
            }}
            .risk-medium {{
                color: #f47738 !important;
                font-weight: bold;
            }}
            .risk-low {{
                color: #006747 !important;
                font-weight: bold;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

def initialize_session():
    """Initialize session state variables"""
    defaults = {
        'consent': False,
        'patient_data': {
            'name': '',
            'age': 45,
            'weight': 70,
            'bp': '120/80',
            'hba1c': 40,
            'ethnicity': 'White',
            'activity': '30-150 mins',
            'meds': '',
            'smoker': False,
            'family_history': False
        },
        'risk_score': 0.0,
        'advice_generated': False,
        'report_generated': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def consent_form():
    """NHS-compliant consent form"""
    st.title("Data Consent Declaration")
    st.write("""
    This service helps assess your risk of developing Type 2 diabetes and provides 
    prevention advice aligned with NHS guidelines. Before proceeding, please review:
    """)
    
    with st.expander("Privacy Notice"):
        st.write("""
        - Your data will be stored securely in encrypted format
        - No personally identifiable information is shared
        - Data may be used anonymously for service improvement
        - You can request deletion of your data at any time
        """)
    
    if st.checkbox("I consent to the storage and processing of my health data"):
        if st.button("Confirm Consent"):
            st.session_state.consent = True
            st.experimental_rerun()
    else:
        st.warning("You must provide consent to use this service")

def patient_input_page():
    """Input form with clinical data collection"""
    st.title("Diabetes Risk Assessment")
    st.write("Complete all fields for accurate risk prediction")
    
    with st.form("health_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Details")
            st.session_state.patient_data['name'] = st.text_input(
                "Full Name", 
                value=st.session_state.patient_data['name']
            )
            st.session_state.patient_data['age'] = st.number_input(
                "Age", 
                min_value=18, 
                max_value=100, 
                value=st.session_state.patient_data['age']
            )
            st.session_state.patient_data['ethnicity'] = st.selectbox(
                "Ethnic Group", 
                options=["White", "South Asian", "Black African", "Mixed/Other"],
                index=["White", "South Asian", "Black African", "Mixed/Other"].index(
                    st.session_state.patient_data['ethnicity']
                )
            )
            
        with col2:
            st.subheader("Clinical Measurements")
            st.session_state.patient_data['hba1c'] = st.slider(
                "HbA1c (mmol/mol)", 
                min_value=20, 
                max_value=150, 
                value=st.session_state.patient_data['hba1c'],
                help="Glycated hemoglobin - key diabetes marker"
            )
            st.session_state.patient_data['weight'] = st.number_input(
                "Weight (kg)", 
                min_value=30, 
                max_value=300, 
                value=st.session_state.patient_data['weight']
            )
            st.session_state.patient_data['bp'] = st.text_input(
                "Blood Pressure (mmHg)", 
                value=st.session_state.patient_data['bp'],
                placeholder="e.g., 120/80"
            )
        
        st.subheader("Lifestyle Factors")
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.patient_data['activity'] = st.selectbox(
                "Weekly Physical Activity", 
                options=["<30 mins", "30-150 mins", "150+ mins"],
                index=["<30 mins", "30-150 mins", "150+ mins"].index(
                    st.session_state.patient_data['activity']
                )
            )
            st.session_state.patient_data['smoker'] = st.checkbox(
                "Current smoker",
                value=st.session_state.patient_data['smoker']
            )
            
        with col4:
            st.session_state.patient_data['family_history'] = st.checkbox(
                "Family history of diabetes",
                value=st.session_state.patient_data['family_history']
            )
            st.session_state.patient_data['meds'] = st.text_area(
                "Current Medications",
                value=st.session_state.patient_data['meds'],
                placeholder="List all medications separated by commas"
            )
        
        if st.form_submit_button("Save & Calculate Risk"):
            with st.spinner("Calculating diabetes risk..."):
                try:
                    # Calculate risk score
                    st.session_state.risk_score = calculate_risk_score(
                        st.session_state.patient_data
                    )
                    st.session_state.advice_generated = False
                    st.success("Data saved successfully!")
                    time.sleep(1)
                    st.experimental_rerun()
                except Exception as e:
                    logger.error(f"Risk calculation failed: {str(e)}")
                    st.error("Error calculating risk score. Please check your inputs.")

def clinical_advice_page():
    """Personalized prevention advice"""
    st.title("Personalised Prevention Plan")
    
    if not st.session_state.patient_data.get('hba1c'):
        st.warning("Please complete the Patient Input form first")
        return
    
    # Calculate risk if not done
    if not st.session_state.get('risk_score'):
        with st.spinner("Calculating risk profile..."):
            st.session_state.risk_score = calculate_risk_score(
                st.session_state.patient_data
            )
    
    # Display risk score with NHS color coding
    st.subheader("Diabetes Risk Assessment")
    risk_level = "LOW"
    if st.session_state.risk_score >= 20:
        risk_level = "HIGH"
        risk_class = "risk-high"
    elif st.session_state.risk_score >= 10:
        risk_level = "MEDIUM"
        risk_class = "risk-medium"
    else:
        risk_class = "risk-low"
    
    st.markdown(f"""
    <div class='{risk_class}'>
        <h3>10-Year Diabetes Risk: {st.session_state.risk_score}% ({risk_level} RISK)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate advice if not already done
    if not st.session_state.advice_generated or st.button("Regenerate Advice"):
        with st.spinner("Generating personalized advice..."):
            try:
                st.session_state.advice = generate_advice(st.session_state.patient_data)
                st.session_state.advice_generated = True
            except Exception as e:
                logger.error(f"Advice generation failed: {str(e)}")
                st.error("Error generating advice. Please try again.")
    
    # Display advice
    if st.session_state.advice_generated:
        advice = st.session_state.advice
        
        st.subheader("Clinical Recommendations")
        st.info(advice["summary"])
        
        with st.expander("Detailed Prevention Plan"):
            for recommendation in advice["recommendations"]:
                st.write(f"- {recommendation}")
        
        # NHS Prevention Programme
        if advice["referral"]:
            st.subheader("NHS Referral Pathways")
            st.warning("**Clinical Referral Recommended**")
            st.write("Based on your risk profile, you may benefit from:")
            st.markdown("""
            - [NHS Diabetes Prevention Programme](https://www.england.nhs.uk/diabetes/diabetes-prevention/)
            - [Healthier You NHS DPP](https://www.nhs.uk/conditions/type-2-diabetes/understanding-medication/)
            - Local GP diabetes clinic
            """)
            
            if st.button("Find Local Services"):
                st.info("Searching nearby NHS services...")
                # Simulated service lookup
                time.sleep(1)
                st.success("""
                **Services near you:**
                - St Thomas' Hospital Diabetes Clinic (0.8 miles)
                - Guy's Health Centre Prevention Programme (1.2 miles)
                """)
    
    # Lifestyle Resources
    st.subheader("NHS Prevention Resources")
    st.video("https://www.youtube.com/watch?v=kYfNvmF0Bqw")  # NHS diabetes prevention video
    st.markdown("""
    - [NHS Food Scanner App](https://www.nhs.uk/apps-library/nhs-food-scanner-app/)
    - [Couch to 5K Running Plan](https://www.nhs.uk/live-well/exercise/couch-to-5k-week-by-week/)
    - [Diabetes UK Resources](https://www.diabetes.org.uk/preventing-type-2-diabetes)
    """)

def gp_report_page():
    """Clinical report generation"""
    st.title("Clinical Report Generator")
    
    if not st.session_state.patient_data.get('hba1c'):
        st.warning("Please complete the Patient Input form first")
        return
    
    # Generate report on demand
    if st.button("Generate Clinical Report", key="generate_report"):
        with st.spinner("Compiling NHS-compliant report..."):
            try:
                # Ensure latest risk score
                if not st.session_state.get('risk_score'):
                    st.session_state.risk_score = calculate_risk_score(
                        st.session_state.patient_data
                    )
                
                # Generate advice if needed
                if not st.session_state.advice_generated:
                    st.session_state.advice = generate_advice(st.session_state.patient_data)
                    st.session_state.advice_generated = True
                
                # Create PDF
                pdf_path = generate_report(
                    st.session_state.patient_data, 
                    st.session_state.advice,
                    st.session_state.risk_score
                )
                
                # Make downloadable
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📄 Download Full Report", 
                        f, 
                        file_name="nhs_diabetes_report.pdf",
                        mime="application/pdf"
                    )
                
                st.session_state.report_generated = True
                st.success("Report generated successfully!")
                
            except Exception as e:
                logger.error(f"Report generation failed: {str(e)}")
                st.error("Error generating report. Please try again.")
    
    # Preview when report exists
    if st.session_state.report_generated:
        st.subheader("Report Preview")
        advice = st.session_state.advice
        
        with st.expander("Clinical Summary"):
            st.write(advice["summary"])
            
        with st.expander("Key Recommendations"):
            for rec in advice["recommendations"][:5]:
                st.write(f"- {rec}")
        
        st.info("""
        **This report includes:**
        - QDiabetes® risk score analysis
        - NICE guideline compliance checklist
        - Personalized prevention roadmap
        - Referral pathways
        - NHS resource directory
        """)

def main():
    """Main application flow"""
    apply_nhs_styles()
    initialize_session()
    
    # Consent gate
    if not st.session_state.consent:
        consent_form()
        return
    
    # Navigation
    st.sidebar.header("NHS Diabetes Prevention")
    page = st.sidebar.radio("Navigation", [
        "Patient Input", 
        "Clinical Advice", 
        "GP Report",
        "NHS Resources"
    ])
    
    # Page routing
    if page == "Patient Input":
        patient_input_page()
    elif page == "Clinical Advice":
        clinical_advice_page()
    elif page == "GP Report":
        gp_report_page()
    elif page == "NHS Resources":
        st.title("NHS Diabetes Prevention Resources")
        st.write("""
        ## Official NHS Programmes
        - [Healthier You NHS Diabetes Prevention Programme](https://preventing-diabetes.co.uk/)
        - [NHS Type 2 Diabetes Path to Remission](https://www.england.nhs.uk/diabetes/treatment-care/path-to-remission/)
        - [NHS Weight Management Services](https://www.nhs.uk/live-well/healthy-weight/managing-your-weight/nhs-weight-management-guide/)
        
        ## Digital Tools
        - [NHS Food Scanner App](https://www.nhs.uk/apps-library/nhs-food-scanner-app/)
        - [Active 10 Walking Tracker](https://www.nhs.uk/oneyou/active10/home)
        - [NHS BMI Calculator](https://www.nhs.uk/live-well/healthy-weight/bmi-calculator/)
        
        ## Educational Materials
        - [Understanding Type 2 Diabetes](https://www.nhs.uk/conditions/type-2-diabetes/)
        - [Diabetes UK Learning Zone](https://learning.diabetes.org.uk/)
        - [NHS Healthy Eating Guide](https://www.nhs.uk/live-well/eat-well/)
        """)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Clinical Support Line**: 0345 123 4567  
    **NHS Website**: [www.nhs.uk/diabetes](https://www.nhs.uk/conditions/type-2-diabetes/)
    """)

if __name__ == "__main__":
    main()
