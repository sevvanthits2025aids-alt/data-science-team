"""
Advanced Vaccine Prediction System for Healthcare Project
Provides intelligent vaccine availability checking with normalization, synonyms, confidence scoring, and explainable results.
"""

import re
from difflib import SequenceMatcher

# Disease synonyms mapping for better matching
DISEASE_SYNONYMS = {
    "covid": "covid-19",
    "covid-19": "covid-19",
    "coronavirus": "covid-19",
    "sars-cov-2": "covid-19",
    "flu": "influenza",
    "flu virus": "influenza",
    "influenza virus": "influenza",
    "measles virus": "measles",
    "polio virus": "polio",
    "hepatitis b virus": "hepatitis b",
    "tetanus bacteria": "tetanus",
    "yellow fever virus": "yellow fever",
    "tb": "tuberculosis",
    "tuberculosis bacteria": "tuberculosis",
    "pneumococcal": "pneumonia",
    "pneumococcal pneumonia": "pneumonia",
    "mumps virus": "mumps",
    "rubella virus": "rubella",
    "chickenpox": "varicella",
    "chicken pox": "varicella",
    "hepatitis a virus": "hepatitis a",
    "whooping cough": "pertussis",
    "diphtheria bacteria": "diphtheria",
    "meningococcal": "meningitis",
    "rotavirus infection": "rotavirus",
    "common cold virus": "common cold",
    "hiv virus": "hiv",
    "aids virus": "hiv",
    "ebola virus": "ebola",
    "zika virus": "zika",
    "dengue virus": "dengue",
    "smallpox virus": "smallpox",
    "rsv virus": "rsv",
    "respiratory syncytial virus": "rsv",
    "norovirus infection": "norovirus",
    "lyme": "lyme disease",
    "lyme disease bacteria": "lyme disease",
    "chronic fatigue": "chronic fatigue syndrome",
    "me/cfs": "chronic fatigue syndrome",
    "cystic fibrosis disease": "cystic fibrosis",
    "diabetes mellitus": "diabetes",
    "type 1 diabetes": "diabetes",
    "type 2 diabetes": "diabetes",
    "cardiovascular disease": "heart disease",
    "coronary heart disease": "heart disease",
    "autoimmune disorders": "autoimmune disease",
}

