"""
Enhanced Vaccine Information System for AI Healthcare Chatbot
Provides comprehensive vaccine data with clear explanations for unavailable vaccines
"""

VACCINE_DATABASE = {
    # ===== AVAILABLE VACCINES =====
    "influenza": {
        "available": True,
        "vaccine_name": "Influenza Vaccine (Flu Shot)",
        "doses": "1-2 doses",
        "schedule": "Annual vaccination (preferably before winter)",
        "dosage_details": "0.5 mL dose administered via intramuscular injection",
        "recommendation": "Recommended for all individuals 6 months or older, especially elderly, children, and immunocompromised",
        "side_effects": "Mild: soreness at injection site, low-grade fever. Rare: severe allergic reaction",
    },
    "covid-19": {
        "available": True,
        "vaccine_name": "COVID-19 Vaccine (Pfizer, Moderna, J&J, AstraZeneca)",
        "doses": "2-3 doses (primary series + booster)",
        "schedule": "Primary: 3-4 weeks apart; Boosters: annually or as recommended",
        "dosage_details": "Varies by brand (30 mcg Pfizer, 100 mcg Moderna, etc.)",
        "recommendation": "Recommended for all individuals 6 months or older for protection against severe illness",
        "side_effects": "Common: arm soreness, fatigue, headache. Rare: myocarditis (very rare)",
    },
    "measles": {
        "available": True,
        "vaccine_name": "MMR Vaccine (Measles, Mumps, Rubella)",
        "doses": "2 doses",
        "schedule": "First dose at 12-15 months; Second dose at 4-6 years",
        "dosage_details": "0.5 mL subcutaneous injection",
        "recommendation": "Part of routine childhood immunization. Essential for disease eradication.",
        "side_effects": "Mild rash, fever. Rare: febrile seizures",
    },
    "polio": {
        "available": True,
        "vaccine_name": "Polio Vaccine (IPV - Inactivated Polio Vaccine)",
        "doses": "4 doses",
        "schedule": "At 2, 4, 6-18 months, and 4-6 years",
        "dosage_details": "0.5 mL intramuscular injection",
        "recommendation": "Critical childhood vaccine. Nearly eradicated due to vaccination programs.",
        "side_effects": "Minimal; soreness at injection site",
    },
    "hepatitis b": {
        "available": True,
        "vaccine_name": "Hepatitis B Vaccine",
        "doses": "3 doses",
        "schedule": "Birth, 1-2 months, and 6 months (standard series)",
        "dosage_details": "10-20 mcg depending on formulation",
        "recommendation": "Given at birth; protects against chronic liver disease and cancer",
        "side_effects": "Mild soreness, low-grade fever",
    },
    "tetanus": {
        "available": True,
        "vaccine_name": "Tetanus Vaccine (DPT - Diphtheria, Pertussis, Tetanus)",
        "doses": "5 doses (primary) + boosters every 10 years",
        "schedule": "At 2, 4, 6, 15-18 months, and 4-6 years; Boosters every 10 years",
        "dosage_details": "0.5 mL intramuscular injection",
        "recommendation": "Essential protection against tetanus, diphtheria, and pertussis. Booster after injury if >5 years",
        "side_effects": "Arm soreness, low-grade fever",
    },
    "yellow fever": {
        "available": True,
        "vaccine_name": "Yellow Fever Vaccine",
        "doses": "1 dose",
        "schedule": "Single dose provides lifelong immunity (booster every 10 years if needed)",
        "dosage_details": "0.5 mL subcutaneous injection",
        "recommendation": "Required for travelers to endemic regions in Africa and South America",
        "side_effects": "Mild: fever, myalgia. Rare: vaccine-derived viscerotropic disease in elderly",
    },
    "tuberculosis": {
        "available": True,
        "vaccine_name": "BCG Vaccine (Bacillus Calmette-Guérin)",
        "doses": "1 dose",
        "schedule": "At birth or within first year in endemic regions",
        "dosage_details": "0.1 mL intradermal injection",
        "recommendation": "Primarily used in tuberculosis-endemic regions. Protects children from severe TB.",
        "side_effects": "Localized scar at injection site",
    },
    "pneumonia": {
        "available": True,
        "vaccine_name": "Pneumococcal Vaccine (PCV and PPSV)",
        "doses": "Multiple doses (dosing depends on type and age)",
        "schedule": "Ages 2, 4, 6 months, and 12-15 months (PCV); PPSV23 at 65+ or high-risk groups",
        "dosage_details": "0.5 mL intramuscular or subcutaneous injection",
        "recommendation": "Protects against bacterial pneumonia. Essential for elderly and immunocompromised",
        "side_effects": "Arm soreness, mild fever, muscle aches",
    },
    "mumps": {
        "available": True,
        "vaccine_name": "MMR Vaccine (Measles, Mumps, Rubella)",
        "doses": "2 doses",
        "schedule": "First dose at 12-15 months; Second dose at 4-6 years",
        "dosage_details": "0.5 mL subcutaneous injection",
        "recommendation": "Part of routine childhood immunization",
        "side_effects": "Mild rash, fever. Rare: parotitis (swelling of salivary glands)",
    },
    "rubella": {
        "available": True,
        "vaccine_name": "MMR Vaccine (Measles, Mumps, Rubella)",
        "doses": "2 doses",
        "schedule": "First dose at 12-15 months; Second dose at 4-6 years",
        "dosage_details": "0.5 mL subcutaneous injection",
        "recommendation": "Essential for women of childbearing age to prevent congenital rubella",
        "side_effects": "Mild rash, fever",
    },
    "varicella": {
        "available": True,
        "vaccine_name": "Varicella Vaccine (Chickenpox Vaccine)",
        "doses": "2 doses",
        "schedule": "First dose at 12-15 months; Second dose at 4-6 years",
        "dosage_details": "0.5 mL subcutaneous injection",
        "recommendation": "Prevents chickenpox. Essential for childhood immunization",
        "side_effects": "Mild rash, low-grade fever",
    },
    "hepatitis a": {
        "available": True,
        "vaccine_name": "Hepatitis A Vaccine",
        "doses": "2 doses",
        "schedule": "Initial dose, then booster at 6-12 months",
        "dosage_details": "0.5 mL intramuscular injection",
        "recommendation": "Recommended for travelers to endemic regions and high-risk groups",
        "side_effects": "Soreness at injection site, mild fatigue",
    },
    "pertussis": {
        "available": True,
        "vaccine_name": "Pertussis Vaccine (DPT - Diphtheria, Pertussis, Tetanus)",
        "doses": "5 doses (primary) + boosters every 10 years",
        "schedule": "At 2, 4, 6, 15-18 months, and 4-6 years",
        "dosage_details": "0.5 mL intramuscular injection",
        "recommendation": "Protects against whooping cough. Essential for newborns and infants",
        "side_effects": "Mild fever, fussiness in infants",
    },
    "diphtheria": {
        "available": True,
        "vaccine_name": "Diphtheria Vaccine (DPT - Diphtheria, Pertussis, Tetanus)",
        "doses": "5 doses (primary) + boosters every 10 years",
        "schedule": "At 2, 4, 6, 15-18 months, and 4-6 years",
        "dosage_details": "0.5 mL intramuscular injection",
        "recommendation": "Critical vaccine against dangerous respiratory infection",
        "side_effects": "Arm soreness, low-grade fever",
    },
    "meningitis": {
        "available": True,
        "vaccine_name": "Meningococcal Vaccine (MCV, MenB, MenACWY)",
        "doses": "1-4 doses depending on type",
        "schedule": "Ages 11-12 (routine); can be given as early as age 9 or up to age 26",
        "dosage_details": "0.5 mL intramuscular injection",
        "recommendation": "Prevents bacterial meningitis. Recommended for teens and young adults",
        "side_effects": "Arm soreness, mild fever, fatigue",
    },
    "rotavirus": {
        "available": True,
        "vaccine_name": "Rotavirus Vaccine",
        "doses": "2-3 doses (depends on brand)",
        "schedule": "At 2, 4 months (Rotarix); or 2, 4, 6 months (RotaTeq)",
        "dosage_details": "Oral vaccine",
        "recommendation": "Essential infant vaccine against severe gastroenteritis",
        "side_effects": "Mild diarrhea or vomiting (rare)",
    },

    # ===== UNAVAILABLE VACCINES =====
    "common cold": {
        "available": False,
        "disease_name": "Common Cold",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is currently available for the common cold.",
        "scientific_reason": "The virus mutates very quickly and has over 200 different viral strains causing cold symptoms. Creating a vaccine covering all variants would be extremely complex and expensive. Additionally, immunity from the vaccine would be short-lived due to constant viral mutations.",
        "alternative": "Wash hands frequently, avoid close contact with sick people, stay hydrated, rest, and use over-the-counter symptom relief.",
    },
    "hiv": {
        "available": False,
        "disease_name": "HIV",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is currently available for HIV.",
        "scientific_reason": "HIV is extremely complex for vaccine development. The virus mutates rapidly, has multiple strains, and can hide in immune cells. It doesn't trigger natural immunity even after infection. Vaccine development is ongoing in clinical trials, but success has been limited so far.",
        "alternative": "Use preventive medications (PrEP), practice safe sex, avoid sharing needles, and seek immediate treatment if exposed.",
    },
    "ebola": {
        "available": False,
        "disease_name": "Ebola",
        "vaccine_status": "Not Available",
        "reason_unavailable": "A vaccine exists but is not widely available or recommended for general population.",
        "scientific_reason": "Ebola vaccine development was limited due to rare outbreaks and funding constraints. While some vaccines (Ervebo) have been approved, they are reserved for healthcare workers and outbreak response teams. The disease affects a small population, making general distribution impractical.",
        "alternative": "Avoid contact with infected animals or people, use protective equipment if exposed, and seek immediate medical care.",
    },
    "zika": {
        "available": False,
        "disease_name": "Zika Virus",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is currently available for Zika virus.",
        "scientific_reason": "Though vaccine development is ongoing, no approved vaccine has reached clinical use yet. Research is challenging due to the virus's fast-changing strains and small patient populations between outbreaks. Several candidates are in clinical trials but face funding and research hurdles.",
        "alternative": "Use mosquito repellent, wear protective clothing, avoid mosquito-prone areas, and practice safe sex if traveling to endemic regions.",
    },
    "dengue": {
        "available": False,
        "disease_name": "Dengue",
        "vaccine_status": "Not Available",
        "reason_unavailable": "A vaccine exists but has very limited availability and specific use restrictions.",
        "scientific_reason": "Dengue has four distinct strains. The available vaccine (Dengvaxia) can only be safely given to people who have had dengue before. In unvaccinated individuals, the vaccine can actually increase severe illness risk. This 'antibody-dependent enhancement' makes widespread vaccination dangerous without prior infection.",
        "alternative": "Use mosquito nets, apply insect repellent, wear long sleeves, and seek early treatment if symptoms develop.",
    },
    "smallpox": {
        "available": False,
        "disease_name": "Smallpox",
        "vaccine_status": "Not Available",
        "reason_unavailable": "Smallpox vaccine is not needed for the general population.",
        "scientific_reason": "Smallpox was completely eradicated from nature in 1980 through global vaccination campaigns. Since the disease no longer exists naturally, routine vaccination is unnecessary. Vaccines are only given to researchers studying the virus or military/emergency personnel.",
        "alternative": "No vaccination needed. The disease's natural form has been eliminated worldwide.",
    },
    "rsv": {
        "available": False,
        "disease_name": "Respiratory Syncytial Virus (RSV)",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No safe or effective vaccine is currently available for RSV.",
        "scientific_reason": "RSV vaccine development has been challenging for decades. A past vaccine trial in the 1960s actually worsened disease in vaccinated children (antibody-dependent enhancement). Current vaccines are in clinical trials but face safety concerns and the need for repeated doses due to RSV's immune evasion.",
        "alternative": "Practice good hygiene, avoid crowded places during RSV season, use hand sanitizer, and seek medical care for severe symptoms.",
    },
    "norovirus": {
        "available": False,
        "disease_name": "Norovirus",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is currently available for Norovirus.",
        "scientific_reason": "Norovirus constantly mutates with hundreds of strains emerging continuously. The virus causes short-term illness but limited long-term immunity. Research funding is low due to the disease's self-limiting nature in most patients, making vaccine development economically unviable.",
        "alternative": "Practice strict hand hygiene, avoid contaminated food and water, disinfect surfaces, and stay hydrated during infection.",
    },
    "lyme disease": {
        "available": False,
        "disease_name": "Lyme Disease",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is currently available for Lyme disease.",
        "scientific_reason": "A Lyme vaccine (LYMErix) existed but was withdrawn from the market in 2002 due to public concerns about side effects (later shown to be unfounded). Vaccine development has largely ceased due to liability concerns and limited market demand, despite the disease's increasing prevalence.",
        "alternative": "Use tick repellent, wear protective clothing in wooded areas, check for ticks regularly, and seek early treatment with antibiotics if infected.",
    },
    "aids": {
        "available": False,
        "disease_name": "AIDS",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is currently available for AIDS.",
        "scientific_reason": "AIDS is caused by HIV, which rapidly mutates and hides from the immune system. The virus has multiple strains globally, and natural infection doesn't prevent reinfection with different strains. Despite 40+ years of research, vaccine efficacy remains below acceptable levels for approval.",
        "alternative": "Use antiretroviral therapy (ART) if infected, take PrEP as prevention, practice safe sex, and avoid sharing needles.",
    },
    "chronic fatigue syndrome": {
        "available": False,
        "disease_name": "Chronic Fatigue Syndrome",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine exists for Chronic Fatigue Syndrome.",
        "scientific_reason": "Chronic Fatigue Syndrome (ME/CFS) is a complex condition of unclear origin. While possibly triggered by viruses, the underlying mechanism isn't fully understood. Without understanding the exact cause, developing and testing a vaccine is not scientifically feasible.",
        "alternative": "Treatment focuses on symptom management, pacing of activities, cognitive behavioral therapy, and gradual exercise programs.",
    },
    "cancer": {
        "available": False,
        "disease_name": "Cancer",
        "vaccine_status": "Limited Availability",
        "reason_unavailable": "While cancer-prevention vaccines exist (like HPV vaccine), no universal cancer vaccine is available.",
        "scientific_reason": "Cancer is hundreds of different diseases with distinct genetic mutations. A single vaccine cannot prevent all cancer types. HPV vaccine prevents specific cancers caused by human papillomavirus, but other cancers (lung, breast, colon) arise from various causes requiring different approaches.",
        "alternative": "Use available preventive vaccines (HPV for cervical cancer), screening tests, maintain healthy lifestyle, avoid carcinogens, and seek early treatment.",
    },
    "autoimmune disease": {
        "available": False,
        "disease_name": "Autoimmune Disease",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is available for autoimmune diseases.",
        "scientific_reason": "Autoimmune diseases occur when the immune system attacks the body's own cells. Vaccinating could theoretically strengthen an already overactive immune system, worsening the condition. Treatment focuses on immune suppression, not activation.",
        "alternative": "Treatment uses anti-inflammatory medications, immunosuppressants, and symptom management tailored to specific conditions.",
    },
    "cystic fibrosis": {
        "available": False,
        "disease_name": "Cystic Fibrosis",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is available for Cystic Fibrosis.",
        "scientific_reason": "Cystic Fibrosis is a genetic disorder caused by mutations in the CFTR gene. Vaccines prevent infectious diseases but cannot correct genetic mutations in every cell of the body. Gene therapy approaches are being researched but are not yet widely available.",
        "alternative": "Treatment includes chest physiotherapy, medications to clear airways, antibiotics for infections, and emerging gene therapy options.",
    },
    "diabetes": {
        "available": False,
        "disease_name": "Diabetes",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is available for Diabetes.",
        "scientific_reason": "Diabetes is primarily a metabolic disorder, not an infectious disease. Vaccines prevent infections by training the immune system. Type 1 diabetes is autoimmune, and Type 2 is metabolic. Neither can be prevented by vaccination.",
        "alternative": "Prevention involves maintaining healthy weight, regular exercise, balanced diet, limiting sugar, and monitoring blood glucose levels.",
    },
    "heart disease": {
        "available": False,
        "disease_name": "Heart Disease",
        "vaccine_status": "Not Available",
        "reason_unavailable": "No vaccine is available for Heart Disease.",
        "scientific_reason": "Heart disease results from atherosclerosis, plaque buildup, and lifestyle factors—not from infection. Vaccines work against pathogens, not chronic degenerative conditions. A few research trials explore vaccines against specific lipoproteins, but these are years away from general use.",
        "alternative": "Prevention focuses on healthy diet, exercise, managing blood pressure and cholesterol, not smoking, and regular monitoring.",
    },
}


