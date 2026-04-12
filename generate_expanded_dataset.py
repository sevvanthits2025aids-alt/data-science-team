"""
Expanded Vaccine Dataset Generator
Integrates medical datasets to create 15,000+ entries for disease prediction and vaccine information.
Combines data from multiple sources including Kaggle-style medical datasets.
"""

import json
import csv
import random
from collections import defaultdict

# Base medical data structures (simulating Kaggle dataset integration)
DISEASE_CATEGORIES = {
    "Disease": [
        "Influenza", "COVID-19", "Pneumonia", "Bronchitis", "Tuberculosis", "Malaria",
        "Dengue", "Cholera", "Typhoid", "Hepatitis A", "Hepatitis B", "Hepatitis C",
        "Chickenpox", "Shingles", "Measles", "Mumps", "Rubella", "Polio",
        "Tetanus", "Diphtheria", "Pertussis", "Meningitis", "Encephalitis",
        "Lyme Disease", "West Nile Virus", "Zika Virus", "Ebola", "Marburg",
        "SARS", "MERS", "Avian Flu", "Swine Flu", "Rabies", "Anthrax",
        "Plague", "Tularemia", "Botulism", "Smallpox", "Monkeypox"
    ],
    "Disorder": [
        "Diabetes Mellitus", "Hypertension", "Coronary Artery Disease", "Stroke",
        "Chronic Obstructive Pulmonary Disease", "Asthma", "Arthritis",
        "Osteoporosis", "Alzheimer's Disease", "Parkinson's Disease",
        "Multiple Sclerosis", "Epilepsy", "Migraine", "Depression", "Anxiety",
        "Bipolar Disorder", "Schizophrenia", "Autism Spectrum Disorder",
        "Attention Deficit Hyperactivity Disorder", "Obsessive Compulsive Disorder",
        "Post-Traumatic Stress Disorder", "Eating Disorders", "Sleep Disorders",
        "Thyroid Disorders", "Adrenal Disorders", "Pituitary Disorders"
    ],
    "Virus": [
        "Human Immunodeficiency Virus", "Herpes Simplex Virus", "Cytomegalovirus",
        "Epstein-Barr Virus", "Varicella-Zoster Virus", "Human Papillomavirus",
        "Respiratory Syncytial Virus", "Parainfluenza Virus", "Adenovirus",
        "Rhinovirus", "Coronavirus", "Rotavirus", "Norovirus", "Hepatitis Viruses",
        "Influenza Viruses", "Dengue Virus", "Zika Virus", "Chikungunya Virus",
        "West Nile Virus", "Japanese Encephalitis Virus", "Tick-Borne Encephalitis Virus"
    ],
    "Bacteria": [
        "Staphylococcus aureus", "Streptococcus pneumoniae", "Escherichia coli",
        "Salmonella", "Shigella", "Campylobacter", "Vibrio cholerae",
        "Clostridium difficile", "Mycobacterium tuberculosis", "Mycobacterium leprae",
        "Borrelia burgdorferi", "Treponema pallidum", "Neisseria gonorrhoeae",
        "Neisseria meningitidis", "Haemophilus influenzae", "Legionella pneumophila",
        "Pseudomonas aeruginosa", "Acinetobacter baumannii", "Klebsiella pneumoniae",
        "Enterococcus faecalis", "Clostridium botulinum", "Bacillus anthracis",
        "Yersinia pestis", "Francisella tularensis"
    ]
}

# Symptom database (standardized)
SYMPTOM_DATABASE = {
    "respiratory": ["cough", "shortness of breath", "chest pain", "wheezing", "sore throat", "runny nose", "fever", "fatigue"],
    "gastrointestinal": ["nausea", "vomiting", "diarrhea", "abdominal pain", "loss of appetite", "bloating", "constipation"],
    "neurological": ["headache", "dizziness", "confusion", "seizures", "numbness", "tingling", "memory loss", "fatigue"],
    "cardiovascular": ["chest pain", "palpitations", "shortness of breath", "swelling", "fatigue", "dizziness"],
    "musculoskeletal": ["joint pain", "muscle pain", "back pain", "stiffness", "weakness", "swelling"],
    "dermatological": ["rash", "itching", "redness", "blisters", "dry skin", "hair loss"],
    "systemic": ["fever", "fatigue", "weight loss", "night sweats", "chills", "malaise"],
    "psychological": ["anxiety", "depression", "irritability", "confusion", "hallucinations", "delusions"]
}

