def calculate_risk_score(data):
    """Simplified QDiabetes risk calculator"""
    score = 0
    
    # Age scoring
    age = data.get('age', 45)
    if age < 40: score += 1
    elif 40 <= age < 50: score += 3
    elif 50 <= age < 60: score += 5
    else: score += 7
    
    # HbA1c scoring
    hba1c = data.get('hba1c', 0)
    if 42 <= hba1c <= 47: score += 4
    elif hba1c >= 48: score += 8
    
    # Ethnicity modifiers
    ethnicity = data.get('ethnicity', 'White')
    if ethnicity == "South Asian": score += 6
    elif ethnicity == "Black African": score += 4
    
    # Other factors
    if data.get('smoker', False): score += 3
    if data.get('family_history', False): score += 2
    
    # Convert to percentage
    risk = min(score * 1.2, 50)
    return round(risk, 1)