def get_vaccine_info(disease_input):
    """
    Retrieve vaccine information for a given disease.
    
    Args:
        disease_input (str): The disease name entered by the user
        
    Returns:
        dict: Vaccine information with appropriate format for available/unavailable vaccines
    """
    disease = disease_input.strip().lower()

    if disease in VACCINE_DATABASE:
        vaccine_data = VACCINE_DATABASE[disease].copy()
        vaccine_data["disease"] = disease_input.strip().title()

        if not vaccine_data.get("available", False):
            # Format for unavailable vaccines
            return {
                "disease": vaccine_data.get("disease_name", vaccine_data["disease"]),
                "available": False,
                "vaccine_status": vaccine_data.get("vaccine_status", "Not Available"),
                "reason_unavailable": vaccine_data.get("reason_unavailable", "Vaccine not available"),
                "scientific_reason": vaccine_data.get("scientific_reason", ""),
                "alternative": vaccine_data.get("alternative", ""),
            }
        else:
            # Format for available vaccines
            return {
                "disease": vaccine_data["disease"],
                "available": True,
                "vaccine_name": vaccine_data.get("vaccine_name", ""),
                "doses": vaccine_data.get("doses", ""),
                "schedule": vaccine_data.get("schedule", ""),
                "dosage_details": vaccine_data.get("dosage_details", ""),
                "recommendation": vaccine_data.get("recommendation", ""),
                "side_effects": vaccine_data.get("side_effects", ""),
            }

    # Disease not found
    return {
        "disease": disease_input.strip().title(),
        "available": None,
        "message": f"Disease '{disease_input}' not found in our vaccine database.",
        "suggestion": "Please check the spelling or try another disease name. Common diseases include: Influenza, COVID-19, Measles, Polio, Hepatitis B, Tetanus, Yellow Fever, and Pneumonia.",
    }


def list_available_vaccines():
    """
    Get a list of all available vaccines in the database.
    
    Returns:
        list: List of diseases/conditions with available vaccines
    """
    available = []
    for disease, info in VACCINE_DATABASE.items():
        if info.get("available", False):
            available.append(disease.title())

    return sorted(available)