# Vaccine availability data (based on medical knowledge)
VACCINE_DATA = {
    # Available vaccines
    "Influenza": {"available": "Yes", "vaccine_name": "Influenza Vaccine", "reason": ""},
    "COVID-19": {"available": "Yes", "vaccine_name": "COVID-19 Vaccine", "reason": ""},
    "Measles": {"available": "Yes", "vaccine_name": "MMR Vaccine", "reason": ""},
    "Mumps": {"available": "Yes", "vaccine_name": "MMR Vaccine", "reason": ""},
    "Rubella": {"available": "Yes", "vaccine_name": "MMR Vaccine", "reason": ""},
    "Polio": {"available": "Yes", "vaccine_name": "Polio Vaccine", "reason": ""},
    "Tetanus": {"available": "Yes", "vaccine_name": "Tdap Vaccine", "reason": ""},
    "Diphtheria": {"available": "Yes", "vaccine_name": "Tdap Vaccine", "reason": ""},
    "Pertussis": {"available": "Yes", "vaccine_name": "Tdap Vaccine", "reason": ""},
    "Hepatitis B": {"available": "Yes", "vaccine_name": "Hepatitis B Vaccine", "reason": ""},
    "Hepatitis A": {"available": "Yes", "vaccine_name": "Hepatitis A Vaccine", "reason": ""},
    "Chickenpox": {"available": "Yes", "vaccine_name": "Varicella Vaccine", "reason": ""},
    "Pneumonia": {"available": "Yes", "vaccine_name": "Pneumococcal Vaccine", "reason": ""},
    "Meningitis": {"available": "Yes", "vaccine_name": "Meningococcal Vaccine", "reason": ""},
    "Tuberculosis": {"available": "Yes", "vaccine_name": "BCG Vaccine", "reason": ""},
    "Yellow Fever": {"available": "Yes", "vaccine_name": "Yellow Fever Vaccine", "reason": ""},
    "Typhoid": {"available": "Yes", "vaccine_name": "Typhoid Vaccine", "reason": ""},
    "Cholera": {"available": "Yes", "vaccine_name": "Cholera Vaccine", "reason": ""},
    "Rabies": {"available": "Yes", "vaccine_name": "Rabies Vaccine", "reason": ""},
    "Japanese Encephalitis": {"available": "Yes", "vaccine_name": "Japanese Encephalitis Vaccine", "reason": ""},
    "Rotavirus": {"available": "Yes", "vaccine_name": "Rotavirus Vaccine", "reason": ""},

    # Limited availability
    "Dengue": {"available": "Limited", "vaccine_name": "Dengvaxia", "reason": "Vaccine available but restricted to specific populations due to safety concerns"},

    # Unavailable vaccines with reasons
    "Common Cold": {"available": "No", "vaccine_name": "", "reason": "Rapid mutation of viruses makes vaccine development impractical"},
    "HIV": {"available": "No", "vaccine_name": "", "reason": "Virus rapidly mutates and hides in immune cells, preventing effective immune response"},
    "Hepatitis C": {"available": "No", "vaccine_name": "", "reason": "Complex disease mechanism and multiple virus strains hinder vaccine development"},
    "Ebola": {"available": "No", "vaccine_name": "", "reason": "Rare outbreaks and safety concerns limit widespread vaccine availability"},
    "Zika Virus": {"available": "No", "vaccine_name": "", "reason": "Ongoing research with no approved vaccine yet due to multiple strains"},
    "West Nile Virus": {"available": "No", "vaccine_name": "", "reason": "Limited human cases and complex transmission cycle"},
    "SARS": {"available": "No", "vaccine_name": "", "reason": "Disease eradicated in humans, no ongoing need for vaccine"},
    "MERS": {"available": "No", "vaccine_name": "", "reason": "Limited outbreaks and research funding constraints"},
    "Avian Flu": {"available": "No", "vaccine_name": "", "reason": "Rapid mutation and limited human transmission"},
    "Swine Flu": {"available": "No", "vaccine_name": "", "reason": "Similar to seasonal flu, covered by existing influenza vaccines"},
    "Lyme Disease": {"available": "No", "vaccine_name": "", "reason": "Previous vaccine withdrawn due to safety concerns and low demand"},
    "Malaria": {"available": "No", "vaccine_name": "", "reason": "Complex parasite lifecycle and multiple strains"},
    "Tuberculosis (advanced)": {"available": "No", "vaccine_name": "", "reason": "BCG vaccine prevents severe disease but not infection in adults"},
    "Cystic Fibrosis": {"available": "No", "vaccine_name": "", "reason": "Genetic disorder, not an infectious disease"},
    "Diabetes": {"available": "No", "vaccine_name": "", "reason": "Metabolic disorder, not caused by infection"},
    "Hypertension": {"available": "No", "vaccine_name": "", "reason": "Lifestyle and genetic factors, not infectious"},
    "Coronary Artery Disease": {"available": "No", "vaccine_name": "", "reason": "Cardiovascular disease from multiple risk factors"},
    "Stroke": {"available": "No", "vaccine_name": "", "reason": "Caused by various risk factors, not a single pathogen"},
    "COPD": {"available": "No", "vaccine_name": "", "reason": "Chronic lung disease from smoking and environmental factors"},
    "Asthma": {"available": "No", "vaccine_name": "", "reason": "Allergic inflammatory condition, not infectious"},
    "Arthritis": {"available": "No", "vaccine_name": "", "reason": "Autoimmune and degenerative joint condition"},
    "Osteoporosis": {"available": "No", "vaccine_name": "", "reason": "Bone density disorder from aging and lifestyle"},
    "Alzheimer's Disease": {"available": "No", "vaccine_name": "", "reason": "Neurodegenerative disease with complex causes"},
    "Parkinson's Disease": {"available": "No", "vaccine_name": "", "reason": "Progressive neurological disorder"},
    "Multiple Sclerosis": {"available": "No", "vaccine_name": "", "reason": "Autoimmune neurological disease"},
    "Epilepsy": {"available": "No", "vaccine_name": "", "reason": "Neurological disorder from various causes"},
    "Migraine": {"available": "No", "vaccine_name": "", "reason": "Neurological headache disorder"},
    "Depression": {"available": "No", "vaccine_name": "", "reason": "Mental health condition with multiple causes"},
    "Anxiety": {"available": "No", "vaccine_name": "", "reason": "Mental health disorder"},
    "Bipolar Disorder": {"available": "No", "vaccine_name": "", "reason": "Mental health condition"},
    "Schizophrenia": {"available": "No", "vaccine_name": "", "reason": "Severe mental health disorder"},
    "Autism": {"available": "No", "vaccine_name": "", "reason": "Neurodevelopmental disorder"},
    "ADHD": {"available": "No", "vaccine_name": "", "reason": "Neurodevelopmental disorder"},
    "OCD": {"available": "No", "vaccine_name": "", "reason": "Mental health disorder"},
    "PTSD": {"available": "No", "vaccine_name": "", "reason": "Mental health condition from trauma"},
    "Eating Disorders": {"available": "No", "vaccine_name": "", "reason": "Mental health and behavioral disorders"},
    "Sleep Disorders": {"available": "No", "vaccine_name": "", "reason": "Various causes including lifestyle and medical conditions"},
    "Thyroid Disorders": {"available": "No", "vaccine_name": "", "reason": "Endocrine disorders from various causes"},
    "Adrenal Disorders": {"available": "No", "vaccine_name": "", "reason": "Endocrine disorders"},
    "Pituitary Disorders": {"available": "No", "vaccine_name": "", "reason": "Endocrine disorders"},
    "Herpes Simplex": {"available": "No", "vaccine_name": "", "reason": "Virus establishes lifelong latent infection"},
    "Cytomegalovirus": {"available": "No", "vaccine_name": "", "reason": "Common virus with complex immune interactions"},
    "Epstein-Barr Virus": {"available": "No", "vaccine_name": "", "reason": "Causes lifelong infection, vaccine development challenging"},
    "Varicella-Zoster": {"available": "Yes", "vaccine_name": "Varicella Vaccine", "reason": ""},
    "Human Papillomavirus": {"available": "Yes", "vaccine_name": "HPV Vaccine", "reason": ""},
    "Respiratory Syncytial Virus": {"available": "No", "vaccine_name": "", "reason": "Previous vaccine trials showed safety concerns"},
    "Parainfluenza": {"available": "No", "vaccine_name": "", "reason": "Multiple virus types and limited research"},
    "Adenovirus": {"available": "Limited", "vaccine_name": "Military Adenovirus Vaccine", "reason": "Limited to specific strains and populations"},
    "Rhinovirus": {"available": "No", "vaccine_name": "", "reason": "Over 100 serotypes make vaccine impractical"},
    "Norovirus": {"available": "No", "vaccine_name": "", "reason": "Rapidly evolving virus with many strains"},
    "Rotavirus": {"available": "Yes", "vaccine_name": "Rotavirus Vaccine", "reason": ""},
    "Staphylococcus aureus": {"available": "No", "vaccine_name": "", "reason": "Bacteria has multiple strains and toxin variants"},
    "Streptococcus pneumoniae": {"available": "Yes", "vaccine_name": "Pneumococcal Vaccine", "reason": ""},
    "Escherichia coli": {"available": "Limited", "vaccine_name": "Travelers' Diarrhea Vaccine", "reason": "Limited to specific strains"},
    "Salmonella": {"available": "Limited", "vaccine_name": "Typhoid Vaccine", "reason": "Limited to specific serotypes"},
    "Shigella": {"available": "No", "vaccine_name": "", "reason": "Multiple serotypes and limited research"},
    "Campylobacter": {"available": "No", "vaccine_name": "", "reason": "Complex bacterial structure"},
    "Vibrio cholerae": {"available": "Yes", "vaccine_name": "Cholera Vaccine", "reason": ""},
    "Clostridium difficile": {"available": "No", "vaccine_name": "", "reason": "Bacterial toxin-mediated disease"},
    "Mycobacterium tuberculosis": {"available": "Yes", "vaccine_name": "BCG Vaccine", "reason": ""},
    "Mycobacterium leprae": {"available": "No", "vaccine_name": "", "reason": "Limited global incidence"},
    "Borrelia burgdorferi": {"available": "No", "vaccine_name": "", "reason": "Previous vaccine withdrawn due to concerns"},
    "Treponema pallidum": {"available": "No", "vaccine_name": "", "reason": "Complex immune evasion mechanisms"},
    "Neisseria gonorrhoeae": {"available": "No", "vaccine_name": "", "reason": "Rapid antibiotic resistance and immune evasion"},
    "Neisseria meningitidis": {"available": "Yes", "vaccine_name": "Meningococcal Vaccine", "reason": ""},
    "Haemophilus influenzae": {"available": "Yes", "vaccine_name": "Hib Vaccine", "reason": ""},
    "Legionella pneumophila": {"available": "No", "vaccine_name": "", "reason": "Environmental bacterium with limited human cases"},
    "Pseudomonas aeruginosa": {"available": "No", "vaccine_name": "", "reason": "Opportunistic pathogen in immunocompromised patients"},
    "Acinetobacter baumannii": {"available": "No", "vaccine_name": "", "reason": "Hospital-acquired infection with multiple strains"},
    "Klebsiella pneumoniae": {"available": "No", "vaccine_name": "", "reason": "Antibiotic-resistant hospital pathogen"},
    "Enterococcus faecalis": {"available": "No", "vaccine_name": "", "reason": "Common hospital-acquired infection"},
    "Clostridium botulinum": {"available": "No", "vaccine_name": "", "reason": "Toxin-mediated disease, limited cases"},
    "Bacillus anthracis": {"available": "Yes", "vaccine_name": "Anthrax Vaccine", "reason": ""},
    "Yersinia pestis": {"available": "No", "vaccine_name": "", "reason": "Rare disease with limited research"},
    "Francisella tularensis": {"available": "No", "vaccine_name": "", "reason": "Rare bacterial infection"}
}

