def calculate_risk_score(data):
    """QDiabetes®-inspired risk calculation (simplified for MVP)"""
    score = 0
    
    # Base parameters
    age = data.get('age', 45)
    hba1c = data.get('hba1c', 40)
    ethnicity = data.get('ethnicity', 'White')
    bp = data.get('bp', '120/80')
    
    # Age factor (peaks at 55-64)
    if age < 35: score += 1
    elif 35 <= age < 45: score += 3
    elif 45 <= age < 55: score += 6
    elif 55 <= age < 65: score += 9
    else: score += 7
    
    # HbA1c (mmol/mol)
    if 42 <= hba1c <= 47: score += 4  # Prediabetes
    elif hba1c >= 48: score += 8       # Diabetes range
    
    # Ethnicity (NICE NG28 higher risk groups)
    if ethnicity == "South Asian": score += 6
    elif ethnicity == "Black African": score += 4
    
    # Blood pressure
    try:
        systolic, _ = map(int, bp.split('/'))
        if systolic >= 140: score += 3
        elif systolic >= 160: score += 5
    except:
        pass
    
    # Lifestyle factors
    if data.get('smoker'): score += 3
    if data.get('family_history'): score += 2
    if data.get('activity') == "<30 mins": score += 4
    
    # Convert to percentage (simplified algorithm)
    base_risk = min(score * 0.9, 50)
    
    # Apply BMI modifier
    weight = data.get('weight', 70)
    height = 1.75  # Assume average height
    bmi = weight / (height ** 2)
    if bmi > 30: base_risk *= 1.4
    elif bmi > 25: base_risk *= 1.2
    
    return round(min(base_risk, 70), 1)  # Cap at 70%