# Enhanced Vaccine Database with effectiveness levels
VACCINE_DATABASE = {
    # ===== AVAILABLE VACCINES =====
    "influenza": {
        "available": True,
        "vaccine_name": "Influenza Vaccine (Flu Shot)",
        "doses": "Annual dose recommended",
        "effectiveness": "High",
        "reason": "Well-established vaccine widely used globally",
    },
    "covid-19": {
        "available": True,
        "vaccine_name": "COVID-19 Vaccine (Various brands)",
        "doses": "2-3 doses (primary + boosters)",
        "effectiveness": "High",
        "reason": "Highly effective against severe illness and hospitalization",
    },
    "measles": {
        "available": True,
        "vaccine_name": "MMR Vaccine",
        "doses": "2 doses",
        "effectiveness": "High",
        "reason": "Nearly 100% effective when properly administered",
    },
    "polio": {
        "available": True,
        "vaccine_name": "Polio Vaccine (IPV)",
        "doses": "4 doses",
        "effectiveness": "High",
        "reason": "Critical for global polio eradication efforts",
    },
    "hepatitis b": {
        "available": True,
        "vaccine_name": "Hepatitis B Vaccine",
        "doses": "3 doses",
        "effectiveness": "High",
        "reason": "Highly effective against chronic liver disease",
    },
    "tetanus": {
        "available": True,
        "vaccine_name": "Tetanus Vaccine (Td/Tdap)",
        "doses": "5 doses + boosters every 10 years",
        "effectiveness": "High",
        "reason": "Essential protection against deadly bacterial infection",
    },
    "yellow fever": {
        "available": True,
        "vaccine_name": "Yellow Fever Vaccine",
        "doses": "1 dose (lifelong immunity)",
        "effectiveness": "High",
        "reason": "Highly effective for travelers to endemic areas",
    },
    "tuberculosis": {
        "available": True,
        "vaccine_name": "BCG Vaccine",
        "doses": "1 dose",
        "effectiveness": "Medium",
        "reason": "Effective in preventing severe TB in children",
    },
    "pneumonia": {
        "available": True,
        "vaccine_name": "Pneumococcal Vaccine",
        "doses": "Multiple doses based on age",
        "effectiveness": "High",
        "reason": "Strong protection against bacterial pneumonia",
    },
    "mumps": {
        "available": True,
        "vaccine_name": "MMR Vaccine",
        "doses": "2 doses",
        "effectiveness": "High",
        "reason": "Highly effective against mumps infection",
    },
    "rubella": {
        "available": True,
        "vaccine_name": "MMR Vaccine",
        "doses": "2 doses",
        "effectiveness": "High",
        "reason": "Essential for preventing congenital rubella",
    },
    "varicella": {
        "available": True,
        "vaccine_name": "Varicella Vaccine",
        "doses": "2 doses",
        "effectiveness": "High",
        "reason": "Highly effective against chickenpox",
    },
    "hepatitis a": {
        "available": True,
        "vaccine_name": "Hepatitis A Vaccine",
        "doses": "2 doses",
        "effectiveness": "High",
        "reason": "Excellent protection against hepatitis A",
    },
    "pertussis": {
        "available": True,
        "vaccine_name": "Pertussis Vaccine (DTaP/Tdap)",
        "doses": "5 doses + boosters",
        "effectiveness": "High",
        "reason": "Critical for protecting infants from whooping cough",
    },
    "diphtheria": {
        "available": True,
        "vaccine_name": "Diphtheria Vaccine (DTaP/Tdap)",
        "doses": "5 doses + boosters",
        "effectiveness": "High",
        "reason": "Highly effective against diphtheria",
    },
    "meningitis": {
        "available": True,
        "vaccine_name": "Meningococcal Vaccine",
        "doses": "1-4 doses depending on type",
        "effectiveness": "High",
        "reason": "Strong protection against bacterial meningitis",
    },
    "rotavirus": {
        "available": True,
        "vaccine_name": "Rotavirus Vaccine",
        "doses": "2-3 doses",
        "effectiveness": "High",
        "reason": "Highly effective against severe rotavirus gastroenteritis",
    },

    # ===== UNAVAILABLE OR LIMITED VACCINES =====
    "common cold": {
        "available": False,
        "reason": "No vaccine developed yet due to numerous viral strains and rapid mutations",
    },
    "hiv": {
        "available": False,
        "reason": "Extremely complex virus with rapid mutations; vaccine development ongoing but challenging",
    },
    "ebola": {
        "available": "Limited",
        "vaccine_name": "Ervebo (rVSV-ZEBOV)",
        "doses": "1 dose",
        "effectiveness": "High",
        "reason": "Available but primarily for outbreak response and high-risk groups",
    },
    "zika": {
        "available": False,
        "reason": "No approved vaccine yet; research ongoing but challenging due to virus characteristics",
    },
    "dengue": {
        "available": "Limited",
        "vaccine_name": "Dengvaxia",
        "doses": "3 doses",
        "effectiveness": "Medium",
        "reason": "Only safe for those previously infected; can increase risk in others",
    },
    "smallpox": {
        "available": "Limited",
        "reason": "Disease eradicated; vaccine only for research/emergency personnel",
    },
    "rsv": {
        "available": False,
        "reason": "Vaccine development challenging due to immune enhancement risks",
    },
    "norovirus": {
        "available": False,
        "reason": "Rapidly mutating virus with many strains; economically unviable",
    },
    "lyme disease": {
        "available": False,
        "reason": "Previous vaccine withdrawn; development stalled due to market concerns",
    },
    "aids": {
        "available": False,
        "reason": "Caused by HIV; vaccine development extremely difficult due to viral complexity",
    },
    "chronic fatigue syndrome": {
        "available": False,
        "reason": "Not an infectious disease; cause unclear, so no vaccine possible",
    },
    "cancer": {
        "available": "Limited",
        "reason": "Some preventive vaccines exist (e.g., HPV), but no universal cancer vaccine",
    },
    "autoimmune disease": {
        "available": False,
        "reason": "Not caused by infection; immune system disorders managed with other treatments",
    },
    "cystic fibrosis": {
        "available": False,
        "reason": "Genetic disorder, not infectious; requires gene therapy approaches",
    },
    "diabetes": {
        "available": False,
        "reason": "Metabolic disorder managed with medication and lifestyle, not vaccination",
    },
    "heart disease": {
        "available": False,
        "reason": "Not an infectious disease; caused by lifestyle and genetic factors",
    },
}