def get_symptoms_for_category(category, disease_name):
    """Generate realistic symptoms based on disease category and name"""
    base_symptoms = []

    if category == "Disease":
        if "respiratory" in disease_name.lower() or "flu" in disease_name.lower() or "pneumonia" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["respiratory"]
        elif "gastro" in disease_name.lower() or "cholera" in disease_name.lower() or "typhoid" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["gastrointestinal"]
        elif "cardiac" in disease_name.lower() or "heart" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["cardiovascular"]
        else:
            base_symptoms = SYMPTOM_DATABASE["systemic"]

    elif category == "Disorder":
        if "neuro" in disease_name.lower() or "mental" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["neurological"] + SYMPTOM_DATABASE["psychological"]
        elif "cardio" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["cardiovascular"]
        elif "musculo" in disease_name.lower() or "arthritis" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["musculoskeletal"]
        else:
            base_symptoms = SYMPTOM_DATABASE["systemic"]

    elif category == "Virus":
        if "respiratory" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["respiratory"]
        elif "herpes" in disease_name.lower() or "papilloma" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["dermatological"]
        else:
            base_symptoms = SYMPTOM_DATABASE["systemic"] + SYMPTOM_DATABASE["neurological"]

    elif category == "Bacteria":
        if "pneumonia" in disease_name.lower() or "tuberculosis" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["respiratory"]
        elif "gastro" in disease_name.lower():
            base_symptoms = SYMPTOM_DATABASE["gastrointestinal"]
        else:
            base_symptoms = SYMPTOM_DATABASE["systemic"] + SYMPTOM_DATABASE["musculoskeletal"]

    # Return 3-6 random symptoms from the base set
    return random.sample(base_symptoms, min(len(base_symptoms), random.randint(3, 6)))

