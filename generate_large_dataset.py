import csv
import random
import json
from collections import defaultdict

# Comprehensive medical dataset generator inspired by Kaggle datasets
# Generates 15,000+ entries for disease prediction training

class MedicalDatasetGenerator:
    def __init__(self):
        self.diseases_data = self._load_disease_templates()
        self.generated_entries = []

    def _load_disease_templates(self):
        """Load comprehensive disease templates with medical accuracy"""
        return {
            # ===== INFECTIOUS DISEASES =====
            "Influenza": {
                "category": "Virus",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fever", "cough", "sore throat", "fatigue", "body aches", "headache"],
                "additional_symptoms": ["chills", "runny nose", "sneezing", "loss of appetite", "muscle weakness"],
                "causes": ["Influenza A virus", "Influenza B virus", "seasonal transmission", "airborne droplets"]
            },
            "COVID-19": {
                "category": "Virus",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fever", "cough", "fatigue", "loss of taste", "loss of smell"],
                "additional_symptoms": ["shortness of breath", "sore throat", "headache", "body aches", "diarrhea", "nausea"],
                "causes": ["SARS-CoV-2 virus", "respiratory droplets", "surface contamination", "asymptomatic transmission"]
            },
            "Pneumonia": {
                "category": "Bacteria",
                "severity": ["Medium", "High"],
                "base_symptoms": ["cough", "fever", "shortness of breath", "chest pain"],
                "additional_symptoms": ["fatigue", "nausea", "vomiting", "diarrhea", "confusion", "rapid heartbeat"],
                "causes": ["Streptococcus pneumoniae", "Haemophilus influenzae", "viral infection", "aspiration"]
            },
            "Tuberculosis": {
                "category": "Bacteria",
                "severity": ["Medium", "High"],
                "base_symptoms": ["persistent cough", "weight loss", "night sweats", "fatigue"],
                "additional_symptoms": ["fever", "chest pain", "coughing up blood", "loss of appetite", "chills"],
                "causes": ["Mycobacterium tuberculosis", "airborne transmission", "latent infection reactivation"]
            },
            "Malaria": {
                "category": "Parasite",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fever", "chills", "headache", "fatigue"],
                "additional_symptoms": ["nausea", "vomiting", "diarrhea", "abdominal pain", "muscle pain", "sweating"],
                "causes": ["Plasmodium parasites", "mosquito bites", "Anopheles mosquito vector"]
            },
            "Dengue Fever": {
                "category": "Virus",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["high fever", "severe headache", "pain behind eyes", "joint pain"],
                "additional_symptoms": ["muscle pain", "rash", "nausea", "vomiting", "fatigue", "bleeding gums"],
                "causes": ["Dengue virus", "Aedes mosquito bites", "urban transmission"]
            },
            "Cholera": {
                "category": "Bacteria",
                "severity": ["High"],
                "base_symptoms": ["severe diarrhea", "vomiting", "dehydration"],
                "additional_symptoms": ["muscle cramps", "rapid heartbeat", "low blood pressure", "dry mouth"],
                "causes": ["Vibrio cholerae", "contaminated water", "poor sanitation", "raw shellfish"]
            },
            "Typhoid Fever": {
                "category": "Bacteria",
                "severity": ["Medium", "High"],
                "base_symptoms": ["persistent fever", "headache", "fatigue", "abdominal pain"],
                "additional_symptoms": ["loss of appetite", "rash", "constipation", "cough", "weakness"],
                "causes": ["Salmonella typhi", "contaminated food/water", "poor hygiene"]
            },
            "Hepatitis A": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fatigue", "nausea", "abdominal pain", "loss of appetite"],
                "additional_symptoms": ["fever", "dark urine", "clay-colored stools", "jaundice", "joint pain"],
                "causes": ["Hepatitis A virus", "contaminated food/water", "close contact"]
            },
            "Hepatitis B": {
                "category": "Virus",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fatigue", "abdominal pain", "loss of appetite", "nausea"],
                "additional_symptoms": ["jaundice", "dark urine", "joint pain", "fever", "vomiting"],
                "causes": ["Hepatitis B virus", "blood contact", "sexual transmission", "mother-to-child"]
            },
            "HIV/AIDS": {
                "category": "Virus",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fatigue", "weight loss", "fever", "night sweats"],
                "additional_symptoms": ["swollen lymph nodes", "diarrhea", "oral thrush", "persistent cough", "skin rashes"],
                "causes": ["Human Immunodeficiency Virus", "unprotected sex", "shared needles", "blood transfusion"]
            },
            "Ebola": {
                "category": "Virus",
                "severity": ["High"],
                "base_symptoms": ["fever", "severe headache", "muscle pain", "fatigue"],
                "additional_symptoms": ["diarrhea", "vomiting", "abdominal pain", "unexplained bleeding", "rash"],
                "causes": ["Ebolavirus", "contact with infected fluids", "animal transmission", "nosocomial spread"]
            },
            "Zika Virus": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "rash", "joint pain", "conjunctivitis"],
                "additional_symptoms": ["headache", "muscle pain", "fatigue", "swollen lymph nodes"],
                "causes": ["Zika virus", "Aedes mosquito bites", "sexual transmission", "vertical transmission"]
            },
            "Measles": {
                "category": "Virus",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fever", "cough", "runny nose", "rash"],
                "additional_symptoms": ["red eyes", "sore throat", "white spots in mouth", "fatigue"],
                "causes": ["Measles virus", "airborne droplets", "unvaccinated populations"]
            },
            "Mumps": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["swollen salivary glands", "fever", "headache"],
                "additional_symptoms": ["fatigue", "loss of appetite", "muscle pain", "testicle pain"],
                "causes": ["Mumps virus", "respiratory droplets", "close contact"]
            },
            "Rubella": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "rash", "swollen lymph nodes"],
                "additional_symptoms": ["joint pain", "headache", "runny nose", "red eyes"],
                "causes": ["Rubella virus", "respiratory droplets", "congenital transmission"]
            },
            "Chickenpox": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "rash", "itching"],
                "additional_symptoms": ["fatigue", "loss of appetite", "headache", "mild cough"],
                "causes": ["Varicella-zoster virus", "airborne transmission", "direct contact"]
            },
            "Shingles": {
                "category": "Virus",
                "severity": ["Medium"],
                "base_symptoms": ["painful rash", "burning sensation", "itching"],
                "additional_symptoms": ["fever", "headache", "fatigue", "sensitivity to touch"],
                "causes": ["Reactivation of Varicella-zoster virus", "stress", "immune suppression"]
            },
            "Norovirus": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["nausea", "vomiting", "diarrhea", "stomach pain"],
                "additional_symptoms": ["fever", "headache", "body aches", "fatigue"],
                "causes": ["Norovirus", "contaminated food/water", "close contact", "fecal-oral route"]
            },
            "Rotavirus": {
                "category": "Virus",
                "severity": ["Medium"],
                "base_symptoms": ["severe diarrhea", "vomiting", "fever"],
                "additional_symptoms": ["abdominal pain", "dehydration", "loss of appetite"],
                "causes": ["Rotavirus", "fecal-oral transmission", "contaminated surfaces"]
            },

            # ===== BACTERIAL INFECTIONS =====
            "Strep Throat": {
                "category": "Bacteria",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["sore throat", "fever", "swollen lymph nodes"],
                "additional_symptoms": ["difficulty swallowing", "red throat", "white patches", "rash"],
                "causes": ["Streptococcus pyogenes", "droplet transmission", "direct contact"]
            },
            "Urinary Tract Infection": {
                "category": "Bacteria",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["frequent urination", "burning sensation", "lower abdominal pain"],
                "additional_symptoms": ["cloudy urine", "blood in urine", "fever", "nausea"],
                "causes": ["Escherichia coli", "poor hygiene", "sexual activity", "catheter use"]
            },
            "Salmonella Infection": {
                "category": "Bacteria",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["diarrhea", "fever", "abdominal cramps"],
                "additional_symptoms": ["nausea", "vomiting", "headache", "blood in stool"],
                "causes": ["Salmonella bacteria", "contaminated food", "undercooked poultry", "raw eggs"]
            },
            "Lyme Disease": {
                "category": "Bacteria",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["bull's-eye rash", "fever", "fatigue"],
                "additional_symptoms": ["headache", "joint pain", "muscle pain", "swollen lymph nodes"],
                "causes": ["Borrelia burgdorferi", "deer tick bites", "outdoor activities"]
            },
            "Tetanus": {
                "category": "Bacteria",
                "severity": ["High"],
                "base_symptoms": ["muscle stiffness", "lockjaw", "difficulty swallowing"],
                "additional_symptoms": ["muscle spasms", "sweating", "fever", "rapid heartbeat"],
                "causes": ["Clostridium tetani", "wound contamination", "rusty nails", "deep cuts"]
            },
            "Pertussis": {
                "category": "Bacteria",
                "severity": ["Medium", "High"],
                "base_symptoms": ["severe coughing fits", "whooping sound", "runny nose"],
                "additional_symptoms": ["fever", "fatigue", "vomiting after coughing"],
                "causes": ["Bordetella pertussis", "respiratory droplets", "close contact"]
            },
            "Meningitis": {
                "category": "Bacteria",
                "severity": ["High"],
                "base_symptoms": ["severe headache", "fever", "stiff neck"],
                "additional_symptoms": ["nausea", "vomiting", "sensitivity to light", "confusion", "seizures"],
                "causes": ["Neisseria meningitidis", "Streptococcus pneumoniae", "Haemophilus influenzae", "viral infection"]
            },
            "Cellulitis": {
                "category": "Bacteria",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["red skin", "swelling", "warmth", "pain"],
                "additional_symptoms": ["fever", "chills", "red streaks", "blisters"],
                "causes": ["Staphylococcus aureus", "Streptococcus species", "skin breaks", "insect bites"]
            },
            "Gonorrhea": {
                "category": "Bacteria",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["painful urination", "discharge", "pelvic pain"],
                "additional_symptoms": ["fever", "nausea", "bleeding between periods", "testicle pain"],
                "causes": ["Neisseria gonorrhoeae", "sexual transmission", "asymptomatic carriers"]
            },
            "Syphilis": {
                "category": "Bacteria",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["chancre sore", "rash", "fatigue"],
                "additional_symptoms": ["fever", "swollen lymph nodes", "hair loss", "joint pain"],
                "causes": ["Treponema pallidum", "sexual contact", "congenital transmission"]
            },

            # ===== CHRONIC DISEASES =====
            "Diabetes Type 1": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["frequent urination", "increased thirst", "extreme hunger"],
                "additional_symptoms": ["fatigue", "slow-healing sores", "frequent infections", "blurred vision", "tingling hands/feet"],
                "causes": ["Autoimmune destruction of insulin-producing cells", "genetic predisposition", "environmental triggers"]
            },
            "Diabetes Type 2": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["frequent urination", "increased thirst", "fatigue"],
                "additional_symptoms": ["slow-healing sores", "frequent infections", "blurred vision", "tingling hands/feet", "darkened skin"],
                "causes": ["Insulin resistance", "obesity", "sedentary lifestyle", "genetic factors", "aging"]
            },
            "Hypertension": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["headache", "dizziness", "blurred vision"],
                "additional_symptoms": ["chest pain", "shortness of breath", "nosebleeds", "fatigue"],
                "causes": ["genetic factors", "obesity", "high salt intake", "stress", "kidney disease", "hormonal disorders"]
            },
            "Coronary Artery Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["chest pain", "shortness of breath", "fatigue"],
                "additional_symptoms": ["dizziness", "nausea", "sweating", "arm/shoulder pain"],
                "causes": ["atherosclerosis", "high cholesterol", "hypertension", "smoking", "diabetes", "family history"]
            },
            "Asthma": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["wheezing", "coughing", "shortness of breath"],
                "additional_symptoms": ["chest tightness", "fatigue", "difficulty sleeping", "anxiety"],
                "causes": ["genetic predisposition", "environmental allergens", "air pollution", "respiratory infections", "stress"]
            },
            "Chronic Obstructive Pulmonary Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["chronic cough", "shortness of breath", "wheezing"],
                "additional_symptoms": ["chest tightness", "fatigue", "frequent respiratory infections", "weight loss"],
                "causes": ["long-term smoking", "air pollution", "genetic factors", "occupational exposure", "childhood respiratory infections"]
            },
            "Arthritis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["joint pain", "stiffness", "swelling"],
                "additional_symptoms": ["reduced range of motion", "fatigue", "fever", "weight loss"],
                "causes": ["wear and tear", "autoimmune response", "infection", "crystal deposits", "genetic factors"]
            },
            "Osteoporosis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["back pain", "loss of height", "stooped posture"],
                "additional_symptoms": ["bone fractures", "neck pain", "hip pain"],
                "causes": ["aging", "hormonal changes", "calcium deficiency", "vitamin D deficiency", "sedentary lifestyle"]
            },
            "Alzheimer's Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["memory loss", "confusion", "difficulty with familiar tasks"],
                "additional_symptoms": ["mood changes", "disorientation", "difficulty communicating", "poor judgment"],
                "causes": ["genetic factors", "age", "family history", "head trauma", "cardiovascular disease"]
            },
            "Parkinson's Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["tremor", "stiffness", "bradykinesia"],
                "additional_symptoms": ["balance problems", "difficulty walking", "speech changes", "depression"],
                "causes": ["genetic factors", "environmental toxins", "age", "head trauma", "oxidative stress"]
            },
            "Multiple Sclerosis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fatigue", "difficulty walking", "numbness"],
                "additional_symptoms": ["vision problems", "pain", "cognitive changes", "bladder problems"],
                "causes": ["autoimmune response", "genetic predisposition", "environmental factors", "viral infections"]
            },
            "Epilepsy": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["seizures", "confusion", "loss of consciousness"],
                "additional_symptoms": ["muscle spasms", "staring spells", "unusual sensations", "fatigue"],
                "causes": ["genetic factors", "brain injury", "stroke", "brain tumors", "infections"]
            },
            "Migraine": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["severe headache", "nausea", "sensitivity to light"],
                "additional_symptoms": ["vomiting", "aura", "fatigue", "neck stiffness"],
                "causes": ["genetic factors", "hormonal changes", "stress", "certain foods", "environmental triggers"]
            },
            "Irritable Bowel Syndrome": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "bloating", "gas"],
                "additional_symptoms": ["diarrhea", "constipation", "fatigue", "anxiety"],
                "causes": ["abnormal gut motility", "visceral hypersensitivity", "stress", "diet", "infection"]
            },
            "Chronic Kidney Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fatigue", "swelling", "poor appetite"],
                "additional_symptoms": ["difficulty concentrating", "sleep problems", "muscle cramps", "itchy skin"],
                "causes": ["diabetes", "hypertension", "glomerulonephritis", "polycystic kidney disease", "prolonged obstruction"]
            },
            "Liver Cirrhosis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fatigue", "easy bruising", "loss of appetite"],
                "additional_symptoms": ["jaundice", "swelling", "confusion", "vomiting blood"],
                "causes": ["chronic alcohol abuse", "hepatitis B/C", "fatty liver disease", "autoimmune hepatitis"]
            },

            # ===== MENTAL HEALTH DISORDERS =====
            "Depression": {
                "category": "Disorder",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["persistent sadness", "loss of interest", "fatigue"],
                "additional_symptoms": ["sleep disturbances", "appetite changes", "difficulty concentrating", "feelings of worthlessness"],
                "causes": ["genetic factors", "brain chemistry", "stress", "trauma", "medical conditions", "substance abuse"]
            },
            "Anxiety Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["excessive worry", "restlessness", "rapid heartbeat"],
                "additional_symptoms": ["sweating", "trembling", "weakness", "difficulty concentrating", "sleep problems"],
                "causes": ["genetic factors", "brain chemistry", "stress", "trauma", "caffeine", "medical conditions"]
            },
            "Bipolar Disorder": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["mood swings", "elevated mood", "depressed mood"],
                "additional_symptoms": ["increased energy", "decreased need for sleep", "racing thoughts", "impulsive behavior"],
                "causes": ["genetic factors", "brain chemistry", "stress", "trauma", "substance abuse"]
            },
            "Schizophrenia": {
                "category": "Disorder",
                "severity": ["High"],
                "base_symptoms": ["hallucinations", "delusions", "disorganized thinking"],
                "additional_symptoms": ["lack of motivation", "poor hygiene", "social withdrawal", "cognitive difficulties"],
                "causes": ["genetic factors", "brain chemistry", "prenatal exposure", "stress", "substance abuse"]
            },
            "Post-Traumatic Stress Disorder": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["flashbacks", "nightmares", "avoidance"],
                "additional_symptoms": ["hypervigilance", "irritability", "sleep problems", "emotional numbness"],
                "causes": ["trauma", "abuse", "violence", "accidents", "natural disasters", "combat"]
            },
            "Obsessive-Compulsive Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["obsessive thoughts", "compulsive behaviors", "anxiety"],
                "additional_symptoms": ["time-consuming rituals", "interference with daily life", "distress"],
                "causes": ["genetic factors", "brain chemistry", "learned behavior", "stress", "trauma"]
            },
            "Attention Deficit Hyperactivity Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["inattention", "hyperactivity", "impulsivity"],
                "additional_symptoms": ["disorganization", "forgetfulness", "fidgeting", "interrupting others"],
                "causes": ["genetic factors", "brain chemistry", "prenatal exposure", "low birth weight", "environmental factors"]
            },

            # ===== RARE DISEASES =====
            "Cystic Fibrosis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["chronic cough", "recurrent lung infections", "poor weight gain"],
                "additional_symptoms": ["salty skin", "fatty stools", "shortness of breath", "infertility"],
                "causes": ["genetic mutation", "CFTR gene defect", "autosomal recessive inheritance"]
            },
            "Sickle Cell Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["pain episodes", "fatigue", "jaundice"],
                "additional_symptoms": ["swelling", "frequent infections", "delayed growth", "vision problems"],
                "causes": ["genetic mutation", "hemoglobin S", "autosomal recessive inheritance"]
            },
            "Huntington's Disease": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["uncontrolled movements", "cognitive decline", "emotional disturbances"],
                "additional_symptoms": ["difficulty swallowing", "weight loss", "depression", "irritability"],
                "causes": ["genetic mutation", "HTT gene expansion", "autosomal dominant inheritance"]
            },
            "Amyotrophic Lateral Sclerosis": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["muscle weakness", "difficulty speaking", "difficulty swallowing"],
                "additional_symptoms": ["muscle twitching", "fatigue", "emotional changes", "cognitive changes"],
                "causes": ["unknown", "genetic factors", "environmental factors", "military service"]
            },
            "Duchenne Muscular Dystrophy": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["muscle weakness", "difficulty walking", "frequent falls"],
                "additional_symptoms": ["delayed motor milestones", "calf muscle enlargement", "learning difficulties"],
                "causes": ["genetic mutation", "dystrophin gene", "X-linked recessive inheritance"]
            },

            # ===== EMERGING DISEASES =====
            "Monkeypox": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "rash", "swollen lymph nodes"],
                "additional_symptoms": ["headache", "muscle aches", "fatigue", "back pain"],
                "causes": ["Monkeypox virus", "contact with infected animals", "human-to-human transmission"]
            },
            "Avian Influenza": {
                "category": "Virus",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fever", "cough", "sore throat"],
                "additional_symptoms": ["shortness of breath", "muscle aches", "fatigue", "conjunctivitis"],
                "causes": ["Avian influenza viruses", "contact with infected birds", "zoonotic transmission"]
            },
            "Middle East Respiratory Syndrome": {
                "category": "Virus",
                "severity": ["High"],
                "base_symptoms": ["fever", "cough", "shortness of breath"],
                "additional_symptoms": ["diarrhea", "nausea", "vomiting", "abdominal pain"],
                "causes": ["MERS-CoV virus", "contact with infected camels", "nosocomial transmission"]
            },

            # ===== SKIN CONDITIONS =====
            "Acne": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["pimples", "blackheads", "whiteheads"],
                "additional_symptoms": ["oily skin", "scarring", "inflammation", "pain"],
                "causes": ["hormonal changes", "excess sebum", "clogged pores", "bacterial infection"]
            },
            "Eczema": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["itchy skin", "red patches", "dry skin"],
                "additional_symptoms": ["swelling", "cracking", "oozing", "thickened skin"],
                "causes": ["genetic factors", "immune system dysfunction", "environmental triggers", "stress"]
            },
            "Psoriasis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["red patches", "silvery scales", "itchy skin"],
                "additional_symptoms": ["dry skin", "cracking", "bleeding", "joint pain"],
                "causes": ["immune system dysfunction", "genetic factors", "stress", "infection", "medication"]
            },

            # ===== ENDOCRINE DISORDERS =====
            "Hypothyroidism": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fatigue", "weight gain", "cold intolerance"],
                "additional_symptoms": ["dry skin", "hair loss", "constipation", "depression", "memory problems"],
                "causes": ["autoimmune thyroiditis", "iodine deficiency", "thyroid surgery", "radiation therapy"]
            },
            "Hyperthyroidism": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["weight loss", "rapid heartbeat", "heat intolerance"],
                "additional_symptoms": ["tremor", "anxiety", "sweating", "diarrhea", "goiter"],
                "causes": ["Graves' disease", "toxic adenoma", "thyroiditis", "excess iodine", "medication"]
            },
            "Addison's Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fatigue", "weight loss", "low blood pressure"],
                "additional_symptoms": ["salt craving", "hyperpigmentation", "nausea", "dizziness"],
                "causes": ["autoimmune destruction", "infection", "cancer", "adrenal hemorrhage"]
            },

            # ===== BLOOD DISORDERS =====
            "Anemia": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fatigue", "weakness", "pale skin"],
                "additional_symptoms": ["shortness of breath", "dizziness", "cold hands/feet", "irregular heartbeat"],
                "causes": ["iron deficiency", "vitamin deficiency", "chronic disease", "blood loss", "bone marrow problems"]
            },
            "Thrombocytopenia": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["easy bruising", "nosebleeds", "prolonged bleeding"],
                "additional_symptoms": ["petechiae", "fatigue", "enlarged spleen", "fever"],
                "causes": ["immune thrombocytopenia", "drug-induced", "infection", "bone marrow disorders"]
            },

            # ===== NEUROLOGICAL DISORDERS =====
            "Stroke": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["sudden numbness", "confusion", "trouble speaking"],
                "additional_symptoms": ["vision problems", "difficulty walking", "severe headache", "dizziness"],
                "causes": ["ischemic stroke", "hemorrhagic stroke", "atherosclerosis", "hypertension", "atrial fibrillation"]
            },
            "Epilepsy": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["seizures", "loss of consciousness", "convulsions"],
                "additional_symptoms": ["confusion", "fatigue", "headache", "muscle pain"],
                "causes": ["genetic factors", "brain injury", "infection", "stroke", "brain tumors"]
            },
            "Dementia": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["memory loss", "confusion", "difficulty with familiar tasks"],
                "additional_symptoms": ["mood changes", "personality changes", "disorientation", "poor judgment"],
                "causes": ["Alzheimer's disease", "vascular dementia", "Lewy body dementia", "frontotemporal dementia"]
            },

            # ===== GASTROINTESTINAL DISORDERS =====
            "Gastroesophageal Reflux Disease": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["heartburn", "regurgitation", "chest pain"],
                "additional_symptoms": ["difficulty swallowing", "chronic cough", "hoarseness", "bad breath"],
                "causes": ["lower esophageal sphincter weakness", "hiatal hernia", "obesity", "pregnancy", "smoking"]
            },
            "Peptic Ulcer Disease": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "bloating", "nausea"],
                "additional_symptoms": ["vomiting", "weight loss", "loss of appetite", "dark stools"],
                "causes": ["Helicobacter pylori infection", "NSAID use", "stress", "smoking", "alcohol"]
            },
            "Inflammatory Bowel Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["abdominal pain", "diarrhea", "fatigue"],
                "additional_symptoms": ["weight loss", "fever", "rectal bleeding", "joint pain"],
                "causes": ["immune system dysfunction", "genetic factors", "environmental factors", "gut microbiome"]
            },

            # ===== UROLOGICAL DISORDERS =====
            "Kidney Stones": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["severe pain", "blood in urine", "nausea"],
                "additional_symptoms": ["vomiting", "frequent urination", "burning sensation", "fever"],
                "causes": ["dehydration", "high calcium", "high oxalate", "infection", "genetic factors"]
            },
            "Benign Prostatic Hyperplasia": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["frequent urination", "weak urine stream", "difficulty starting urination"],
                "additional_symptoms": ["nocturia", "urgency", "incomplete bladder emptying"],
                "causes": ["aging", "hormonal changes", "family history", "obesity", "diabetes"]
            },

            # ===== MUSCULOSKELETAL DISORDERS =====
            "Osteoarthritis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["joint pain", "stiffness", "reduced range of motion"],
                "additional_symptoms": ["swelling", "tenderness", "crepitus", "muscle weakness"],
                "causes": ["wear and tear", "aging", "joint injury", "obesity", "genetic factors"]
            },
            "Rheumatoid Arthritis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["joint pain", "swelling", "morning stiffness"],
                "additional_symptoms": ["fatigue", "fever", "weight loss", "nodules under skin"],
                "causes": ["autoimmune response", "genetic factors", "environmental triggers", "hormonal factors"]
            },
            "Gout": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["severe joint pain", "swelling", "redness"],
                "additional_symptoms": ["warmth", "tenderness", "limited range of motion", "fever"],
                "causes": ["high uric acid levels", "diet", "genetics", "medications", "obesity"]
            },

            # ===== RESPIRATORY DISORDERS =====
            "Allergic Rhinitis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["sneezing", "runny nose", "itchy nose"],
                "additional_symptoms": ["congestion", "itchy eyes", "postnasal drip", "fatigue"],
                "causes": ["pollen", "dust mites", "pet dander", "mold", "environmental allergens"]
            },
            "Sinusitis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["facial pain", "nasal congestion", "headache"],
                "additional_symptoms": ["thick nasal discharge", "cough", "fever", "fatigue"],
                "causes": ["viral infection", "bacterial infection", "allergic reaction", "anatomical abnormalities"]
            },
            "Bronchitis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["cough", "mucus production", "fatigue"],
                "additional_symptoms": ["chest discomfort", "shortness of breath", "fever", "wheezing"],
                "causes": ["viral infection", "bacterial infection", "smoking", "air pollution", "allergies"]
            },

            # ===== CARDIOVASCULAR DISORDERS =====
            "Atrial Fibrillation": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["irregular heartbeat", "palpitations", "fatigue"],
                "additional_symptoms": ["shortness of breath", "dizziness", "chest pain", "fainting"],
                "causes": ["hypertension", "heart disease", "thyroid problems", "sleep apnea", "alcohol"]
            },
            "Heart Failure": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["shortness of breath", "fatigue", "swelling"],
                "additional_symptoms": ["rapid heartbeat", "persistent cough", "weight gain", "reduced exercise tolerance"],
                "causes": ["coronary artery disease", "hypertension", "cardiomyopathy", "valve disease", "arrhythmia"]
            },
            "Peripheral Artery Disease": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["leg pain", "numbness", "weakness"],
                "additional_symptoms": ["cold feet", "slow-healing sores", "hair loss on legs", "skin discoloration"],
                "causes": ["atherosclerosis", "smoking", "diabetes", "hypertension", "high cholesterol"]
            },

            # ===== EMERGENCY CONDITIONS =====
            "Acute Myocardial Infarction": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["chest pain", "shortness of breath", "nausea"],
                "additional_symptoms": ["sweating", "lightheadedness", "pain radiating to arm/jaw", "anxiety"],
                "causes": ["coronary artery blockage", "atherosclerosis", "blood clot", "coronary spasm"]
            },
            "Pulmonary Embolism": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["sudden shortness of breath", "chest pain", "cough"],
                "additional_symptoms": ["rapid heartbeat", "dizziness", "fainting", "bloody sputum"],
                "causes": ["deep vein thrombosis", "blood clot in lungs", "immobility", "surgery", "cancer"]
            },
            "Acute Pancreatitis": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["severe abdominal pain", "nausea", "vomiting"],
                "additional_symptoms": ["fever", "rapid heartbeat", "tenderness", "jaundice"],
                "causes": ["gallstones", "alcohol abuse", "hypertriglyceridemia", "medications", "infection"]
            },
            "Appendicitis": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["abdominal pain", "nausea", "vomiting"],
                "additional_symptoms": ["fever", "loss of appetite", "constipation", "diarrhea"],
                "causes": ["appendix obstruction", "infection", "fecal matter", "foreign bodies"]
            },
            "Cholecystitis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["right upper abdominal pain", "fever", "nausea"],
                "additional_symptoms": ["vomiting", "tenderness", "jaundice", "chills"],
                "causes": ["gallstones", "gallbladder obstruction", "infection", "ischemia"]
            },

            # ===== PEDIATRIC CONDITIONS =====
            "Croup": {
                "category": "Virus",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["barking cough", "hoarse voice", "stridor"],
                "additional_symptoms": ["fever", "difficulty breathing", "restlessness"],
                "causes": ["parainfluenza virus", "respiratory syncytial virus", "influenza virus"]
            },
            "Kawasaki Disease": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["fever", "rash", "red eyes"],
                "additional_symptoms": ["swollen lymph nodes", "red lips/tongue", "swollen hands/feet", "peeling skin"],
                "causes": ["unknown", "immune system response", "possible viral trigger", "genetic predisposition"]
            },
            "Reye's Syndrome": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["vomiting", "confusion", "seizures"],
                "additional_symptoms": ["coma", "liver dysfunction", "brain swelling"],
                "causes": ["aspirin use in viral infection", "varicella virus", "influenza virus", "metabolic disorder"]
            },

            # ===== WOMEN'S HEALTH =====
            "Endometriosis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["pelvic pain", "painful periods", "pain during intercourse"],
                "additional_symptoms": ["heavy bleeding", "infertility", "fatigue", "bowel problems"],
                "causes": ["retrograde menstruation", "immune system dysfunction", "hormonal factors", "genetic factors"]
            },
            "Polycystic Ovary Syndrome": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["irregular periods", "excess hair growth", "weight gain"],
                "additional_symptoms": ["acne", "infertility", "hair loss", "dark skin patches"],
                "causes": ["hormonal imbalance", "insulin resistance", "genetic factors", "obesity"]
            },
            "Gestational Diabetes": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["increased thirst", "frequent urination", "fatigue"],
                "additional_symptoms": ["nausea", "blurred vision", "yeast infections", "slow-healing sores"],
                "causes": ["hormonal changes of pregnancy", "insulin resistance", "obesity", "family history"]
            },

            # ===== MEN'S HEALTH =====
            "Erectile Dysfunction": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["difficulty achieving erection", "difficulty maintaining erection"],
                "additional_symptoms": ["reduced libido", "premature ejaculation", "delayed ejaculation"],
                "causes": ["vascular disease", "diabetes", "hypertension", "medications", "psychological factors", "hormonal imbalance"]
            },
            "Benign Prostatic Hyperplasia": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["frequent urination", "weak urine stream", "nocturia"],
                "additional_symptoms": ["urgency", "incomplete emptying", "straining to urinate"],
                "causes": ["aging", "hormonal changes", "family history", "obesity", "sedentary lifestyle"]
            },

            # ===== ENVIRONMENTAL CONDITIONS =====
            "Heat Stroke": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["high body temperature", "confusion", "loss of consciousness"],
                "additional_symptoms": ["rapid heartbeat", "rapid breathing", "seizures", "organ failure"],
                "causes": ["prolonged heat exposure", "dehydration", "strenuous activity", "inadequate acclimation"]
            },
            "Frostbite": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["numbness", "white or grayish skin", "hard or waxy skin"],
                "additional_symptoms": ["blistering", "severe pain", "gangrene", "amputation risk"],
                "causes": ["extreme cold exposure", "wind chill", "inadequate clothing", "poor circulation"]
            },
            "Altitude Sickness": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["headache", "nausea", "fatigue"],
                "additional_symptoms": ["dizziness", "insomnia", "loss of appetite", "shortness of breath"],
                "causes": ["rapid ascent to high altitude", "low oxygen levels", "dehydration", "overexertion"]
            },

            # ===== TOXIC CONDITIONS =====
            "Carbon Monoxide Poisoning": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["headache", "dizziness", "nausea"],
                "additional_symptoms": ["confusion", "weakness", "chest pain", "loss of consciousness"],
                "causes": ["inhalation of carbon monoxide", "faulty heating systems", "car exhaust", "generator fumes"]
            },
            "Lead Poisoning": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fatigue", "abdominal pain", "headache"],
                "additional_symptoms": ["constipation", "anemia", "nervousness", "developmental delays"],
                "causes": ["lead exposure", "old paint", "contaminated water", "industrial exposure", "lead-based products"]
            },
            "Alcohol Poisoning": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["confusion", "vomiting", "seizures"],
                "additional_symptoms": ["slow breathing", "irregular heartbeat", "hypothermia", "unconsciousness"],
                "causes": ["excessive alcohol consumption", "binge drinking", "alcohol intolerance", "mixing substances"]
            },

            # ===== SLEEP DISORDERS =====
            "Insomnia": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["difficulty falling asleep", "difficulty staying asleep", "early morning awakening"],
                "additional_symptoms": ["daytime fatigue", "irritability", "difficulty concentrating", "mood changes"],
                "causes": ["stress", "anxiety", "depression", "caffeine", "irregular schedule", "medical conditions"]
            },
            "Sleep Apnea": {
                "category": "Disorder",
                "severity": ["Medium"],
                "base_symptoms": ["loud snoring", "pauses in breathing", "gasping during sleep"],
                "additional_symptoms": ["daytime sleepiness", "morning headache", "irritability", "cognitive impairment"],
                "causes": ["obesity", "narrow airway", "enlarged tonsils", "alcohol use", "smoking"]
            },
            "Narcolepsy": {
                "category": "Disorder",
                "severity": ["Medium"],
                "base_symptoms": ["excessive daytime sleepiness", "sudden sleep attacks", "cataplexy"],
                "additional_symptoms": ["sleep paralysis", "hallucinations", "fragmented nighttime sleep"],
                "causes": ["genetic factors", "brain chemistry", "autoimmune response", "brain injury"]
            },

            # ===== EYE CONDITIONS =====
            "Cataracts": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["blurred vision", "cloudy vision", "glare sensitivity"],
                "additional_symptoms": ["double vision", "faded colors", "poor night vision", "frequent prescription changes"],
                "causes": ["aging", "UV exposure", "diabetes", "smoking", "steroid use", "eye injury"]
            },
            "Glaucoma": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["gradual vision loss", "tunnel vision", "eye pain"],
                "additional_symptoms": ["headache", "nausea", "halos around lights", "red eyes"],
                "causes": ["increased eye pressure", "aging", "family history", "eye injury", "medical conditions"]
            },
            "Macular Degeneration": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["blurred central vision", "distorted vision", "dark spots"],
                "additional_symptoms": ["difficulty reading", "facial recognition problems", "color perception changes"],
                "causes": ["aging", "genetic factors", "smoking", "obesity", "cardiovascular disease"]
            },

            # ===== EAR CONDITIONS =====
            "Otitis Media": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["ear pain", "fluid drainage", "hearing difficulty"],
                "additional_symptoms": ["fever", "irritability", "balance problems", "tugging at ear"],
                "causes": ["bacterial infection", "viral infection", "eustachian tube dysfunction", "allergies"]
            },
            "Tinnitus": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["ringing in ears", "buzzing sounds", "hissing sounds"],
                "additional_symptoms": ["hearing loss", "sleep disturbance", "concentration problems", "anxiety"],
                "causes": ["age-related hearing loss", "ear wax buildup", "ear infections", "loud noise exposure", "medications"]
            },
            "Meniere's Disease": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["vertigo", "hearing loss", "tinnitus"],
                "additional_symptoms": ["ear fullness", "balance problems", "nausea", "vomiting"],
                "causes": ["endolymphatic hydrops", "genetic factors", "viral infection", "autoimmune response"]
            },

            # ===== DENTAL CONDITIONS =====
            "Periodontal Disease": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["bleeding gums", "swollen gums", "bad breath"],
                "additional_symptoms": ["loose teeth", "receding gums", "pain when chewing", "sensitive teeth"],
                "causes": ["poor oral hygiene", "plaque buildup", "smoking", "diabetes", "medications", "genetic factors"]
            },
            "Dental Caries": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["tooth pain", "sensitivity to hot/cold", "visible holes in teeth"],
                "additional_symptoms": ["bad breath", "swelling", "fever", "difficulty chewing"],
                "causes": ["bacterial infection", "sugar consumption", "poor oral hygiene", "dry mouth", "acidic foods"]
            },

            # ===== NUTRITIONAL DEFICIENCIES =====
            "Iron Deficiency Anemia": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fatigue", "weakness", "pale skin"],
                "additional_symptoms": ["shortness of breath", "dizziness", "cold hands/feet", "brittle nails"],
                "causes": ["inadequate iron intake", "blood loss", "poor absorption", "pregnancy", "heavy menstruation"]
            },
            "Vitamin D Deficiency": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fatigue", "bone pain", "muscle weakness"],
                "additional_symptoms": ["depression", "hair loss", "impaired wound healing", "increased infection risk"],
                "causes": ["inadequate sunlight exposure", "poor dietary intake", "malabsorption", "kidney disease", "obesity"]
            },
            "Vitamin B12 Deficiency": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fatigue", "weakness", "tingling in hands/feet"],
                "additional_symptoms": ["memory problems", "depression", "difficulty walking", "pale skin"],
                "causes": ["inadequate dietary intake", "pernicious anemia", "malabsorption", "vegan diet", "aging"]
            },

            # ===== ALLERGIC CONDITIONS =====
            "Food Allergy": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["hives", "itching", "swelling"],
                "additional_symptoms": ["nausea", "vomiting", "diarrhea", "difficulty breathing", "anaphylaxis"],
                "causes": ["immune response to food proteins", "genetic predisposition", "cross-contamination", "hidden allergens"]
            },
            "Drug Allergy": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["rash", "itching", "hives"],
                "additional_symptoms": ["swelling", "difficulty breathing", "nausea", "fever", "anaphylaxis"],
                "causes": ["immune response to medication", "previous sensitization", "cross-reactivity", "genetic factors"]
            },
            "Latex Allergy": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["skin rash", "itching", "hives"],
                "additional_symptoms": ["swelling", "runny nose", "watery eyes", "difficulty breathing", "anaphylaxis"],
                "causes": ["immune response to latex proteins", "repeated exposure", "cross-reactivity with foods", "genetic predisposition"]
            },

            # ===== OCCUPATIONAL DISEASES =====
            "Asbestosis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["shortness of breath", "chronic cough", "chest pain"],
                "additional_symptoms": ["fatigue", "weight loss", "finger clubbing", "crackling sounds in lungs"],
                "causes": ["asbestos fiber inhalation", "occupational exposure", "construction work", "shipbuilding"]
            },
            "Silicosis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["chronic cough", "shortness of breath", "weakness"],
                "additional_symptoms": ["weight loss", "chest pain", "fever", "night sweats"],
                "causes": ["silica dust inhalation", "mining", "quarrying", "sandblasting", "stone cutting"]
            },
            "Black Lung Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["chronic cough", "shortness of breath", "chest pain"],
                "additional_symptoms": ["fatigue", "weight loss", "cyanosis", "cor pulmonale"],
                "causes": ["coal dust inhalation", "coal mining", "long-term exposure", "inadequate ventilation"]
            },

            # ===== IATROGENIC DISEASES =====
            "Hospital-Acquired Pneumonia": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fever", "cough", "shortness of breath"],
                "additional_symptoms": ["chest pain", "confusion", "low oxygen levels", "sepsis"],
                "causes": ["multidrug-resistant bacteria", "ventilator use", "prolonged hospitalization", "immune suppression"]
            },
            "Catheter-Associated Urinary Tract Infection": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "frequency", "urgency"],
                "additional_symptoms": ["dysuria", "suprapubic pain", "hematuria", "confusion"],
                "causes": ["urinary catheter insertion", "bacterial colonization", "prolonged catheterization", "poor hygiene"]
            },
            "Surgical Site Infection": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["redness", "swelling", "pain"],
                "additional_symptoms": ["drainage", "fever", "warmth", "abscess formation"],
                "causes": ["skin flora contamination", "poor surgical technique", "immune suppression", "diabetes"]
            },

            # ===== PEDIATRIC-SPECIFIC CONDITIONS =====
            "Sudden Infant Death Syndrome": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["unexpected death", "no prior symptoms"],
                "additional_symptoms": ["none apparent", "sleep-related", "autopsy findings"],
                "causes": ["unknown", "brain abnormalities", "respiratory issues", "overheating", "prone sleeping"]
            },
            "Necrotizing Enterocolitis": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["abdominal distension", "feeding intolerance", "bloody stools"],
                "additional_symptoms": ["apnea", "bradycardia", "lethargy", "metabolic acidosis"],
                "causes": ["premature birth", "formula feeding", "intestinal immaturity", "bacterial overgrowth"]
            },
            "Bronchopulmonary Dysplasia": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["rapid breathing", "wheezing", "chronic cough"],
                "additional_symptoms": ["poor weight gain", "frequent infections", "oxygen dependence", "developmental delays"],
                "causes": ["premature birth", "mechanical ventilation", "oxygen toxicity", "lung immaturity"]
            },

            # ===== GERIATRIC CONDITIONS =====
            "Delirium": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["confusion", "disorientation", "fluctuating consciousness"],
                "additional_symptoms": ["hallucinations", "agitation", "sleep disturbances", "poor judgment"],
                "causes": ["infection", "medication changes", "metabolic disturbances", "sensory deprivation", "hospitalization"]
            },
            "Pressure Ulcers": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["red skin", "skin breakdown", "pain"],
                "additional_symptoms": ["swelling", "drainage", "odor", "infection"],
                "causes": ["immobility", "poor nutrition", "moisture", "friction", "shear forces"]
            },
            "Sarcopenia": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["muscle weakness", "reduced muscle mass", "difficulty walking"],
                "additional_symptoms": ["falls", "reduced mobility", "fatigue", "metabolic changes"],
                "causes": ["aging", "sedentary lifestyle", "poor nutrition", "chronic diseases", "hormonal changes"]
            },

            # ===== RARE GENETIC DISORDERS =====
            "Tay-Sachs Disease": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["developmental delay", "seizures", "loss of motor skills"],
                "additional_symptoms": ["cherry-red spot in eye", "hearing loss", "blindness", "paralysis"],
                "causes": ["genetic mutation", "hexosaminidase A deficiency", "autosomal recessive inheritance"]
            },
            "Gaucher's Disease": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fatigue", "bone pain", "easy bruising"],
                "additional_symptoms": ["enlarged spleen/liver", "anemia", "lung problems", "neurological symptoms"],
                "causes": ["genetic mutation", "glucocerebrosidase deficiency", "autosomal recessive inheritance"]
            },
            "Fabry Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["pain in extremities", "fatigue", "fever"],
                "additional_symptoms": ["skin lesions", "heart problems", "kidney failure", "stroke"],
                "causes": ["genetic mutation", "alpha-galactosidase A deficiency", "X-linked inheritance"]
            },

            # ===== AUTOIMMUNE DISORDERS (ADDITIONAL) =====
            "Scleroderma": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["skin thickening", "Raynaud's phenomenon", "joint pain"],
                "additional_symptoms": ["difficulty swallowing", "shortness of breath", "heart problems", "kidney problems"],
                "causes": ["autoimmune response", "genetic factors", "environmental triggers", "vascular abnormalities"]
            },
            "Vasculitis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fever", "fatigue", "weight loss"],
                "additional_symptoms": ["rash", "joint pain", "nerve problems", "organ damage"],
                "causes": ["autoimmune response", "infection", "medication", "malignancy", "genetic factors"]
            },
            "Sjögren's Syndrome": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["dry eyes", "dry mouth", "fatigue"],
                "additional_symptoms": ["joint pain", "skin rash", "vaginal dryness", "cognitive difficulties"],
                "causes": ["autoimmune response", "genetic factors", "hormonal factors", "viral infection"]
            },

            # ===== METABOLIC DISORDERS (ADDITIONAL) =====
            "Wilson's Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fatigue", "abdominal pain", "jaundice"],
                "additional_symptoms": ["tremor", "speech difficulties", "psychiatric symptoms", "kidney stones"],
                "causes": ["genetic mutation", "copper accumulation", "ATP7B gene defect", "autosomal recessive inheritance"]
            },
            "Hemochromatosis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fatigue", "joint pain", "abdominal pain"],
                "additional_symptoms": ["skin darkening", "diabetes", "heart problems", "liver disease"],
                "causes": ["genetic mutation", "iron overload", "HFE gene defect", "autosomal recessive inheritance"]
            },

            # ===== CONNECTIVE TISSUE DISORDERS =====
            "Marfan Syndrome": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["tall stature", "long limbs", "flexible joints"],
                "additional_symptoms": ["aortic aneurysm", "lens dislocation", "scoliosis", "pectus excavatum"],
                "causes": ["genetic mutation", "fibrillin-1 deficiency", "autosomal dominant inheritance"]
            },
            "Ehlers-Danlos Syndrome": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["joint hypermobility", "skin hyperelasticity", "easy bruising"],
                "additional_symptoms": ["chronic pain", "fatigue", "organ prolapse", "vascular complications"],
                "causes": ["genetic mutations", "collagen defects", "various inheritance patterns"]
            },

            # ===== HEMATOLOGICAL DISORDERS (ADDITIONAL) =====
            "Thalassemia": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fatigue", "pale skin", "shortness of breath"],
                "additional_symptoms": ["jaundice", "bone deformities", "growth retardation", "organ damage"],
                "causes": ["genetic mutations", "hemoglobin synthesis defects", "autosomal recessive inheritance"]
            },
            "Sickle Cell Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["pain episodes", "fatigue", "jaundice"],
                "additional_symptoms": ["swelling", "frequent infections", "delayed growth", "vision problems"],
                "causes": ["genetic mutation", "hemoglobin S", "autosomal recessive inheritance"]
            },

            # ===== ENDOCRINE DISORDERS (ADDITIONAL) =====
            "Pheochromocytoma": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["hypertension", "headache", "sweating"],
                "additional_symptoms": ["palpitations", "tremor", "anxiety", "weight loss"],
                "causes": ["adrenal gland tumor", "genetic mutations", "familial syndromes", "sporadic occurrence"]
            },
            "Cushing's Disease": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["weight gain", "moon face", "buffalo hump"],
                "additional_symptoms": ["thin skin", "easy bruising", "muscle weakness", "osteoporosis"],
                "causes": ["pituitary adenoma", "ACTH overproduction", "corticotroph hyperplasia"]
            },

            # ===== NEURODEGENERATIVE DISORDERS (ADDITIONAL) =====
            "Huntington's Disease": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["uncontrolled movements", "cognitive decline", "emotional disturbances"],
                "additional_symptoms": ["difficulty swallowing", "weight loss", "depression", "irritability"],
                "causes": ["genetic mutation", "HTT gene expansion", "autosomal dominant inheritance"]
            },
            "Spinocerebellar Ataxia": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["balance problems", "coordination difficulties", "speech problems"],
                "additional_symptoms": ["tremor", "muscle weakness", "vision problems", "cognitive decline"],
                "causes": ["genetic mutations", "various gene expansions", "autosomal dominant inheritance"]
            },

            # ===== CARDIAC DISORDERS (ADDITIONAL) =====
            "Cardiomyopathy": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["shortness of breath", "fatigue", "swelling"],
                "additional_symptoms": ["chest pain", "palpitations", "dizziness", "syncope"],
                "causes": ["genetic mutations", "hypertension", "coronary artery disease", "infection", "toxins"]
            },
            "Arrhythmogenic Right Ventricular Cardiomyopathy": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["palpitations", "syncope", "sudden cardiac death"],
                "additional_symptoms": ["fatigue", "shortness of breath", "edema", "ventricular arrhythmias"],
                "causes": ["genetic mutations", "desmosome protein defects", "autosomal dominant inheritance"]
            },

            # ===== PULMONARY DISORDERS (ADDITIONAL) =====
            "Idiopathic Pulmonary Fibrosis": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["shortness of breath", "dry cough", "fatigue"],
                "additional_symptoms": ["weight loss", "finger clubbing", "crackles on lung exam"],
                "causes": ["unknown", "genetic factors", "environmental exposures", "autoimmune factors"]
            },
            "Pulmonary Arterial Hypertension": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["shortness of breath", "fatigue", "chest pain"],
                "additional_symptoms": ["dizziness", "edema", "palpitations", "syncope"],
                "causes": ["unknown primary", "connective tissue diseases", "congenital heart disease", "liver disease"]
            },

            # ===== GASTROINTESTINAL DISORDERS (ADDITIONAL) =====
            "Celiac Disease": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["diarrhea", "abdominal pain", "bloating"],
                "additional_symptoms": ["weight loss", "fatigue", "anemia", "bone problems", "dermatitis herpetiformis"],
                "causes": ["immune response to gluten", "genetic factors", "environmental triggers", "intestinal permeability"]
            },
            "Eosinophilic Esophagitis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["difficulty swallowing", "chest pain", "food impaction"],
                "additional_symptoms": ["nausea", "vomiting", "abdominal pain", "failure to thrive"],
                "causes": ["eosinophil accumulation", "allergic inflammation", "genetic factors", "environmental allergens"]
            },

            # ===== UROLOGICAL DISORDERS (ADDITIONAL) =====
            "Interstitial Cystitis": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["bladder pain", "frequent urination", "urgency"],
                "additional_symptoms": ["pelvic pain", "pain during intercourse", "fatigue", "depression"],
                "causes": ["bladder wall inflammation", "unknown etiology", "autoimmune factors", "neurological factors"]
            },
            "Autosomal Dominant Polycystic Kidney Disease": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["flank pain", "hematuria", "hypertension"],
                "additional_symptoms": ["kidney enlargement", "liver cysts", "brain aneurysms", "cardiac valve problems"],
                "causes": ["genetic mutations", "PKD1 or PKD2 gene defects", "autosomal dominant inheritance"]
            },

            # ===== DERMATOLOGICAL DISORDERS (ADDITIONAL) =====
            "Vitiligo": {
                "category": "Disease",
                "severity": ["Low"],
                "base_symptoms": ["white patches on skin", "premature graying of hair"],
                "additional_symptoms": ["loss of skin color", "increased sun sensitivity", "psychological distress"],
                "causes": ["autoimmune response", "genetic factors", "oxidative stress", "neural factors"]
            },
            "Pemphigus Vulgaris": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["blisters", "erosions", "painful sores"],
                "additional_symptoms": ["skin fragility", "mucosal involvement", "infection risk", "fluid loss"],
                "causes": ["autoimmune response", "antibodies against desmoglein", "genetic predisposition"]
            },

            # ===== OPHTHALMOLOGICAL DISORDERS =====
            "Retinitis Pigmentosa": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["night blindness", "tunnel vision", "photophobia"],
                "additional_symptoms": ["bone spicules", "optic disc pallor", "arteriolar narrowing", "cataracts"],
                "causes": ["genetic mutations", "retinal pigment epithelium degeneration", "various inheritance patterns"]
            },
            "Keratoconus": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["blurred vision", "distorted vision", "light sensitivity"],
                "additional_symptoms": ["frequent prescription changes", "eye rubbing", "corneal scarring"],
                "causes": ["genetic factors", "eye rubbing", "atopy", "connective tissue disorders"]
            },

            # ===== OTOLARYNGOLOGICAL DISORDERS =====
            "Ménière's Disease": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["vertigo", "tinnitus", "hearing loss"],
                "additional_symptoms": ["ear fullness", "balance problems", "nausea", "vomiting"],
                "causes": ["endolymphatic hydrops", "genetic factors", "viral infection", "autoimmune response"]
            },
            "Acoustic Neuroma": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["hearing loss", "tinnitus", "balance problems"],
                "additional_symptoms": ["facial numbness", "headache", "difficulty swallowing", "hoarseness"],
                "causes": ["vestibular schwannoma", "NF2 gene mutation", "radiation exposure", "unknown causes"]
            },

            # ===== RHEUMATOLOGICAL DISORDERS (ADDITIONAL) =====
            "Ankylosing Spondylitis": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["back pain", "stiffness", "reduced spinal mobility"],
                "additional_symptoms": ["fatigue", "enthesitis", "uveitis", "inflammatory bowel disease"],
                "causes": ["genetic factors", "HLA-B27 association", "autoimmune response", "environmental triggers"]
            },
            "Polymyalgia Rheumatica": {
                "category": "Disease",
                "severity": ["Medium"],
                "base_symptoms": ["shoulder pain", "hip pain", "stiffness"],
                "additional_symptoms": ["fatigue", "weight loss", "fever", "temporal arteritis"],
                "causes": ["unknown", "autoimmune response", "genetic factors", "environmental triggers"]
            },

            # ===== HEMATOLOGICAL MALIGNANCIES (ADDITIONAL) =====
            "Hodgkin's Lymphoma": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["enlarged lymph nodes", "fever", "night sweats"],
                "additional_symptoms": ["weight loss", "fatigue", "itching", "alcohol-induced pain"],
                "causes": ["Reed-Sternberg cells", "EBV association", "genetic factors", "immune suppression"]
            },
            "Non-Hodgkin's Lymphoma": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["enlarged lymph nodes", "fatigue", "weight loss"],
                "additional_symptoms": ["fever", "night sweats", "itching", "abdominal pain"],
                "causes": ["B-cell or T-cell malignancy", "genetic factors", "immune suppression", "viral infections"]
            },

            # ===== SOLID TUMORS (ADDITIONAL) =====
            "Glioblastoma": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["headache", "seizures", "cognitive changes"],
                "additional_symptoms": ["nausea", "vomiting", "vision changes", "motor deficits"],
                "causes": ["glial cell malignancy", "genetic mutations", "radiation exposure", "unknown factors"]
            },
            "Renal Cell Carcinoma": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["blood in urine", "flank pain", "weight loss"],
                "additional_symptoms": ["fatigue", "fever", "hypertension", "varicocele"],
                "causes": ["renal tubular cell malignancy", "smoking", "obesity", "genetic syndromes"]
            },

            # ===== INFECTIOUS DISEASES (FINAL ADDITIONS) =====
            "Bacterial Endocarditis": {
                "category": "Bacteria",
                "severity": ["High"],
                "base_symptoms": ["fever", "fatigue", "weight loss"],
                "additional_symptoms": ["heart murmur", "petechiae", "splinter hemorrhages", "embolic events"],
                "causes": ["Streptococcus viridans", "Staphylococcus aureus", "heart valve abnormalities", "intravenous drug use"]
            },
            "Fungal Endocarditis": {
                "category": "Fungus",
                "severity": ["High"],
                "base_symptoms": ["fever", "weight loss", "embolic events"],
                "additional_symptoms": ["heart murmur", "petechiae", "mycotic aneurysms", "immune suppression"],
                "causes": ["Candida species", "Aspergillus species", "immune deficiency", "prosthetic valves"]
            },
            "Viral Hepatitis": {
                "category": "Virus",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fatigue", "jaundice", "abdominal pain"],
                "additional_symptoms": ["nausea", "dark urine", "clay-colored stools", "joint pain"],
                "causes": ["Hepatitis viruses", "blood contact", "sexual transmission", "contaminated food/water"]
            },
            "Amebiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["diarrhea", "abdominal pain", "fever"],
                "additional_symptoms": ["bloody stools", "weight loss", "liver abscess", "peritonitis"],
                "causes": ["Entamoeba histolytica", "contaminated water/food", "poor sanitation", "fecal-oral transmission"]
            },
            "Trichomoniasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["vaginal discharge", "itching", "pain during urination"],
                "additional_symptoms": ["pain during intercourse", "abdominal pain", "frequent urination"],
                "causes": ["Trichomonas vaginalis", "sexual transmission", "asymptomatic carriers"]
            },
            "Babesiosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fever", "fatigue", "chills"],
                "additional_symptoms": ["sweating", "headache", "muscle pain", "hemolytic anemia"],
                "causes": ["Babesia parasites", "tick bites", "blood transfusion", "congenital transmission"]
            },
            "Strongyloidiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["abdominal pain", "diarrhea", "rash"],
                "additional_symptoms": ["cough", "weight loss", "eosinophilia", "hyperinfection syndrome"],
                "causes": ["Strongyloides stercoralis", "skin penetration", "contaminated soil", "autoinfection"]
            },
            "Hookworm Infection": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "diarrhea", "fatigue"],
                "additional_symptoms": ["anemia", "protein deficiency", "edema", "growth retardation"],
                "causes": ["Ancylostoma duodenale", "Necator americanus", "skin penetration", "contaminated soil"]
            },
            "Ascariasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "nausea", "vomiting"],
                "additional_symptoms": ["cough", "wheezing", "intestinal obstruction", "malnutrition"],
                "causes": ["Ascaris lumbricoides", "fecal-oral transmission", "contaminated food/water", "poor hygiene"]
            },
            "Taeniasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "nausea", "weight loss"],
                "additional_symptoms": ["headache", "vision changes", "seizures", "cysticercosis"],
                "causes": ["Taenia species", "undercooked pork/beef", "contaminated water", "poor sanitation"]
            },
            "Echinococcosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["abdominal pain", "nausea", "vomiting"],
                "additional_symptoms": ["liver enlargement", "cyst rupture", "allergic reactions", "organ dysfunction"],
                "causes": ["Echinococcus species", "contact with infected dogs", "contaminated food", "zoonotic transmission"]
            },
            "Onchocerciasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["itching", "skin rash", "nodules"],
                "additional_symptoms": ["vision loss", "blindness", "lymphadenopathy", "skin depigmentation"],
                "causes": ["Onchocerca volvulus", "blackfly bites", "river blindness", "endemic areas"]
            },
            "Dracunculiasis": {
                "category": "Parasite",
                "severity": ["Medium"],
                "base_symptoms": ["painful blister", "fever", "nausea"],
                "additional_symptoms": ["swelling", "ulcer formation", "secondary infection", "disability"],
                "causes": ["Dracunculus medinensis", "contaminated water", "copepod intermediate hosts"]
            },
            "Schistosomiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fever", "rash", "cough"],
                "additional_symptoms": ["abdominal pain", "blood in stool/urine", "liver enlargement", "bladder cancer"],
                "causes": ["Schistosoma species", "contact with contaminated water", "snail intermediate hosts"]
            },
            "Fascioliasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "abdominal pain", "fatigue"],
                "additional_symptoms": ["nausea", "vomiting", "liver enlargement", "eosinophilia"],
                "causes": ["Fasciola hepatica", "contaminated watercress", "raw vegetables", "zoonotic transmission"]
            },
            "Opisthorchiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "fatigue", "fever"],
                "additional_symptoms": ["nausea", "diarrhea", "liver enlargement", "cholangiocarcinoma"],
                "causes": ["Opisthorchis viverrini", "undercooked fish", "contaminated water", "poor sanitation"]
            },
            "Clonorchiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "fatigue", "fever"],
                "additional_symptoms": ["nausea", "diarrhea", "liver enlargement", "cholangiocarcinoma"],
                "causes": ["Clonorchis sinensis", "undercooked fish", "contaminated water", "poor sanitation"]
            },
            "Paragonimiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["cough", "chest pain", "fever"],
                "additional_symptoms": ["hemoptysis", "dyspnea", "abdominal pain", "eosinophilia"],
                "causes": ["Paragonimus species", "undercooked crustaceans", "contaminated water", "zoonotic transmission"]
            },
            "Angiostrongyliasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["headache", "fever", "dizziness"],
                "additional_symptoms": ["confusion", "seizures", "encephalitis", "respiratory problems"],
                "causes": ["Angiostrongylus cantonensis", "raw snails/slugs", "contaminated vegetables", "intermediate hosts"]
            },
            "Gnathostomiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "rash", "eosinophilia"],
                "additional_symptoms": ["migratory swelling", "abdominal pain", "neurological symptoms"],
                "causes": ["Gnathostoma species", "undercooked fish/frogs", "contaminated water", "zoonotic transmission"]
            },
            "Sparganosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["painful swelling", "fever", "eosinophilia"],
                "additional_symptoms": ["migratory lesions", "neurological symptoms", "ocular involvement"],
                "causes": ["Spirometra species", "contaminated water", "raw frog/snake meat", "copepod intermediate hosts"]
            },
            "Diphyllobothriasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "diarrhea", "fatigue"],
                "additional_symptoms": ["vitamin B12 deficiency", "anemia", "neurological symptoms"],
                "causes": ["Diphyllobothrium latum", "undercooked fish", "contaminated water", "poor sanitation"]
            },
            "Hymenolepiasis": {
                "category": "Parasite",
                "severity": ["Low"],
                "base_symptoms": ["abdominal pain", "diarrhea", "anorexia"],
                "additional_symptoms": ["nausea", "headache", "dizziness", "allergic reactions"],
                "causes": ["Hymenolepis nana", "fecal-oral transmission", "contaminated food/water", "poor hygiene"]
            },
            "Enterobiasis": {
                "category": "Parasite",
                "severity": ["Low"],
                "base_symptoms": ["perianal itching", "restless sleep", "irritability"],
                "additional_symptoms": ["abdominal pain", "nausea", "vulvovaginitis", "urinary tract infection"],
                "causes": ["Enterobius vermicularis", "fecal-oral transmission", "hand-to-mouth", "autoinfection"]
            },
            "Trichuriasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "diarrhea", "bloody stools"],
                "additional_symptoms": ["anemia", "growth retardation", "rectal prolapse", "nutritional deficiency"],
                "causes": ["Trichuris trichiura", "fecal-oral transmission", "contaminated soil", "poor sanitation"]
            },
            "Ancylostomiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "diarrhea", "fatigue"],
                "additional_symptoms": ["anemia", "protein deficiency", "edema", "pica"],
                "causes": ["Ancylostoma duodenale", "skin penetration", "contaminated soil", "barefoot walking"]
            },
            "Necatoriasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abdominal pain", "diarrhea", "fatigue"],
                "additional_symptoms": ["anemia", "protein deficiency", "edema", "pica"],
                "causes": ["Necator americanus", "skin penetration", "contaminated soil", "barefoot walking"]
            },
            "Trichinellosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fever", "muscle pain", "edema"],
                "additional_symptoms": ["diarrhea", "nausea", "eosinophilia", "myocarditis"],
                "causes": ["Trichinella species", "undercooked pork", "wild game meat", "zoonotic transmission"]
            },
            "Cysticercosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["seizures", "headache", "focal neurological deficits"],
                "additional_symptoms": ["hydrocephalus", "increased intracranial pressure", "cognitive impairment"],
                "causes": ["Taenia solium", "fecal-oral transmission", "undercooked pork", "autoinfection"]
            },
            "Echinococcosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["abdominal pain", "nausea", "vomiting"],
                "additional_symptoms": ["liver enlargement", "cyst rupture", "allergic reactions", "organ dysfunction"],
                "causes": ["Echinococcus species", "contact with infected dogs", "contaminated food", "zoonotic transmission"]
            },
            "Toxocariasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "cough", "rash"],
                "additional_symptoms": ["abdominal pain", "hepatomegaly", "pulmonary infiltrates", "eosinophilia"],
                "causes": ["Toxocara species", "ingestion of eggs", "contaminated soil", "pica"]
            },
            "Baylisascariasis": {
                "category": "Parasite",
                "severity": ["High"],
                "base_symptoms": ["fever", "headache", "seizures"],
                "additional_symptoms": ["coma", "neurological deficits", "vision loss", "death"],
                "causes": ["Baylisascaris procyonis", "ingestion of eggs", "contaminated soil", "raccoon feces"]
            },
            "Dirofilariasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["cough", "chest pain", "fever"],
                "additional_symptoms": ["hemoptysis", "pleural effusion", "pulmonary nodules", "eosinophilia"],
                "causes": ["Dirofilaria species", "mosquito transmission", "canine reservoir", "zoonotic infection"]
            },
            "Loiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["subcutaneous swellings", "itching", "fever"],
                "additional_symptoms": ["joint pain", "fatigue", "eosinophilia", "ocular involvement"],
                "causes": ["Loa loa", "tabanid fly bites", "day-biting flies", "endemic areas"]
            },
            "Mansonellosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["fever", "headache", "rash"],
                "additional_symptoms": ["joint pain", "edema", "eosinophilia", "chronic symptoms"],
                "causes": ["Mansonella species", "biting midges", "blackfly bites", "endemic areas"]
            },
            "Thelaziasis": {
                "category": "Parasite",
                "severity": ["Low"],
                "base_symptoms": ["eye irritation", "lacrimation", "foreign body sensation"],
                "additional_symptoms": ["conjunctivitis", "corneal ulcers", "vision impairment"],
                "causes": ["Thelazia species", "face fly transmission", "ocular infection", "animal reservoir"]
            },
            "Myiasis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["pain", "itching", "swelling"],
                "additional_symptoms": ["discharge", "secondary infection", "tissue destruction", "migration tracks"],
                "causes": ["fly larvae", "skin penetration", "wound contamination", "poor hygiene"]
            },
            "Scabies": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["intense itching", "rash", "burrows"],
                "additional_symptoms": ["excoriations", "secondary infection", "regional lymphadenopathy"],
                "causes": ["Sarcoptes scabiei", "skin-to-skin contact", "fomite transmission", "crowded conditions"]
            },
            "Pediculosis": {
                "category": "Parasite",
                "severity": ["Low"],
                "base_symptoms": ["itching", "lice visible", "nits on hair"],
                "additional_symptoms": ["excoriations", "secondary infection", "regional lymphadenopathy"],
                "causes": ["Pediculus humanus", "head-to-head contact", "shared combs/brushes", "crowded conditions"]
            },
            "Demodicosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["facial redness", "itching", "rosacea-like symptoms"],
                "additional_symptoms": ["blepharitis", "ocular irritation", "cylindrical dandruff"],
                "causes": ["Demodex mites", "facial skin colonization", "immune suppression", "ocular involvement"]
            },
            "Cheyletiellosis": {
                "category": "Parasite",
                "severity": ["Low"],
                "base_symptoms": ["pruritic dermatitis", "scaling", "erythema"],
                "additional_symptoms": ["papules", "excoriations", "secondary infection"],
                "causes": ["Cheyletiella mites", "contact with infested animals", "walking dandruff", "zoonotic transmission"]
            },
            "Trombiculosis": {
                "category": "Parasite",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["intense itching", "papular rash", "red lesions"],
                "additional_symptoms": ["vesicles", "secondary infection", "regional lymphadenopathy"],
                "causes": ["Trombicula mites", "chigger bites", "outdoor activities", "seasonal occurrence"]
            },
            "Sarcoidosis": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fatigue", "weight loss", "fever"],
                "additional_symptoms": ["enlarged lymph nodes", "skin lesions", "joint pain", "pulmonary involvement"],
                "causes": ["unknown", "immune system dysfunction", "genetic factors", "environmental triggers"]
            },
            "Amyloidosis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fatigue", "weight loss", "edema"],
                "additional_symptoms": ["shortness of breath", "neuropathy", "organ dysfunction", "purpura"],
                "causes": ["abnormal protein folding", "chronic inflammation", "genetic mutations", "plasma cell disorders"]
            },
            "Porphyria": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["abdominal pain", "neurological symptoms", "skin photosensitivity"],
                "additional_symptoms": ["vomiting", "constipation", "psychiatric symptoms", "anemia"],
                "causes": ["enzyme deficiencies", "heme synthesis defects", "genetic mutations", "environmental triggers"]
            },
            "Mucopolysaccharidosis": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["developmental delay", "coarse facial features", "joint stiffness"],
                "additional_symptoms": ["hearing loss", "vision problems", "cardiac involvement", "skeletal abnormalities"],
                "causes": ["lysosomal enzyme deficiencies", "genetic mutations", "autosomal recessive inheritance"]
            },
            "Lysosomal Storage Diseases": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["developmental delay", "organomegaly", "neurological deterioration"],
                "additional_symptoms": ["skeletal abnormalities", "vision/hearing loss", "cardiac involvement"],
                "causes": ["lysosomal enzyme deficiencies", "genetic mutations", "autosomal recessive inheritance"]
            },
            "Peroxisomal Disorders": {
                "category": "Disease",
                "severity": ["High"],
                "base_symptoms": ["developmental delay", "seizures", "hearing loss"],
                "additional_symptoms": ["vision problems", "liver dysfunction", "adrenal insufficiency"],
                "causes": ["peroxisomal enzyme deficiencies", "genetic mutations", "autosomal recessive inheritance"]
            },
            "Mitochondrial Diseases": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["fatigue", "muscle weakness", "neurological symptoms"],
                "additional_symptoms": ["vision/hearing loss", "cardiac involvement", "gastrointestinal problems"],
                "causes": ["mitochondrial DNA mutations", "nuclear DNA mutations", "energy metabolism defects"]
            },
            "Channelopathies": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["muscle weakness", "paralysis", "cardiac arrhythmias"],
                "additional_symptoms": ["seizures", "periodic paralysis", "myotonia", "neurological symptoms"],
                "causes": ["ion channel mutations", "genetic defects", "various inheritance patterns"]
            },
            "Ciliopathies": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["developmental delay", "organ dysfunction", "skeletal abnormalities"],
                "additional_symptoms": ["vision/hearing loss", "kidney problems", "cardiac defects"],
                "causes": ["ciliary dysfunction", "genetic mutations", "various inheritance patterns"]
            },
            "Primary Immunodeficiencies": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["recurrent infections", "failure to thrive", "autoimmune disorders"],
                "additional_symptoms": ["chronic diarrhea", "skin rashes", "organ dysfunction"],
                "causes": ["genetic mutations", "immune system defects", "various inheritance patterns"]
            },
            "Inborn Errors of Metabolism": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["developmental delay", "seizures", "organ dysfunction"],
                "additional_symptoms": ["metabolic crises", "neurological deterioration", "failure to thrive"],
                "causes": ["enzyme deficiencies", "genetic mutations", "metabolic pathway defects"]
            },
            "Chromosomal Disorders": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["developmental delay", "congenital abnormalities", "intellectual disability"],
                "additional_symptoms": ["growth retardation", "organ malformations", "various phenotypic features"],
                "causes": ["chromosomal abnormalities", "genetic mutations", "parental age factors"]
            },
            "Single Gene Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["variable symptoms", "organ-specific manifestations", "developmental abnormalities"],
                "additional_symptoms": ["neurological symptoms", "metabolic disturbances", "structural defects"],
                "causes": ["single gene mutations", "autosomal dominant/recessive", "X-linked inheritance"]
            },
            "Multifactorial Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["variable presentation", "environmental influences", "genetic predisposition"],
                "additional_symptoms": ["complex phenotypes", "variable severity", "environmental triggers"],
                "causes": ["gene-environment interactions", "multiple genetic factors", "environmental exposures"]
            },
            "Teratogenic Disorders": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["congenital abnormalities", "developmental defects", "organ malformations"],
                "additional_symptoms": ["growth retardation", "intellectual disability", "functional impairments"],
                "causes": ["prenatal exposures", "teratogenic agents", "maternal factors", "environmental toxins"]
            },
            "Degenerative Disorders": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["progressive deterioration", "functional decline", "organ dysfunction"],
                "additional_symptoms": ["neurological symptoms", "musculoskeletal problems", "cognitive impairment"],
                "causes": ["aging processes", "genetic factors", "environmental exposures", "lifestyle factors"]
            },
            "Inflammatory Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["inflammation", "pain", "swelling"],
                "additional_symptoms": ["redness", "heat", "loss of function", "systemic symptoms"],
                "causes": ["immune responses", "infections", "autoimmune reactions", "environmental triggers"]
            },
            "Vascular Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["circulatory problems", "pain", "swelling"],
                "additional_symptoms": ["ischemia", "organ dysfunction", "thrombosis", "hemorrhage"],
                "causes": ["vascular abnormalities", "atherosclerosis", "hypertension", "genetic factors"]
            },
            "Hematopoietic Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["anemia", "bleeding disorders", "thrombosis"],
                "additional_symptoms": ["fatigue", "infection susceptibility", "organomegaly", "cytopenias"],
                "causes": ["bone marrow dysfunction", "genetic mutations", "acquired disorders", "nutritional deficiencies"]
            },
            "Endocrine Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["hormonal imbalances", "metabolic disturbances", "growth abnormalities"],
                "additional_symptoms": ["reproductive problems", "electrolyte imbalances", "organ dysfunction"],
                "causes": ["glandular dysfunction", "genetic mutations", "autoimmune disorders", "tumors"]
            },
            "Neurological Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["neurological symptoms", "cognitive impairment", "motor dysfunction"],
                "additional_symptoms": ["sensory disturbances", "coordination problems", "behavioral changes"],
                "causes": ["brain/spinal cord abnormalities", "genetic factors", "infections", "trauma"]
            },
            "Musculoskeletal Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["pain", "stiffness", "reduced mobility"],
                "additional_symptoms": ["deformity", "weakness", "inflammation", "functional impairment"],
                "causes": ["joint/cartilage problems", "muscle disorders", "bone diseases", "genetic factors"]
            },
            "Dermatological Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["skin abnormalities", "rashes", "itching"],
                "additional_symptoms": ["pigmentation changes", "texture abnormalities", "hair/nail problems"],
                "causes": ["immune disorders", "genetic factors", "infections", "environmental exposures"]
            },
            "Ophthalmological Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["vision problems", "eye pain", "visual disturbances"],
                "additional_symptoms": ["eye redness", "discharge", "light sensitivity", "field defects"],
                "causes": ["refractive errors", "degenerative diseases", "infections", "trauma"]
            },
            "Otolaryngological Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["hearing problems", "ear pain", "balance issues"],
                "additional_symptoms": ["tinnitus", "vertigo", "speech problems", "nasal symptoms"],
                "causes": ["infections", "trauma", "congenital abnormalities", "aging processes"]
            },
            "Respiratory Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["breathing difficulties", "cough", "chest pain"],
                "additional_symptoms": ["wheezing", "shortness of breath", "sputum production", "hypoxia"],
                "causes": ["infections", "allergies", "obstruction", "genetic factors", "environmental exposures"]
            },
            "Cardiovascular Disorders": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["chest pain", "shortness of breath", "palpitations"],
                "additional_symptoms": ["edema", "fatigue", "dizziness", "syncope"],
                "causes": ["atherosclerosis", "hypertension", "valvular disease", "arrhythmias", "congenital defects"]
            },
            "Gastrointestinal Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["abdominal pain", "nausea", "vomiting"],
                "additional_symptoms": ["diarrhea", "constipation", "bloating", "weight changes"],
                "causes": ["infections", "inflammation", "motility disorders", "malabsorption", "tumors"]
            },
            "Hepatobiliary Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["jaundice", "abdominal pain", "fatigue"],
                "additional_symptoms": ["nausea", "itching", "dark urine", "pale stools"],
                "causes": ["viral infections", "alcohol abuse", "autoimmune disorders", "metabolic disorders"]
            },
            "Pancreatic Disorders": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["abdominal pain", "weight loss", "diarrhea"],
                "additional_symptoms": ["nausea", "vomiting", "steatorrhea", "diabetes"],
                "causes": ["chronic pancreatitis", "cystic fibrosis", "alcohol abuse", "autoimmune disorders"]
            },
            "Renal Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["edema", "fatigue", "hypertension"],
                "additional_symptoms": ["proteinuria", "hematuria", "electrolyte imbalances", "uremia"],
                "causes": ["diabetes", "hypertension", "glomerulonephritis", "polycystic disease", "infections"]
            },
            "Urological Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["urinary frequency", "dysuria", "hematuria"],
                "additional_symptoms": ["incontinence", "retention", "pain", "obstruction"],
                "causes": ["infections", "stones", "obstruction", "neurological disorders", "prostate problems"]
            },
            "Gynecological Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["pelvic pain", "abnormal bleeding", "discharge"],
                "additional_symptoms": ["dysmenorrhea", "dyspareunia", "infertility", "hormonal symptoms"],
                "causes": ["infections", "hormonal imbalances", "structural abnormalities", "neoplasms"]
            },
            "Obstetrical Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["pregnancy complications", "fetal abnormalities", "maternal symptoms"],
                "additional_symptoms": ["hypertension", "diabetes", "preterm labor", "placental problems"],
                "causes": ["maternal factors", "fetal factors", "placental abnormalities", "environmental factors"]
            },
            "Neonatal Disorders": {
                "category": "Disease",
                "severity": ["Medium", "High"],
                "base_symptoms": ["respiratory distress", "feeding difficulties", "jaundice"],
                "additional_symptoms": ["hypothermia", "hypoglycemia", "sepsis", "congenital abnormalities"],
                "causes": ["prematurity", "birth trauma", "infections", "congenital defects", "maternal factors"]
            },
            "Pediatric Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["growth retardation", "developmental delays", "recurrent infections"],
                "additional_symptoms": ["behavioral problems", "learning difficulties", "organ dysfunction"],
                "causes": ["genetic factors", "congenital abnormalities", "infections", "nutritional deficiencies"]
            },
            "Adolescent Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["pubertal abnormalities", "behavioral changes", "mood disturbances"],
                "additional_symptoms": ["eating disorders", "substance abuse", "risk-taking behaviors"],
                "causes": ["hormonal changes", "psychological factors", "peer pressure", "family dynamics"]
            },
            "Geriatric Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["frailty", "cognitive decline", "multiple comorbidities"],
                "additional_symptoms": ["falls", "incontinence", "polypharmacy effects", "social isolation"],
                "causes": ["aging processes", "cumulative damage", "multiple chronic conditions", "lifestyle factors"]
            },
            "Tropical Diseases": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["fever", "rash", "organ involvement"],
                "additional_symptoms": ["vector-borne symptoms", "regional manifestations", "chronic complications"],
                "causes": ["vector transmission", "environmental factors", "poor sanitation", "endemic conditions"]
            },
            "Occupational Diseases": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["respiratory symptoms", "skin problems", "neurological symptoms"],
                "additional_symptoms": ["hearing loss", "musculoskeletal pain", "chemical toxicity"],
                "causes": ["workplace exposures", "chemical agents", "physical hazards", "ergonomic factors"]
            },
            "Iatrogenic Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["treatment complications", "adverse reactions", "nosocomial infections"],
                "additional_symptoms": ["drug interactions", "surgical complications", "device-related problems"],
                "causes": ["medical interventions", "drug side effects", "procedural complications", "hospital-acquired conditions"]
            },
            "Environmental Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["allergic reactions", "toxic exposures", "climate-related symptoms"],
                "additional_symptoms": ["respiratory problems", "skin conditions", "neurological effects"],
                "causes": ["pollution", "chemical exposures", "radiation", "extreme weather", "natural disasters"]
            },
            "Nutritional Disorders": {
                "category": "Disease",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["weight changes", "fatigue", "organ dysfunction"],
                "additional_symptoms": ["deficiency symptoms", "toxicity signs", "metabolic disturbances"],
                "causes": ["inadequate intake", "malabsorption", "excess consumption", "metabolic disorders"]
            },
            "Sleep Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["insomnia", "excessive sleepiness", "abnormal sleep patterns"],
                "additional_symptoms": ["fatigue", "cognitive impairment", "mood disturbances", "behavioral problems"],
                "causes": ["circadian rhythm disorders", "medical conditions", "medications", "lifestyle factors"]
            },
            "Eating Disorders": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["abnormal eating patterns", "body image distortion", "weight abnormalities"],
                "additional_symptoms": ["electrolyte imbalances", "cardiac problems", "gastrointestinal issues"],
                "causes": ["psychological factors", "societal pressures", "genetic predisposition", "neurochemical imbalances"]
            },
            "Substance Use Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["craving", "loss of control", "tolerance"],
                "additional_symptoms": ["withdrawal symptoms", "organ damage", "behavioral changes", "social problems"],
                "causes": ["genetic factors", "environmental influences", "mental health conditions", "peer pressure"]
            },
            "Personality Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["rigid personality traits", "interpersonal difficulties", "maladaptive coping"],
                "additional_symptoms": ["emotional dysregulation", "impulsivity", "identity problems", "relationship instability"],
                "causes": ["childhood experiences", "genetic factors", "environmental influences", "attachment issues"]
            },
            "Mood Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium", "High"],
                "base_symptoms": ["depressed mood", "elevated mood", "mood instability"],
                "additional_symptoms": ["anhedonia", "sleep disturbances", "appetite changes", "cognitive symptoms"],
                "causes": ["genetic factors", "brain chemistry", "stress", "medical conditions", "substance use"]
            },
            "Anxiety Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["excessive worry", "fear", "nervousness"],
                "additional_symptoms": ["panic attacks", "avoidance behaviors", "physical symptoms", "cognitive distortions"],
                "causes": ["genetic factors", "brain chemistry", "stress", "trauma", "medical conditions"]
            },
            "Trauma-Related Disorders": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["intrusive memories", "avoidance", "hyperarousal"],
                "additional_symptoms": ["dissociation", "emotional numbness", "sleep disturbances", "concentration problems"],
                "causes": ["trauma exposure", "abuse", "violence", "accidents", "natural disasters"]
            },
            "Dissociative Disorders": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["dissociation", "identity confusion", "memory gaps"],
                "additional_symptoms": ["depersonalization", "derealization", "identity alteration", "fugue states"],
                "causes": ["severe trauma", "stress", "abuse", "dissociative coping mechanisms"]
            },
            "Somatic Symptom Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["physical symptoms", "excessive concern", "health anxiety"],
                "additional_symptoms": ["pain", "fatigue", "functional impairment", "medical utilization"],
                "causes": ["psychological factors", "stress", "trauma", "reinforcement of symptoms"]
            },
            "Neurodevelopmental Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["developmental delays", "cognitive impairments", "behavioral problems"],
                "additional_symptoms": ["communication difficulties", "social challenges", "adaptive functioning deficits"],
                "causes": ["genetic factors", "prenatal exposures", "perinatal complications", "environmental factors"]
            },
            "Neurocognitive Disorders": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["cognitive decline", "memory impairment", "executive dysfunction"],
                "additional_symptoms": ["language problems", "visuospatial difficulties", "personality changes"],
                "causes": ["Alzheimer's disease", "vascular disease", "Lewy body disease", "frontotemporal degeneration"]
            },
            "Elimination Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["enuresis", "encopresis", "inappropriate elimination"],
                "additional_symptoms": ["embarrassment", "social withdrawal", "behavioral problems"],
                "causes": ["developmental factors", "stress", "medical conditions", "toilet training issues"]
            },
            "Disruptive Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["aggressive behavior", "defiant behavior", "rule-breaking"],
                "additional_symptoms": ["irritability", "impulsivity", "social problems", "academic difficulties"],
                "causes": ["genetic factors", "environmental influences", "family dynamics", "neurobiological factors"]
            },
            " Tic Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["motor tics", "vocal tics", "involuntary movements"],
                "additional_symptoms": ["premonitory urges", "suppression ability", "waxing and waning", "comorbid conditions"],
                "causes": ["genetic factors", "neurochemical imbalances", "environmental triggers", "PANDAS"]
            },
            "Communication Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["speech difficulties", "language delays", "communication problems"],
                "additional_symptoms": ["articulation problems", "fluency issues", "voice disorders", "social communication deficits"],
                "causes": ["genetic factors", "neurological conditions", "hearing problems", "developmental factors"]
            },
            "Motor Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["coordination problems", "motor skill difficulties", "balance issues"],
                "additional_symptoms": ["clumsiness", "developmental delays", "fatigue", "muscle weakness"],
                "causes": ["neurological conditions", "developmental disorders", "genetic factors", "prematurity"]
            },
            "Factitious Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["feigned illness", "self-inflicted injury", "symptom fabrication"],
                "additional_symptoms": ["frequent hospitalizations", "multiple procedures", "inconsistent medical history"],
                "causes": ["psychological needs", "attention-seeking", "underlying mental health conditions"]
            },
            "Maladaptive Personality Patterns": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["rigid personality traits", "interpersonal difficulties", "maladaptive coping"],
                "additional_symptoms": ["emotional dysregulation", "impulsivity", "identity problems", "relationship instability"],
                "causes": ["childhood experiences", "genetic factors", "environmental influences", "attachment issues"]
            },
            "Impulse Control Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["impulsive behaviors", "loss of control", "urges"],
                "additional_symptoms": ["tension before acting", "pleasure during act", "regret afterward"],
                "causes": ["genetic factors", "brain chemistry", "stress", "trauma", "substance use"]
            },
            "Paraphilic Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["intense sexual urges", "atypical sexual interests", "distress"],
                "additional_symptoms": ["impairment in functioning", "harm to others", "legal problems"],
                "causes": ["developmental factors", "conditioning", "neurological factors", "psychological factors"]
            },
            "Gender Dysphoria": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["gender incongruence", "distress with assigned gender", "desire to be another gender"],
                "additional_symptoms": ["social transition", "medical transition", "mental health concerns"],
                "causes": ["biological factors", "neurological differences", "hormonal influences", "social factors"]
            },
            "Relational Problems": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["relationship difficulties", "communication problems", "conflict"],
                "additional_symptoms": ["attachment issues", "trust problems", "intimacy difficulties"],
                "causes": ["childhood experiences", "attachment styles", "communication patterns", "stress"]
            },
            "Grief Reactions": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["sadness", "yearning", "emotional pain"],
                "additional_symptoms": ["guilt", "anger", "anxiety", "depression"],
                "causes": ["loss of loved one", "significant life changes", "traumatic events"]
            },
            "Adjustment Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["emotional distress", "behavioral changes", "functional impairment"],
                "additional_symptoms": ["depression", "anxiety", "withdrawal", "acting out"],
                "causes": ["stressful life events", "major life changes", "trauma", "loss"]
            },
            "Acute Stress Disorder": {
                "category": "Disorder",
                "severity": ["Medium"],
                "base_symptoms": ["intrusive memories", "dissociation", "avoidance"],
                "additional_symptoms": ["hyperarousal", "sleep disturbances", "concentration problems"],
                "causes": ["traumatic events", "threat to life", "serious injury", "sexual violence"]
            },
            "Complex Post-Traumatic Stress Disorder": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["PTSD symptoms", "emotional dysregulation", "negative self-concept"],
                "additional_symptoms": ["interpersonal difficulties", "dissociation", "somatic symptoms"],
                "causes": ["prolonged trauma", "repeated abuse", "captivity", "organizational abuse"]
            },
            "Somatic Symptom Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["physical symptoms", "excessive concern", "health anxiety"],
                "additional_symptoms": ["pain", "fatigue", "functional impairment", "medical utilization"],
                "causes": ["psychological factors", "stress", "trauma", "reinforcement of symptoms"]
            },
            "Illness Anxiety Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["illness preoccupation", "health anxiety", "somatic symptoms"],
                "additional_symptoms": ["reassurance seeking", "avoidance of medical care", "functional impairment"],
                "causes": ["genetic factors", "learned behavior", "stress", "medical experiences"]
            },
            "Conversion Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["neurological symptoms", "functional impairment", "psychological distress"],
                "additional_symptoms": ["paralysis", "blindness", "seizures", "sensory loss"],
                "causes": ["psychological stress", "trauma", "unconscious conflict", "modeling"]
            },
            "Psychological Factors Affecting Medical Condition": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["worsening of medical condition", "non-adherence", "excessive symptoms"],
                "additional_symptoms": ["emotional distress", "behavioral problems", "interpersonal issues"],
                "causes": ["stress", "depression", "anxiety", "coping difficulties", "relationship problems"]
            },
            "Medication-Induced Movement Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["tremor", "rigidity", "bradykinesia"],
                "additional_symptoms": ["dystonia", "akathisia", "tardive dyskinesia", "restless legs"],
                "causes": ["antipsychotics", "anti-nausea drugs", "antidepressants", "long-term use"]
            },
            "Sleep-Related Movement Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["periodic limb movements", "restless legs", "sleep disruption"],
                "additional_symptoms": ["daytime fatigue", "insomnia", "impaired concentration"],
                "causes": ["genetic factors", "iron deficiency", "renal failure", "pregnancy"]
            },
            "Circadian Rhythm Sleep Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["insomnia", "excessive sleepiness", "sleep timing problems"],
                "additional_symptoms": ["jet lag", "shift work problems", "delayed sleep phase", "advanced sleep phase"],
                "causes": ["disruption of circadian rhythm", "travel", "shift work", "genetic factors"]
            },
            "Parasomnias": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["abnormal sleep behaviors", "sleepwalking", "night terrors"],
                "additional_symptoms": ["REM sleep behavior disorder", "sleep eating", "sleep sex"],
                "causes": ["genetic factors", "stress", "medications", "sleep deprivation", "neurological conditions"]
            },
            "Sleep-Related Breathing Disorders": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["snoring", "apneas", "daytime sleepiness"],
                "additional_symptoms": ["morning headaches", "irritability", "cognitive impairment", "cardiovascular problems"],
                "causes": ["obesity", "anatomical abnormalities", "neuromuscular disorders", "aging"]
            },
            "Central Disorders of Hypersomnolence": {
                "category": "Disorder",
                "severity": ["Medium"],
                "base_symptoms": ["excessive sleepiness", "long sleep duration", "sleep inertia"],
                "additional_symptoms": ["cataplexy", "sleep paralysis", "hypnagogic hallucinations"],
                "causes": ["idiopathic", "neurological conditions", "medications", "substance use"]
            },
            "Insomnia Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["difficulty falling asleep", "difficulty maintaining sleep", "early morning awakening"],
                "additional_symptoms": ["non-restorative sleep", "daytime impairment", "fatigue", "cognitive problems"],
                "causes": ["stress", "anxiety", "depression", "medical conditions", "medications", "poor sleep hygiene"]
            },
            "Hypersomnolence Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["excessive sleepiness", "prolonged sleep duration", "difficulty awakening"],
                "additional_symptoms": ["sleep inertia", "automatic behaviors", "cognitive impairment"],
                "causes": ["idiopathic", "neurological conditions", "medications", "environmental factors", "circadian factors"]
            },
            "Narcolepsy": {
                "category": "Disorder",
                "severity": ["Medium"],
                "base_symptoms": ["excessive daytime sleepiness", "cataplexy", "sleep paralysis"],
                "additional_symptoms": ["hypnagogic hallucinations", "fragmented nighttime sleep", "automatic behaviors"],
                "causes": ["genetic factors", "autoimmune destruction of hypocretin neurons", "brain injury"]
            },
            "Breathing-Related Sleep Disorders": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["snoring", "breathing pauses", "daytime sleepiness"],
                "additional_symptoms": ["morning headaches", "dry mouth", "nocturia", "cognitive impairment"],
                "causes": ["obesity", "anatomical abnormalities", "neuromuscular disorders", "congestive heart failure"]
            },
            "Central Sleep Apnea Syndromes": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["breathing pauses", "arousals", "oxygen desaturation"],
                "additional_symptoms": ["daytime sleepiness", "morning headaches", "cognitive impairment"],
                "causes": ["heart failure", "stroke", "neurological disorders", "opioid use", "high altitude"]
            },
            "Sleep-Related Hypoventilation Disorders": {
                "category": "Disorder",
                "severity": ["Medium", "High"],
                "base_symptoms": ["elevated CO2 levels", "oxygen desaturation", "daytime sleepiness"],
                "additional_symptoms": ["morning headaches", "fatigue", "cognitive impairment", "pulmonary hypertension"],
                "causes": ["obesity", "neuromuscular disorders", "chest wall abnormalities", "lung diseases"]
            },
            "Circadian Rhythm Sleep-Wake Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["insomnia", "excessive sleepiness", "misaligned sleep timing"],
                "additional_symptoms": ["jet lag", "shift work sleep disorder", "delayed sleep phase", "advanced sleep phase"],
                "causes": ["travel across time zones", "shift work", "genetic factors", "blindness", "neurological conditions"]
            },
            "Non-24-Hour Sleep-Wake Rhythm Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["progressive delay in sleep timing", "insomnia", "excessive sleepiness"],
                "additional_symptoms": ["free-running circadian rhythm", "social impairment", "work impairment"],
                "causes": ["blindness", "neurological conditions", "genetic factors", "aging"]
            },
            "Irregular Sleep-Wake Rhythm Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["irregular sleep timing", "multiple naps", "insomnia"],
                "additional_symptoms": ["daytime sleepiness", "cognitive impairment", "mood disturbances"],
                "causes": ["neurological conditions", "dementia", "developmental disabilities", "institutionalization"]
            },
            "Shift Work Sleep Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["insomnia", "excessive sleepiness", "fatigue"],
                "additional_symptoms": ["gastrointestinal problems", "cardiovascular problems", "mood disturbances"],
                "causes": ["shift work", "circadian rhythm disruption", "inadequate sleep opportunity"]
            },
            "Jet Lag Disorder": {
                "category": "Disorder",
                "severity": ["Low"],
                "base_symptoms": ["insomnia", "daytime sleepiness", "fatigue"],
                "additional_symptoms": ["gastrointestinal problems", "cognitive impairment", "mood changes"],
                "causes": ["rapid travel across time zones", "circadian rhythm disruption", "sleep deprivation"]
            },
            "Delayed Sleep Phase Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["delayed sleep onset", "delayed wake time", "insomnia"],
                "additional_symptoms": ["daytime sleepiness", "difficulty functioning in morning", "social impairment"],
                "causes": ["genetic factors", "circadian rhythm abnormalities", "environmental factors"]
            },
            "Advanced Sleep Phase Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["early sleep onset", "early wake time", "morning insomnia"],
                "additional_symptoms": ["evening sleepiness", "difficulty staying awake in evening", "social impairment"],
                "causes": ["genetic factors", "circadian rhythm abnormalities", "aging"]
            },
            "Non-Rapid Eye Movement Sleep Arousal Disorders": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["sleepwalking", "sleep terrors", "confusional arousals"],
                "additional_symptoms": ["inappropriate behavior", "amnesia for event", "injury risk"],
                "causes": ["genetic factors", "stress", "sleep deprivation", "fever", "medications"]
            },
            "Nightmare Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["frequent nightmares", "distressing dreams", "arousal from sleep"],
                "additional_symptoms": ["daytime distress", "sleep avoidance", "fatigue", "mood disturbances"],
                "causes": ["stress", "trauma", "medications", "substance withdrawal", "medical conditions"]
            },
            "Rapid Eye Movement Sleep Behavior Disorder": {
                "category": "Disorder",
                "severity": ["Medium"],
                "base_symptoms": ["dream enactment", "vocalizations", "movements during REM sleep"],
                "additional_symptoms": ["injury to self or bed partner", "daytime sleepiness", "cognitive impairment"],
                "causes": ["synucleinopathies", "Parkinson's disease", "multiple system atrophy", "medications"]
            },
            "Restless Legs Syndrome": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["urge to move legs", "uncomfortable sensations", "worse at rest"],
                "additional_symptoms": ["periodic limb movements", "sleep disturbance", "daytime fatigue"],
                "causes": ["genetic factors", "iron deficiency", "pregnancy", "chronic kidney disease", "neuropathy"]
            },
            "Periodic Limb Movement Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["limb movements during sleep", "arousals", "sleep fragmentation"],
                "additional_symptoms": ["daytime sleepiness", "fatigue", "cognitive impairment", "mood changes"],
                "causes": ["unknown", "neurological conditions", "medications", "sleep disorders"]
            },
            "Sleep-Related Leg Cramps": {
                "category": "Disorder",
                "severity": ["Low"],
                "base_symptoms": ["painful leg cramps", "sudden onset", "during sleep"],
                "additional_symptoms": ["muscle tightness", "arousal from sleep", "sleep disturbance"],
                "causes": ["unknown", "dehydration", "electrolyte imbalances", "neurological conditions", "medications"]
            },
            "Sleep-Related Bruxism": {
                "category": "Disorder",
                "severity": ["Low"],
                "base_symptoms": ["tooth grinding", "jaw clenching", "during sleep"],
                "additional_symptoms": ["tooth damage", "jaw pain", "headache", "sleep disturbance"],
                "causes": ["stress", "anxiety", "sleep disorders", "medications", "genetic factors"]
            },
            "Sleep-Related Rhythmic Movement Disorder": {
                "category": "Disorder",
                "severity": ["Low"],
                "base_symptoms": ["rhythmic movements", "head banging", "body rocking"],
                "additional_symptoms": ["during sleep onset", "arousals", "sleep disturbance"],
                "causes": ["developmental", "stress", "anxiety", "neurological conditions"]
            },
            "Benign Sleep Myoclonus of Infancy": {
                "category": "Disorder",
                "severity": ["Low"],
                "base_symptoms": ["myoclonic jerks", "during sleep", "infancy"],
                "additional_symptoms": ["brief movements", "no distress", "resolves spontaneously"],
                "causes": ["normal developmental phenomenon", "immaturity of nervous system"]
            },
            "Propriospinal Myoclonus at Sleep Onset": {
                "category": "Disorder",
                "severity": ["Low"],
                "base_symptoms": ["myoclonic jerks", "at sleep onset", "axial muscles"],
                "additional_symptoms": ["brief movements", "sleep disturbance", "nocturnal occurrence"],
                "causes": ["unknown", "neurological conditions", "medications", "stress"]
            },
            "Sleep-Related Painful Erections": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["painful erections", "during REM sleep", "nocturnal"],
                "additional_symptoms": ["arousal from sleep", "sleep disturbance", "sexual dysfunction"],
                "causes": ["unknown", "neurological conditions", "vascular problems", "medications"]
            },
            "Sleep-Related Disorders Not Otherwise Specified": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["various sleep-related symptoms", "not fitting other categories"],
                "additional_symptoms": ["sleep disturbance", "daytime impairment", "specific symptoms vary"],
                "causes": ["various", "medical conditions", "medications", "environmental factors"]
            },
            "Other Specified Insomnia Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["insomnia symptoms", "not meeting full criteria", "specific circumstances"],
                "additional_symptoms": ["sleep disturbance", "daytime impairment", "context-specific"],
                "causes": ["stress", "medical conditions", "medications", "environmental factors"]
            },
            "Other Specified Hypersomnolence Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["excessive sleepiness", "not meeting full criteria", "specific circumstances"],
                "additional_symptoms": ["prolonged sleep", "sleep inertia", "context-specific"],
                "causes": ["medical conditions", "medications", "environmental factors", "circadian factors"]
            },
            "Other Specified Sleep-Wake Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["sleep-wake disturbance", "not fitting other categories", "specific presentation"],
                "additional_symptoms": ["sleep disturbance", "daytime impairment", "context-specific"],
                "causes": ["various", "medical conditions", "medications", "environmental factors"]
            },
            "Unspecified Insomnia Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["insomnia symptoms", "insufficient information", "diagnostic uncertainty"],
                "additional_symptoms": ["sleep disturbance", "daytime impairment", "symptoms present"],
                "causes": ["unknown", "multiple possible factors", "awaiting further evaluation"]
            },
            "Unspecified Hypersomnolence Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["excessive sleepiness", "insufficient information", "diagnostic uncertainty"],
                "additional_symptoms": ["prolonged sleep", "sleep inertia", "symptoms present"],
                "causes": ["unknown", "multiple possible factors", "awaiting further evaluation"]
            },
            "Unspecified Sleep-Wake Disorder": {
                "category": "Disorder",
                "severity": ["Low", "Medium"],
                "base_symptoms": ["sleep-wake disturbance", "insufficient information", "diagnostic uncertainty"],
                "additional_symptoms": ["sleep disturbance", "daytime impairment", "symptoms present"],
                "causes": ["unknown", "multiple possible factors", "awaiting further evaluation"]
            }
        }

    def generate_symptoms(self, disease_data):
        """Generate realistic symptom combinations for a disease"""
        base_symptoms = disease_data["base_symptoms"]
        additional_symptoms = disease_data.get("additional_symptoms", [])

        # Always include base symptoms
        symptoms = base_symptoms.copy()

        # Add 1-4 additional symptoms randomly
        num_additional = random.randint(1, min(4, len(additional_symptoms)))
        if additional_symptoms:
            additional_to_add = random.sample(additional_symptoms, num_additional)
            symptoms.extend(additional_to_add)

        # Shuffle to vary order
        random.shuffle(symptoms)

        return symptoms

    def generate_entry(self, disease_name, disease_data):
        """Generate a single dataset entry"""
        symptoms = self.generate_symptoms(disease_data)
        severity = random.choice(disease_data["severity"])
        causes = disease_data["causes"]

        # Format symptoms as comma-separated string
        symptoms_str = ", ".join(symptoms)

        # Format causes as semicolon-separated string
        causes_str = "; ".join(causes)

        return {
            "Disease Name": disease_name,
            "Category": disease_data["category"],
            "Symptoms": symptoms_str,
            "Severity": severity,
            "Causes": causes_str
        }

    def generate_dataset(self, target_entries=15000):
        """Generate the complete dataset"""
        print(f"Generating {target_entries} entries...")

        disease_names = list(self.diseases_data.keys())
        entries_per_disease = target_entries // len(disease_names)
        remainder = target_entries % len(disease_names)

        dataset = []

        for i, disease_name in enumerate(disease_names):
            # Distribute entries evenly, with remainder going to first diseases
            num_entries = entries_per_disease + (1 if i < remainder else 0)

            for _ in range(num_entries):
                entry = self.generate_entry(disease_name, self.diseases_data[disease_name])
                dataset.append(entry)

        # Shuffle the dataset to avoid patterns
        random.shuffle(dataset)

        print(f"Generated {len(dataset)} entries successfully!")
        return dataset

    def save_to_csv(self, dataset, filename="expanded_medical_dataset.csv"):
        """Save the dataset to CSV format"""
        if not dataset:
            print("No dataset to save!")
            return

        fieldnames = ["Disease Name", "Category", "Symptoms", "Severity", "Causes"]

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)

        print(f"Dataset saved to {filename}")
        print(f"Total entries: {len(dataset)}")

    def save_to_json(self, dataset, filename="expanded_medical_dataset.json"):
        """Save the dataset to JSON format"""
        if not dataset:
            print("No dataset to save!")
            return

        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(dataset, jsonfile, indent=2, ensure_ascii=False)

        print(f"Dataset saved to {filename}")
        print(f"Total entries: {len(dataset)}")

# Main execution
if __name__ == "__main__":
    generator = MedicalDatasetGenerator()

    # Generate 15,000+ entries
    dataset = generator.generate_dataset(15000)

    # Save in both formats
    generator.save_to_csv(dataset)
    generator.save_to_json(dataset)

    print("\nDataset generation complete!")
    print("Files created:")
    print("- expanded_medical_dataset.csv")
    print("- expanded_medical_dataset.json")