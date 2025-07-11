# COMPLETELY REPLACE this file with:
from clinical_rules import calculate_risk_score

def generate_advice(data):
    advice = {
        "priority": "LOW", 
        "summary": "", 
        "recommendations": [],
        "referral": False
    }
    
    # HbA1c assessment (NICE NG28)
    hba1c = data.get('hba1c', 0)
    if hba1c >= 48:
        advice["priority"] = "HIGH"
        advice["summary"] = "🟥 URGENT: Likely diabetes (HbA1c ≥48)"
        advice["referral"] = True
        advice["recommendations"].append("Immediate GP referral required")
        advice["recommendations"].append("Confirm diagnosis with repeat HbA1c or FPG")
    elif 42 <= hba1c <= 47:
        advice["priority"] = "MEDIUM"
        advice["summary"] = "🟨 WARNING: High risk (Prediabetes)"
        advice["recommendations"].append("Refer to NHS Diabetes Prevention Programme")
        advice["recommendations"].append("Lifestyle intervention: 9-month program")
    else:
        advice["summary"] = "🟩 GOOD: Normal HbA1c"
        if hba1c >= 39:
            advice["recommendations"].append("Maintain healthy lifestyle to prevent progression")
    
    # Cardiovascular risk
    if 'bp' in data and data['bp']:
        try:
            systolic, diastolic = map(int, data['bp'].split('/'))
            if systolic >= 140 or diastolic >= 90:
                advice["recommendations"].append(f"Hypertension ({systolic}/{diastolic}) - Monitor weekly")
                if systolic >= 160:
                    advice["referral"] = True
        except:
            pass
    
    # Ethnicity risk modifiers
    ethnicity = data.get('ethnicity', '')
    if ethnicity in ["South Asian", "Black African"]:
        advice["recommendations"].append(f"Higher risk profile: {ethnicity} ethnicity")
    
    # Lifestyle recommendations
    activity = data.get('activity', '')
    if activity == "<30 mins":
        advice["recommendations"].append("Increase activity: Aim for 150 mins/week")
        advice["recommendations"].append("Start with brisk walking 10 mins/day")
    elif activity == "30-150 mins":
        advice["recommendations"].append("Good activity level - maintain 150+ mins/week")
    
    if data.get('smoker', False):
        advice["recommendations"].append("🚭 Smoking cessation: Refer to NHS Stop Smoking Services")
        advice["referral"] = True
    
    # Risk score calculation
    risk_score = calculate_risk_score(data)
    advice["summary"] += f" | 10-yr risk: {risk_score}%"
    if risk_score > 10:
        advice["recommendations"].append(f"High cardiovascular risk ({risk_score}%) - Consider statin therapy")
    
    return advice