def normalize_input(disease_name):
    """
    Normalize disease name by lowercasing, removing extra spaces, and stripping punctuation.
    
    Args:
        disease_name (str): The input disease name
        
    Returns:
        str: Normalized disease name
    """
    if not disease_name:
        return ""
    
    # Lowercase and strip
    normalized = disease_name.lower().strip()
    
    # Remove extra spaces
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Remove punctuation except hyphens
    normalized = re.sub(r'[^\w\s-]', '', normalized)
    
    return normalized


def find_best_match(normalized_disease):
    """
    Find the best matching disease from database using exact match, synonyms, and fuzzy matching.
    
    Args:
        normalized_disease (str): Normalized disease name
        
    Returns:
        tuple: (matched_disease_key, match_type, confidence_score)
    """
    # Check for exact synonym match
    if normalized_disease in DISEASE_SYNONYMS:
        canonical = DISEASE_SYNONYMS[normalized_disease]
        if canonical in VACCINE_DATABASE:
            return canonical, "exact", 95
    
    # Check for exact database match
    if normalized_disease in VACCINE_DATABASE:
        return normalized_disease, "exact", 100
    
    # Check for partial matches using keywords
    best_match = None
    best_score = 0
    match_type = "weak"
    
    for db_disease in VACCINE_DATABASE.keys():
        # Simple keyword matching
        input_words = set(normalized_disease.split())
        db_words = set(db_disease.split())
        
        if input_words & db_words:  # Intersection
            overlap = len(input_words & db_words)
            total = len(input_words | db_words)
            score = (overlap / total) * 100
            
            if score > best_score:
                best_score = score
                best_match = db_disease
                match_type = "partial" if score >= 50 else "weak"
    
    # Fuzzy string matching as fallback
    if not best_match or best_score < 60:
        for db_disease in VACCINE_DATABASE.keys():
            similarity = SequenceMatcher(None, normalized_disease, db_disease).ratio() * 100
            if similarity > best_score and similarity >= 60:
                best_score = similarity
                best_match = db_disease
                match_type = "partial"
    
    if best_match:
        confidence = calculate_confidence(match_type, best_score)
        return best_match, match_type, confidence
    
    return None, "none", 0


def calculate_confidence(match_type, score=0):
    """
    Calculate confidence score based on match type and similarity score.
    
    Args:
        match_type (str): Type of match ("exact", "partial", "weak", "none")
        score (float): Similarity score for partial matches
        
    Returns:
        int: Confidence percentage
    """
    if match_type == "exact":
        return 95 if score < 100 else 100
    elif match_type == "partial":
        return max(60, min(89, int(score)))
    elif match_type == "weak":
        return max(40, min(59, int(score)))
    else:
        return 0