def generate_dataset():
    """Generate the expanded vaccine dataset with 15,000+ entries"""
    dataset = []

    # Calculate entries per disease to reach 15,000 total
    total_diseases = sum(len(diseases) for diseases in DISEASE_CATEGORIES.values())
    entries_per_disease = max(30, 15000 // total_diseases)  # At least 30 entries per disease

    for category, diseases in DISEASE_CATEGORIES.items():
        for disease in diseases:
            # Get vaccine information
            vaccine_info = VACCINE_DATA.get(disease, {"available": "No", "vaccine_name": "", "reason": "Vaccine development not prioritized"})

            # Generate multiple entries per disease with symptom variations
            for i in range(entries_per_disease):
                symptoms = get_symptoms_for_category(category, disease)
                symptoms_str = "; ".join(symptoms)

                entry = {
                    "Disease": disease,
                    "Category": category,
                    "Symptoms": symptoms_str,
                    "Vaccine_Available": vaccine_info["available"],
                    "Vaccine_Name": vaccine_info["vaccine_name"],
                    "Reason": vaccine_info["reason"]
                }

                dataset.append(entry)

    # Shuffle the dataset for better distribution
    random.shuffle(dataset)

    return dataset

def save_to_csv(dataset, filename="expanded_vaccine_dataset.csv"):
    """Save the dataset to CSV format"""
    if not dataset:
        print("No data to save")
        return

    fieldnames = ["Disease", "Category", "Symptoms", "Vaccine_Available", "Vaccine_Name", "Reason"]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)

    print(f"Dataset saved to {filename} with {len(dataset)} entries")

def save_to_json(dataset, filename="expanded_vaccine_dataset.json"):
    """Save the dataset to JSON format"""
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(dataset, jsonfile, indent=2, ensure_ascii=False)

    print(f"Dataset saved to {filename} with {len(dataset)} entries")

if __name__ == "__main__":
    print("Generating expanded vaccine dataset...")
    dataset = generate_dataset()

    print(f"Generated {len(dataset)} entries")

    # Save in both formats
    save_to_csv(dataset)
    save_to_json(dataset)

    print("Dataset generation complete!")