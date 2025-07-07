def get_advice(data):
    hba1c = data['hba1c']
    
    if hba1c > 64:
        return "🟥 URGENT: HbA1c too high (>64)\n\n- Contact GP immediately\n- Review medications\n- Monitor daily"
    elif hba1c > 53:
        return "🟨 WARNING: HbA1c elevated (53-64)\n\n- Increase activity to 5 days/week\n- Reduce sugar intake\n- Retest in 3 months"
    else:
        return "🟩 GOOD: HbA1c in range (<53)\n\n- Maintain current habits\n- Annual checkup recommended"