def check_vaccine(disease_name, risk_factors=None):
    """
    Check vaccine availability for a disease with intelligent matching.
    
    Args:
        disease_name (str): The disease name to check
        risk_factors (dict, optional): Patient risk factors (age_group, severity, etc.)
        
    Returns:
        dict: Vaccine information with confidence and reasoning
    """
    normalized = normalize_input(disease_name)
    
    if not normalized:
        return {
            "disease": disease_name,
            "available": None,
            "confidence": 0,
            "reason": "Invalid disease name provided"
        }
    
    matched_disease, match_type, confidence = find_best_match(normalized)
    
    if not matched_disease:
        return {
            "disease": disease_name.title(),
            "available": None,
            "confidence": 0,
            "reason": f"No matching disease found for '{disease_name}'. Please check spelling or try a different name."
        }
    
    vaccine_info = VACCINE_DATABASE[matched_disease]
    available = vaccine_info["available"]
    
    # Adjust recommendation based on risk factors if provided
    adjusted_reason = vaccine_info.get("reason", "")
    if risk_factors:
        if "age_group" in risk_factors:
            age = risk_factors["age_group"].lower()
            if age in ["elderly", "senior", "65+"] and matched_disease == "influenza":
                adjusted_reason += " Especially important for elderly due to higher risk of complications."
            elif age in ["infant", "child", "0-5"] and matched_disease in ["measles", "polio"]:
                adjusted_reason += " Critical for young children to prevent severe outcomes."
    
    result = {
        "disease": matched_disease.replace("-", " ").title(),
        "available": available,
        "confidence": confidence,
        "reason": adjusted_reason
    }
    
    if available in [True, "Limited"]:
        result.update({
            "vaccine_name": vaccine_info.get("vaccine_name", "N/A"),
            "doses": vaccine_info.get("doses", "N/A"),
            "effectiveness": vaccine_info.get("effectiveness", "N/A")
        })
    
    return result


def generate_response(disease, vaccine_info, confidence, reason):
    """
    Generate formatted response string for vaccine prediction.
    
    Args:
        disease (str): Disease name
        vaccine_info (dict): Vaccine information
        confidence (int): Confidence score
        reason (str): Explanation reason
        
    Returns:
        str: Formatted response
    """
    available = vaccine_info.get("available")
    
    response = "====================================\n"
    response += "💉 VACCINE PREDICTION SYSTEM\n"
    response += "====================================\n"
    response += f"🦠 Disease: {disease}\n"
    
    if available in [True, "Limited"]:
        response += f"💉 Vaccine Available: {'Yes' if available == True else 'Limited'}\n"
        response += f"📦 Vaccine Name: {vaccine_info.get('vaccine_name', 'N/A')}\n"
        response += f"📊 Effectiveness: {vaccine_info.get('effectiveness', 'N/A')}\n"
        response += f"🔢 Doses: {vaccine_info.get('doses', 'N/A')}\n"
    else:
        response += "💉 Vaccine Available: No\n"
    
    response += f"📈 Confidence Score: {confidence}%\n"
    response += f"💡 Reason: {reason}\n"
    response += "====================================\n"
    
    return response


def predict_vaccine(disease_name, risk_factors=None):
    """
    Main function to predict vaccine availability for a disease.
    
    Args:
        disease_name (str): Disease name
        risk_factors (dict, optional): Risk factors like {"age_group": "elderly", "severity": "high"}
        
    Returns:
        str: Formatted prediction response
    """
    vaccine_result = check_vaccine(disease_name, risk_factors)
    
    return generate_response(
        vaccine_result["disease"],
        vaccine_result,
        vaccine_result["confidence"],
        vaccine_result["reason"]
    )


def get_vaccine_info(disease_name, risk_factors=None):
    """
    Get vaccine information for a disease.
    
    Args:
        disease_name (str): Disease name
        risk_factors (dict, optional): Risk factors
        
    Returns:
        dict: Vaccine information
    """
    return check_vaccine(disease_name, risk_factors)


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    print(predict_vaccine("Flu"))
    print(predict_vaccine("COVID"))
    print(predict_vaccine("Diabetes"))
    print(predict_vaccine("Unknown Disease"))
    
    # With risk factors
    print(predict_vaccine("Influenza", {"age_group": "elderly"}))
