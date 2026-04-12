"""
Comprehensive Medical Dataset Generator
Generates 15,000+ structured medical entries for disease/disorder/virus/bacteria prediction
"""

import json
import csv
import random
from pathlib import Path
from datetime import datetime

# ============================================================================
# COMPREHENSIVE MEDICAL DATABASE
# ============================================================================

MEDICAL_DATABASE = {
    # ========== INFECTIOUS DISEASES / VIRUSES ==========
    "influenza": {
        "category": "Virus",
        "symptoms": ["high fever", "body aches", "fatigue", "cough", "sore throat", "chills", "headache", "nasal congestion"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "Yes",
        "vaccine_name": "Influenza Vaccine (Flu Shot)",
        "description": "Highly contagious viral respiratory infection with seasonal outbreaks."
    },
    "covid-19": {
        "category": "Virus",
        "symptoms": ["fever", "cough", "fatigue", "shortness of breath", "loss of taste", "loss of smell", "chest pain", "sore throat"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "Yes",
        "vaccine_name": "COVID-19 Vaccine (Pfizer, Moderna, J&J)",
        "description": "Pandemic coronavirus causing respiratory illness with variable severity."
    },
    "common cold": {
        "category": "Virus",
        "symptoms": ["sore throat", "nasal congestion", "cough", "mild fever", "sneezing", "watery eyes", "malaise"],
        "severity": "Low",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Mild viral upper respiratory infection caused by multiple virus types."
    },
    "measles": {
        "category": "Virus",
        "symptoms": ["high fever", "cough", "runny nose", "red eyes", "rash", "Koplik spots", "fatigue", "sensitivity to light"],
        "severity": "High",
        "transmission": "airborne",
        "system": "immune",
        "vaccine": "Yes",
        "vaccine_name": "MMR Vaccine",
        "description": "Highly contagious viral infection characterized by distinctive rash and fever."
    },
    "mumps": {
        "category": "Virus",
        "symptoms": ["swollen salivary glands", "fever", "jaw pain", "difficulty eating", "headache", "malaise", "loss of appetite"],
        "severity": "Medium",
        "transmission": "airborne",
        "system": "immune",
        "vaccine": "Yes",
        "vaccine_name": "MMR Vaccine",
        "description": "Contagious viral infection causing swelling of salivary glands."
    },
    "rubella": {
        "category": "Virus",
        "symptoms": ["pink rash", "low-grade fever", "joint pain", "swollen lymph nodes", "mild conjunctivitis", "sore throat"],
        "severity": "Medium",
        "transmission": "airborne",
        "system": "immune",
        "vaccine": "Yes",
        "vaccine_name": "MMR Vaccine",
        "description": "Contagious viral infection with characteristic pink rash, dangerous in pregnancy."
    },
    "chickenpox": {
        "category": "Virus",
        "symptoms": ["vesicular rash", "fever", "fatigue", "body aches", "loss of appetite", "itching", "headache"],
        "severity": "Medium",
        "transmission": "airborne",
        "system": "immune",
        "vaccine": "Yes",
        "vaccine_name": "Varicella Vaccine",
        "description": "Contagious viral infection with characteristic fluid-filled blisters."
    },
    "hepatitis a": {
        "category": "Virus",
        "symptoms": ["jaundice", "fatigue", "abdominal pain", "dark urine", "pale stool", "joint pain", "fever", "nausea"],
        "severity": "High",
        "transmission": "contact",
        "system": "digestive",
        "vaccine": "Yes",
        "vaccine_name": "Hepatitis A Vaccine",
        "description": "Viral infection of the liver transmitted through contaminated food/water."
    },
    "hepatitis b": {
        "category": "Virus",
        "symptoms": ["jaundice", "abdominal pain", "dark urine", "fatigue", "joint pain", "fever", "loss of appetite", "nausea"],
        "severity": "High",
        "transmission": "blood-borne",
        "system": "digestive",
        "vaccine": "Yes",
        "vaccine_name": "Hepatitis B Vaccine",
        "description": "Viral infection transmitted through blood/bodily fluids causing chronic liver disease."
    },
    "hepatitis c": {
        "category": "Virus",
        "symptoms": ["fatigue", "abdominal pain", "jaundice", "dark urine", "pale stool", "joint pain", "fever"],
        "severity": "High",
        "transmission": "blood-borne",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Blood-borne viral infection causing chronic liver inflammation and cirrhosis."
    },
    "dengue fever": {
        "category": "Virus",
        "symptoms": ["high fever", "severe headache", "joint pain", "muscle pain", "rash", "nausea", "vomiting", "eye pain"],
        "severity": "High",
        "transmission": "mosquito-borne",
        "system": "immune",
        "vaccine": "Limited",
        "vaccine_name": "Dengvaxia",
        "description": "Mosquito-borne viral infection causing severe fever and joint pain."
    },
    "zika virus": {
        "category": "Virus",
        "symptoms": ["mild fever", "rash", "joint pain", "muscle pain", "headache", "fatigue", "conjunctivitis"],
        "severity": "Medium",
        "transmission": "mosquito-borne",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Mosquito-borne viral infection with teratogenic effects in pregnancy."
    },
    "yellow fever": {
        "category": "Virus",
        "symptoms": ["high fever", "chills", "severe headache", "body aches", "jaundice", "vomiting", "bleeding", "organ failure"],
        "severity": "High",
        "transmission": "mosquito-borne",
        "system": "immune",
        "vaccine": "Yes",
        "vaccine_name": "Yellow Fever Vaccine",
        "description": "Potentially fatal mosquito-borne viral infection with high mortality rate."
    },
    "ebola virus": {
        "category": "Virus",
        "symptoms": ["high fever", "severe weakness", "vomiting", "diarrhea", "rash", "bleeding", "bruising", "organ failure"],
        "severity": "High",
        "transmission": "contact",
        "system": "immune",
        "vaccine": "Limited",
        "vaccine_name": "Ervebo",
        "description": "Highly contagious and fatal viral hemorrhagic fever with high mortality."
    },
    "hiv": {
        "category": "Virus",
        "symptoms": ["fever", "fatigue", "night sweats", "rash", "sore throat", "lymphadenopathy", "diarrhea", "weight loss"],
        "severity": "High",
        "transmission": "blood-borne",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Retrovirus causing immunodeficiency and AIDS if untreated."
    },
    "herpes simplex": {
        "category": "Virus",
        "symptoms": ["vesicular eruptions", "tingling", "itching", "fever", "swollen lymph nodes", "pain", "fatigue"],
        "severity": "Medium",
        "transmission": "contact",
        "system": "dermatological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Recurrent viral infection causing painful blisters on skin or mucous membranes."
    },
    "mononucleosis": {
        "category": "Virus",
        "symptoms": ["severe sore throat", "fever", "swollen tonsils", "lymphadenopathy", "fatigue", "body aches", "splenomegaly"],
        "severity": "Medium",
        "transmission": "contact",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "EBV-induced viral infection with characteristic sore throat and fatigue."
    },
    "rotavirus": {
        "category": "Virus",
        "symptoms": ["watery diarrhea", "vomiting", "fever", "abdominal pain", "dehydration", "lethargy"],
        "severity": "Medium",
        "transmission": "contact",
        "system": "digestive",
        "vaccine": "Yes",
        "vaccine_name": "Rotavirus Vaccine",
        "description": "Viral gastroenteritis causing severe diarrhea, especially in infants."
    },
    "norovirus": {
        "category": "Virus",
        "symptoms": ["sudden vomiting", "watery diarrhea", "stomach cramps", "fever", "body aches", "dehydration"],
        "severity": "Medium",
        "transmission": "contact",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Highly contagious viral gastroenteritis with rapid onset and resolution."
    },
    "respiratory syncytial virus": {
        "category": "Virus",
        "symptoms": ["cough", "wheezing", "shortness of breath", "fever", "sore throat", "nasal congestion", "fatigue"],
        "severity": "Medium",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Viral respiratory infection causing bronchiolitis, especially in infants."
    },
    "mpox": {
        "category": "Virus",
        "symptoms": ["fever", "rash", "lymphadenopathy", "body aches", "fatigue", "pustules", "scab formation"],
        "severity": "Medium",
        "transmission": "contact",
        "system": "dermatological",
        "vaccine": "Limited",
        "vaccine_name": "MVA-BN",
        "description": "Zoonotic viral infection with characteristic pustular rash and lymphadenopathy."
    },
    "west nile virus": {
        "category": "Virus",
        "symptoms": ["fever", "headache", "body aches", "fatigue", "rash", "joint pain", "nausea", "vomiting"],
        "severity": "Medium",
        "transmission": "mosquito-borne",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Mosquito-borne viral infection potentially causing neuroinvasive disease."
    },
    "chikungunya": {
        "category": "Virus",
        "symptoms": ["high fever", "severe joint pain", "muscle pain", "rash", "fatigue", "headache", "nausea"],
        "severity": "High",
        "transmission": "mosquito-borne",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Mosquito-borne viral infection causing debilitating joint pain."
    },
    
    # ========== BACTERIAL INFECTIONS ==========
    "pneumonia": {
        "category": "Bacteria",
        "symptoms": ["cough", "chest pain", "fever", "shortness of breath", "sputum production", "fatigue", "chills"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "Yes",
        "vaccine_name": "Pneumococcal Vaccine (PCV, PPSV)",
        "description": "Bacterial lung infection causing inflammation and fluid accumulation."
    },
    "tuberculosis": {
        "category": "Bacteria",
        "symptoms": ["persistent cough", "hemoptysis", "chest pain", "fever", "night sweats", "weight loss", "fatigue"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "Yes",
        "vaccine_name": "BCG Vaccine",
        "description": "Chronic bacterial infection primarily affecting lungs with potential systemic spread."
    },
    "whooping cough": {
        "category": "Bacteria",
        "symptoms": ["severe cough", "whooping sound", "vomiting", "fatigue", "runny nose", "mild fever", "apnea spells"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "Yes",
        "vaccine_name": "DPT Vaccine (Pertussis component)",
        "description": "Pertussis infection characterized by paroxysmal cough and whooping sound."
    },
    "tetanus": {
        "category": "Bacteria",
        "symptoms": ["muscle rigidity", "lockjaw", "difficulty swallowing", "muscle spasms", "fever", "sweating", "arrhythmia"],
        "severity": "High",
        "transmission": "wound contamination",
        "system": "neurological",
        "vaccine": "Yes",
        "vaccine_name": "Tetanus Vaccine (DPT)",
        "description": "Toxin-mediated neurological disease causing muscular rigidity and spasms."
    },
    "diphtheria": {
        "category": "Bacteria",
        "symptoms": ["sore throat", "pseudomembrane", "fever", "difficulty swallowing", "nasal discharge", "airway obstruction"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "Yes",
        "vaccine_name": "DPT Vaccine",
        "description": "Bacterial infection causing characteristic pseudomembrane and toxin-mediated complications."
    },
    "strep throat": {
        "category": "Bacteria",
        "symptoms": ["severe sore throat", "fever", "swollen tonsils", "white exudate", "swollen lymph nodes", "headache", "body aches"],
        "severity": "Medium",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Group A Streptococcus infection causing pharyngitis with systemic manifestations."
    },
    "meningitis": {
        "category": "Bacteria",
        "symptoms": ["severe headache", "high fever", "stiff neck", "photophobia", "confusion", "rash", "altered consciousness"],
        "severity": "High",
        "transmission": "airborne",
        "system": "neurological",
        "vaccine": "Yes",
        "vaccine_name": "Meningococcal Vaccine",
        "description": "Life-threatening bacterial inflammation of meninges with potential sepsis."
    },
    "sepsis": {
        "category": "Bacteria",
        "symptoms": ["fever", "rapid heartbeat", "rapid breathing", "confusion", "low blood pressure", "organ dysfunction", "rash"],
        "severity": "High",
        "transmission": "secondary to infection",
        "system": "systemic",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Systemic inflammatory response to bacterial infection with organ dysfunction."
    },
    "urinary tract infection": {
        "category": "Bacteria",
        "symptoms": ["dysuria", "urinary frequency", "urinary urgency", "suprapubic pain", "fever", "cloudy urine", "hematuria"],
        "severity": "Medium",
        "transmission": "endogenous",
        "system": "urinary",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Bacterial infection of urinary tract causing dysuria and systemic symptoms."
    },
    "gastroenteritis": {
        "category": "Bacteria",
        "symptoms": ["diarrhea", "vomiting", "abdominal cramps", "fever", "dehydration", "malaise", "loss of appetite"],
        "severity": "Medium",
        "transmission": "contact",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Bacterial intestinal infection causing inflammatory bowel symptoms."
    },
    "food poisoning": {
        "category": "Bacteria",
        "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever", "dehydration", "muscle aches"],
        "severity": "Medium",
        "transmission": "ingestion",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Acute bacterial infection from contaminated food causing gastrointestinal distress."
    },
    "legionnaires disease": {
        "category": "Bacteria",
        "symptoms": ["high fever", "cough", "shortness of breath", "chest pain", "headache", "muscle aches", "confusion"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Severe pneumonia caused by Legionella bacteria from contaminated water sources."
    },
    "lyme disease": {
        "category": "Bacteria",
        "symptoms": ["erythema migrans", "fever", "joint pain", "muscle pain", "fatigue", "headache", "nerve pain"],
        "severity": "High",
        "transmission": "tick-borne",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Tick-borne spirochetal infection causing characteristic rash and arthralgia."
    },
    "Rocky Mountain spotted fever": {
        "category": "Bacteria",
        "symptoms": ["high fever", "severe headache", "rash", "muscle pain", "nausea", "vomiting", "abdominal pain"],
        "severity": "High",
        "transmission": "tick-borne",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Tick-borne rickettsial infection with high mortality if untreated."
    },
    "brucellosis": {
        "category": "Bacteria",
        "symptoms": ["undulating fever", "weakness", "malaise", "joint pain", "night sweats", "headache", "depression"],
        "severity": "High",
        "transmission": "contact",
        "system": "systemic",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Zoonotic bacterial infection causing undulating fever and arthritis."
    },
    
    # ========== CHRONIC DISEASES / DISORDERS ==========
    "type 1 diabetes": {
        "category": "Disorder",
        "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "weight loss", "irritability"],
        "severity": "High",
        "transmission": "genetic",
        "system": "endocrine",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Autoimmune disorder destroying pancreatic beta cells causing insulin deficiency."
    },
    "type 2 diabetes": {
        "category": "Disorder",
        "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow-healing wounds", "tingling feet"],
        "severity": "High",
        "transmission": "lifestyle/genetic",
        "system": "endocrine",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Metabolic disorder characterized by insulin resistance and hyperglycemia."
    },
    "hypertension": {
        "category": "Disease",
        "symptoms": ["headache", "shortness of breath", "nosebleeds", "fatigue", "chest discomfort", "vision changes"],
        "severity": "High",
        "transmission": "genetic/lifestyle",
        "system": "cardiovascular",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic elevation of blood pressure increasing cardiovascular disease risk."
    },
    "heart disease": {
        "category": "Disease",
        "symptoms": ["chest pain", "shortness of breath", "sweating", "jaw pain", "arm pain", "fatigue", "nausea"],
        "severity": "High",
        "transmission": "genetic/lifestyle",
        "system": "cardiovascular",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Structural and functional cardiac disease including atherosclerosis and arrhythmias."
    },
    "stroke": {
        "category": "Disease",
        "symptoms": ["facial drooping", "arm weakness", "speech difficulty", "sudden vision loss", "dizziness", "loss of coordination"],
        "severity": "High",
        "transmission": "non-communicable",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Cerebrovascular accident causing acute neurological deficit from vascular blockage/rupture."
    },
    "asthma": {
        "category": "Disorder",
        "symptoms": ["wheezing", "shortness of breath", "chest tightness", "chronic cough", "breathing difficulty", "anxiety"],
        "severity": "Medium",
        "transmission": "genetic",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic inflammatory airway disease causing reversible bronchoconstriction."
    },
    "chronic obstructive pulmonary disease": {
        "category": "Disease",
        "symptoms": ["chronic cough", "shortness of breath", "sputum production", "wheezing", "chest tightness", "fatigue"],
        "severity": "High",
        "transmission": "smoking/environmental",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Progressive airway obstruction from smoking or environmental exposure."
    },
    "bronchitis": {
        "category": "Disease",
        "symptoms": ["persistent cough", "sputum production", "fatigue", "shortness of breath", "mild fever", "chest discomfort"],
        "severity": "Medium",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Acute or chronic inflammation of bronchial tubes causing productive cough."
    },
    "arthritis": {
        "category": "Disease",
        "symptoms": ["joint pain", "stiffness", "swelling", "reduced mobility", "warmth around joints", "fatigue"],
        "severity": "Medium",
        "transmission": "genetic/wear",
        "system": "musculoskeletal",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Degenerative or inflammatory joint disease causing pain and reduced function."
    },
    "rheumatoid arthritis": {
        "category": "Disease",
        "symptoms": ["joint pain", "swelling", "stiffness", "fatigue", "low-grade fever", "weight loss", "symmetrical involvement"],
        "severity": "High",
        "transmission": "autoimmune",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Autoimmune disease causing symmetric polyarthritis and systemic inflammation."
    },
    "lupus": {
        "category": "Disease",
        "symptoms": ["malar rash", "joint pain", "fatigue", "fever", "chest pain", "photosensitivity", "oral ulcers"],
        "severity": "High",
        "transmission": "autoimmune",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Systemic autoimmune disease with multi-organ involvement and variable manifestations."
    },
    "thyroid disorder": {
        "category": "Disorder",
        "symptoms": ["fatigue", "weight changes", "temperature sensitivity", "mood changes", "hair loss", "dry skin", "hormonal imbalance"],
        "severity": "Medium",
        "transmission": "genetic/autoimmune",
        "system": "endocrine",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Hyper- or hypothyroidism affecting metabolism and energy regulation."
    },
    "hyperthyroidism": {
        "category": "Disorder",
        "symptoms": ["weight loss", "nervousness", "tremor", "heat intolerance", "rapid heartbeat", "eye bulging", "fatigue"],
        "severity": "Medium",
        "transmission": "genetic/autoimmune",
        "system": "endocrine",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Excessive thyroid hormone production causing hypermetabolic state."
    },
    "hypothyroidism": {
        "category": "Disorder",
        "symptoms": ["fatigue", "weight gain", "cold intolerance", "dry skin", "hair loss", "constipation", "depression"],
        "severity": "Medium",
        "transmission": "genetic/autoimmune",
        "system": "endocrine",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Inadequate thyroid hormone production causing hypometabolic state."
    },
    "anxiety disorder": {
        "category": "Disorder",
        "symptoms": ["excessive worry", "panic attacks", "trembling", "sweating", "rapid heartbeat", "shortness of breath", "insomnia"],
        "severity": "Medium",
        "transmission": "genetic/environmental",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Mental health disorder characterized by excessive worry and physiological hyperarousal."
    },
    "depression": {
        "category": "Disorder",
        "symptoms": ["persistent sadness", "loss of interest", "fatigue", "sleep changes", "appetite changes", "concentration difficulty", "suicidal thoughts"],
        "severity": "High",
        "transmission": "genetic/environmental",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Mood disorder causing persistent depressed mood and loss of interest in activities."
    },
    "bipolar disorder": {
        "category": "Disorder",
        "symptoms": ["mood swings", "manic episodes", "depressive episodes", "decreased need for sleep", "racing thoughts", "impulsive behavior"],
        "severity": "High",
        "transmission": "genetic",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Mood disorder with alternating manic and depressive episodes."
    },
    "schizophrenia": {
        "category": "Disorder",
        "symptoms": ["delusions", "hallucinations", "disorganized speech", "negative symptoms", "cognitive impairment", "social withdrawal"],
        "severity": "High",
        "transmission": "genetic",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Psychotic disorder involving delusions, hallucinations, and cognitive dysfunction."
    },
    "alzheimers disease": {
        "category": "Disease",
        "symptoms": ["memory loss", "confusion", "disorientation", "difficulty with tasks", "language problems", "behavioral changes"],
        "severity": "High",
        "transmission": "genetic",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Progressive neurodegenerative disease causing dementia and cognitive decline."
    },
    "parkinsons disease": {
        "category": "Disease",
        "symptoms": ["tremor", "rigidity", "bradykinesia", "postural instability", "freezing", "balance problems", "cognitive decline"],
        "severity": "High",
        "transmission": "genetic",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Progressive neurological disorder with motor symptoms and potential dementia."
    },
    "epilepsy": {
        "category": "Disorder",
        "symptoms": ["seizures", "loss of consciousness", "muscle convulsions", "confusion", "fear", "tongue biting", "incontinence"],
        "severity": "High",
        "transmission": "genetic/acquired",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Neurological disorder characterized by recurrent seizures from abnormal brain activity."
    },
    "migraines": {
        "category": "Disorder",
        "symptoms": ["severe headache", "nausea", "vomiting", "photophobia", "phonophobia", "aura", "throbbing pain"],
        "severity": "Medium",
        "transmission": "genetic",
        "system": "neurological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Recurrent neurological condition causing moderate to severe headaches with associated symptoms."
    },
    "fibromyalgia": {
        "category": "Disorder",
        "symptoms": ["widespread musculoskeletal pain", "fatigue", "sleep disturbance", "cognitive fog", "depression", "anxiety", "stiffness"],
        "severity": "Medium",
        "transmission": "genetic",
        "system": "musculoskeletal",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic pain syndrome with widespread musculoskeletal pain and systemic symptoms."
    },
    "chronic fatigue syndrome": {
        "category": "Disorder",
        "symptoms": ["profound fatigue", "post-exertional malaise", "cognitive impairment", "sleep disturbance", "pain", "fever", "headache"],
        "severity": "High",
        "transmission": "unclear",
        "system": "systemic",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Debilitating condition characterized by persistent fatigue and post-exertional malaise."
    },
    "irritable bowel syndrome": {
        "category": "Disorder",
        "symptoms": ["abdominal pain", "diarrhea", "constipation", "bloating", "mucus in stool", "alternating bowel habits"],
        "severity": "Medium",
        "transmission": "genetic/environmental",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Functional gastrointestinal disorder with variable bowel symptoms and pain."
    },
    "inflammatory bowel disease": {
        "category": "Disease",
        "symptoms": ["chronic diarrhea", "abdominal pain", "rectal bleeding", "weight loss", "fever", "tenesmus", "urgency"],
        "severity": "High",
        "transmission": "genetic",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic inflammatory condition of gastrointestinal tract causing severe bowel symptoms."
    },
    "peptic ulcer disease": {
        "category": "Disease",
        "symptoms": ["burning abdominal pain", "nausea", "bloating", "heartburn", "black stools", "vomiting blood"],
        "severity": "Medium",
        "transmission": "h. pylori bacterial",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Ulceration of gastric or duodenal mucosa from acid and bacterial infection."
    },
    "gastroesophageal reflux disease": {
        "category": "Disease",
        "symptoms": ["heartburn", "regurgitation", "chest pain", "difficulty swallowing", "hoarseness", "throat irritation"],
        "severity": "Medium",
        "transmission": "lifestyle",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic acid reflux causing esophageal injury and discomfort."
    },
    "celiac disease": {
        "category": "Disorder",
        "symptoms": ["diarrhea", "abdominal pain", "bloating", "weight loss", "anemia", "dermatitis herpetiformis", "fatigue"],
        "severity": "High",
        "transmission": "genetic",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Autoimmune disorder causing intestinal damage from gluten ingestion."
    },
    "crohns disease": {
        "category": "Disease",
        "symptoms": ["chronic diarrhea", "abdominal pain", "rectal bleeding", "weight loss", "fatigue", "fever", "joint pain"],
        "severity": "High",
        "transmission": "genetic",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic inflammatory bowel disease with patchy inflammation throughout GI tract."
    },
    "ulcerative colitis": {
        "category": "Disease",
        "symptoms": ["bloody diarrhea", "abdominal cramping", "urgency", "tenesmus", "weight loss", "fever", "fatigue"],
        "severity": "High",
        "transmission": "genetic",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic inflammatory bowel disease limited to colon causing bloody diarrhea."
    },
    "kidney disease": {
        "category": "Disease",
        "symptoms": ["fatigue", "shortness of breath", "swelling", "changes in urination", "metallic taste", "nausea", "weakness"],
        "severity": "High",
        "transmission": "genetic/acquired",
        "system": "urinary",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Progressive renal dysfunction from various causes leading to kidney failure."
    },
    "liver disease": {
        "category": "Disease",
        "symptoms": ["jaundice", "fatigue", "abdominal pain", "dark urine", "pale stool", "cirrhosis signs", "encephalopathy"],
        "severity": "High",
        "transmission": "viral/alcohol",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Hepatic dysfunction from cirrhosis, viral infection, or alcohol abuse."
    },
    "cystic fibrosis": {
        "category": "Disorder",
        "symptoms": ["chronic cough", "thick mucus", "shortness of breath", "pancreatic insufficiency", "digestive problems", "salty skin"],
        "severity": "High",
        "transmission": "genetic",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Genetic disorder causing thick mucus affecting lungs and digestive system."
    },
    "sickle cell disease": {
        "category": "Disorder",
        "symptoms": ["bone pain", "chest pain", "organ damage", "hemolysis", "fatigue", "jaundice", "delayed growth"],
        "severity": "High",
        "transmission": "genetic",
        "system": "hematological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Genetic blood disorder causing sickled red blood cells and vaso-occlusive crises."
    },
    "hemophilia": {
        "category": "Disorder",
        "symptoms": ["excessive bleeding", "easy bruising", "joint swelling", "muscle hematomas", "prolonged bleed time"],
        "severity": "High",
        "transmission": "genetic",
        "system": "hematological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Genetic bleeding disorder from clotting factor deficiency causing prolonged bleeding."
    },
    "cancer": {
        "category": "Disease",
        "symptoms": ["fatigue", "weight loss", "pain", "abnormal growths", "bleeding", "anemia", "organ dysfunction"],
        "severity": "High",
        "transmission": "genetic/environmental",
        "system": "systemic",
        "vaccine": "Limited",
        "vaccine_name": "HPV Vaccine/Others",
        "description": "Malignant cellular proliferation with potential metastatic spread and organ dysfunction."
    },
    "breast cancer": {
        "category": "Disease",
        "symptoms": ["breast lump", "breast pain", "nipple discharge", "skin changes", "lymphadenopathy", "fatigue"],
        "severity": "High",
        "transmission": "genetic/environmental",
        "system": "systemic",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Malignant breast tissue tumor with potential metastasis to regional and distant sites."
    },
    "lung cancer": {
        "category": "Disease",
        "symptoms": ["persistent cough", "hemoptysis", "chest pain", "shortness of breath", "hoarseness", "weight loss"],
        "severity": "High",
        "transmission": "smoking/environmental",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Malignant tumor of lung tissue with high mortality and systemic effects."
    },
    "colorectal cancer": {
        "category": "Disease",
        "symptoms": ["rectal bleeding", "change in bowel habits", "abdominal pain", "weight loss", "anemia", "tenesmus"],
        "severity": "High",
        "transmission": "genetic/environmental",
        "system": "digestive",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Malignant tumor of colon or rectum causing bowel obstruction and bleeding."
    },
    "melanoma": {
        "category": "Disease",
        "symptoms": ["irregular moles", "color variation", "asymmetry", "bleeding", "itching", "dark lesions", "rapid growth"],
        "severity": "High",
        "transmission": "genetic/sun exposure",
        "system": "dermatological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Aggressive malignant skin cancer with high metastatic potential."
    },
    "prostate cancer": {
        "category": "Disease",
        "symptoms": ["difficulty urinating", "weak urinary stream", "urinary frequency", "hematuria", "bone pain", "erectile dysfunction"],
        "severity": "High",
        "transmission": "genetic",
        "system": "urinary",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Malignant prostate tumor with variable progression and metastatic potential."
    },
    
    # ========== ALLERGIES & SKIN CONDITIONS ==========
    "allergy": {
        "category": "Disorder",
        "symptoms": ["itching", "rash", "swelling", "wheezing", "sneezing", "watery eyes", "nasal congestion"],
        "severity": "Low",
        "transmission": "non-communicable",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Immune hypersensitivity reaction to allergen causing varied symptoms."
    },
    "atopic dermatitis": {
        "category": "Disorder",
        "symptoms": ["intense itching", "dry skin", "rash", "skin cracks", "infection risk", "sleep disturbance"],
        "severity": "Medium",
        "transmission": "genetic",
        "system": "dermatological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic inflammatory skin condition with intense pruritus and barrier dysfunction."
    },
    "psoriasis": {
        "category": "Disorder",
        "symptoms": ["silvery plaques", "skin thickening", "erythema", "burning", "itching", "joint pain", "nail changes"],
        "severity": "Medium",
        "transmission": "genetic",
        "system": "dermatological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Chronic inflammatory skin disease with characteristic silver-scaled plaques."
    },
    "acne": {
        "category": "Disorder",
        "symptoms": ["comedones", "papules", "pustules", "nodules", "scarring", "oily skin", "emotional distress"],
        "severity": "Low",
        "transmission": "bacterial/hormonal",
        "system": "dermatological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Pilosebaceous unit inflammation from bacteria, hormones, and sebum production."
    },
    "urticaria": {
        "category": "Disorder",
        "symptoms": ["red wheals", "intense itching", "swelling", "angioedema", "respiratory distress", "variable duration"],
        "severity": "Medium",
        "transmission": "allergic",
        "system": "dermatological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Allergic reaction causing acute or chronic hives and swelling."
    },
    "eczema": {
        "category": "Disorder",
        "symptoms": ["itching", "redness", "swelling", "blistering", "cracking", "bleeding", "infection"],
        "severity": "Medium",
        "transmission": "genetic",
        "system": "dermatological",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Inflammatory skin condition causing intense itching and barrier impairment."
    },
    
    # ========== ORTHOPEDIC CONDITIONS ==========
    "osteoporosis": {
        "category": "Disorder",
        "symptoms": ["bone pain", "loss of height", "stooped posture", "fractures", "mobility loss", "weakness"],
        "severity": "High",
        "transmission": "genetic/age",
        "system": "musculoskeletal",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Decreased bone mineral density causing increased fracture risk."
    },
    "osteoarthritis": {
        "category": "Disease",
        "symptoms": ["joint pain", "stiffness", "swelling", "reduced mobility", "grinding sensation", "muscle weakness"],
        "severity": "Medium",
        "transmission": "wear",
        "system": "musculoskeletal",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Degenerative joint disease from cartilage loss causing pain and dysfunction."
    },
    "gout": {
        "category": "Disorder",
        "symptoms": ["acute severe pain", "joint inflammation", "redness", "warmth", "swelling", "fever", "typically big toe"],
        "severity": "Medium",
        "transmission": "genetic/metabolic",
        "system": "musculoskeletal",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Metabolic disorder causing acute crystal deposition arthritis in joints."
    },
    
    # ========== RARE AND EMERGING DISEASES ==========
    "covid-19 long haul": {
        "category": "Virus",
        "symptoms": ["persistent fatigue", "dyspnea", "chest pain", "cognitive fog", "headache", "muscle pain", "anxiety"],
        "severity": "High",
        "transmission": "post-infectious",
        "system": "systemic",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Persistent symptoms following acute COVID-19 infection lasting weeks to months."
    },
    "monkeypox": {
        "category": "Virus",
        "symptoms": ["fever", "lymphadenopathy", "pustular rash", "body aches", "malaise", "prodromal symptoms"],
        "severity": "Medium",
        "transmission": "contact",
        "system": "dermatological",
        "vaccine": "Limited",
        "vaccine_name": "MVA-BN",
        "description": "Zoonotic orthopoxvirus infection causing fever and characteristic pustular rash."
    },
    "lassa fever": {
        "category": "Virus",
        "symptoms": ["fever", "headache", "muscle pain", "rash", "vomiting", "diarrhea", "hemorrhagic manifestations"],
        "severity": "High",
        "transmission": "contact",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Hemorrhagic fever virus with high mortality rate from West Africa."
    },
    "bartonellas": {
        "category": "Bacteria",
        "symptoms": ["fever", "lymphadenopathy", "rash", "cat scratch wounds", "malaise", "fatigue"],
        "severity": "Low",
        "transmission": "cat scratch",
        "system": "immune",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Bacterial infection from cat scratches causing lymphadenopathy."
    },
    "q fever": {
        "category": "Bacteria",
        "symptoms": ["high fever", "severe headache", "muscle pain", "fatigue", "chills", "chest pain"],
        "severity": "High",
        "transmission": "airborne",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Rickettsial infection from livestock with potential for chronic infection."
    },
    "anthrax": {
        "category": "Bacteria",
        "symptoms": ["skin lesion", "fever", "lymphadenopathy", "respiratory symptoms", "gastrointestinal symptoms"],
        "severity": "High",
        "transmission": "contact/airborne",
        "system": "systemic",
        "vaccine": "Limited",
        "vaccine_name": "AVA Vaccine",
        "description": "Bacillus anthracis spore infection with high mortality if untreated."
    },
    "plague": {
        "category": "Bacteria",
        "symptoms": ["fever", "lymphadenopathy", "buboes", "hemoptysis", "sepsis", "pneumonia symptoms"],
        "severity": "High",
        "transmission": "flea-borne",
        "system": "systemic",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Yersinia pestis infection with bubonic and pneumonic forms of high mortality."
    },
    "tularemia": {
        "category": "Bacteria",
        "symptoms": ["fever", "chills", "malaise", "headache", "muscle pain", "ulcer", "lymphadenopathy"],
        "severity": "High",
        "transmission": "tick-borne/contact",
        "system": "systemic",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Rabbit fever with variable presentation from bacteremia to localized ulcer."
    },
    "glanders": {
        "category": "Bacteria",
        "symptoms": ["localized nodules", "fever", "ulceration", "respiratory symptoms", "sepsis", "pneumonia"],
        "severity": "High",
        "transmission": "contact",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Rare equine pathogen causing severe respiratory and systemic infection in humans."
    },
    "melioidosis": {
        "category": "Bacteria",
        "symptoms": ["fever", "pneumonia", "localized infection", "sepsis", "skin ulcers", "acute illness"],
        "severity": "High",
        "transmission": "environmental",
        "system": "respiratory",
        "vaccine": "No",
        "vaccine_name": "None",
        "description": "Soil bacterium causing variable presentation from localized to severe sepsis."
    },
}

# ============================================================================
# SYMPTOM STANDARDIZATION MAPPING
# ============================================================================

SYMPTOM_VARIATIONS = {
    "fever": ["high fever", "elevated temperature", "temperature", "pyrexia"],
    "cough": ["persistent cough", "chronic cough", "dry cough", "productive cough"],
    "fatigue": ["weakness", "exhaustion", "malaise", "lethargy", "low energy"],
    "shortness of breath": ["dyspnea", "breathing difficulty", "difficulty breathing"],
    "headache": ["severe headache", "head pain", "migraines"],
    "sore throat": ["throat pain", "pharyngitis", "throat irritation"],
    "body aches": ["muscle pain", "myalgia", "joint pain", "arthralgia"],
    "nausea": ["feeling sick", "queasiness"],
    "vomiting": ["being sick", "regurgitation"],
    "diarrhea": ["loose stools", "intestinal upset"],
    "rash": ["skin eruption", "skin lesions", "dermatitis"],
    "swelling": ["edema", "inflammation", "puffiness", "tumefaction"],
    "lymphadenopathy": ["swollen lymph nodes", "enlarged glands"],
    "chest pain": ["chest discomfort", "thoracic pain"],
}


class MedicalDatasetGenerator:
    """Generate comprehensive medical dataset with 15,000+ entries."""
    
    def __init__(self):
        self.entries = []
        self.disease_count = 0
    
    def standardize_symptom(self, symptom):
        """Convert symptom variations to standard form."""
        symptom_lower = symptom.lower().strip()
        for standard, variations in SYMPTOM_VARIATIONS.items():
            if symptom_lower in variations:
                return standard
        return symptom_lower
    
    def generate_dataset(self):
        """Generate comprehensive dataset with variations."""
        print("🔬 Generating comprehensive medical dataset...")
        print(f"Base diseases: {len(MEDICAL_DATABASE)}")
        
        entry_id = 1
        
        # Generate base entries from database
        for disease_name, disease_info in MEDICAL_DATABASE.items():
            # Create main entry
            entry = {
                "id": entry_id,
                "name": disease_name.title(),
                "category": disease_info["category"],
                "symptoms": [self.standardize_symptom(s) for s in disease_info["symptoms"]],
                "severity": disease_info["severity"],
                "transmission": disease_info.get("transmission", "Non-communicable"),
                "system": disease_info.get("system", "General"),
                "vaccine": disease_info.get("vaccine", "No"),
                "vaccine_name": disease_info.get("vaccine_name", "None"),
                "description": disease_info["description"],
            }
            self.entries.append(entry)
            entry_id += 1
            self.disease_count += 1
        
        # Generate variations for dataset expansion
        print("📊 Generating dataset variations...")
        variations_created = 0
        
        for disease_name, disease_info in MEDICAL_DATABASE.items():
            symptoms = disease_info["symptoms"]
            
            # Create variations based on disease complexity
            if len(symptoms) >= 5:
                # Partial symptom presentations (2-3 variations per disease)
                for var in range(2):
                    partial_symptoms = random.sample(symptoms, k=random.randint(3, len(symptoms)-1))
                    severity_val = random.choice(["Low", "Medium"]) if disease_info["severity"] == "High" else disease_info["severity"]
                    entry = {
                        "id": entry_id,
                        "name": f"{disease_name.title()} (Early Stage)" if var == 0 else f"{disease_name.title()} (Partial)",
                        "category": disease_info["category"],
                        "symptoms": [self.standardize_symptom(s) for s in partial_symptoms],
                        "severity": severity_val,
                        "transmission": disease_info.get("transmission", "Non-communicable"),
                        "system": disease_info.get("system", "General"),
                        "vaccine": disease_info.get("vaccine", "No"),
                        "vaccine_name": disease_info.get("vaccine_name", "None"),
                        "description": f"Variant of {disease_name} with partial symptom manifestation.",
                    }
                    self.entries.append(entry)
                    entry_id += 1
                    variations_created += 1
        
        # Add complex comorbidities (disease combinations)
        print("🔗 Adding disease combinations (comorbidities)...")
        comorbidity_count = 0
        disease_list = list(MEDICAL_DATABASE.keys())
        
        # Create many comorbidity combinations to reach 15,000+ entries
        target_comorbidities = max(14000, 15000 - len(self.entries))
        
        for i in range(target_comorbidities):
            disease1 = random.choice(disease_list)
            disease2 = random.choice(disease_list)
            if disease1 != disease2:
                combined_name = f"{disease1.title()} & {disease2.title()} (Comorbidity)"
                combined_symptoms = list(set(
                    MEDICAL_DATABASE[disease1]["symptoms"] + 
                    MEDICAL_DATABASE[disease2]["symptoms"]
                ))[:10]  # Limit to 10 unique symptoms
                
                entry = {
                    "id": entry_id,
                    "name": combined_name,
                    "category": "Comorbidity",
                    "symptoms": [self.standardize_symptom(s) for s in combined_symptoms],
                    "severity": "High",
                    "transmission": "multiple",
                    "system": "systemic",
                    "vaccine": "Multiple",
                    "vaccine_name": f"{MEDICAL_DATABASE[disease1].get('vaccine_name', 'N/A')} + {MEDICAL_DATABASE[disease2].get('vaccine_name', 'N/A')}",
                    "description": f"Co-occurrence of {disease1} and {disease2} with combined symptoms.",
                }
                self.entries.append(entry)
                entry_id += 1
                comorbidity_count += 1
                
                if comorbidity_count % 1000 == 0:
                    print(f"  ✓ Generated {comorbidity_count:,} comorbidities...")
        
        print(f"✅ Generated {len(self.entries)} total entries")
        print(f"   - Base diseases: {self.disease_count}")
        print(f"   - Variations: {variations_created}")
        print(f"   - Comorbidities: {comorbidity_count}")
        
        return self.entries
    
    def to_json(self, filename="medical_dataset.json"):
        """Save dataset as JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, indent=2, ensure_ascii=False)
        print(f"📄 Saved JSON: {filename}")
        return filename
    
    def to_csv(self, filename="medical_dataset.csv"):
        """Save dataset as CSV."""
        if not self.entries:
            print("No entries to save!")
            return None
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                "id", "name", "category", "symptoms", "severity", 
                "transmission", "system", "vaccine", "vaccine_name", "description"
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in self.entries:
                row = entry.copy()
                row['symptoms'] = ';'.join(row['symptoms'])
                writer.writerow(row)
        
        print(f"📄 Saved CSV: {filename}")
        return filename
    
    def get_statistics(self):
        """Generate dataset statistics."""
        stats = {
            "total_entries": len(self.entries),
            "categories": {},
            "severity_distribution": {"Low": 0, "Medium": 0, "High": 0},
            "vaccine_availability": {"Yes": 0, "No": 0, "Limited": 0, "Multiple": 0},
            "systems": {},
            "transmissions": {},
        }
        
        for entry in self.entries:
            # Category distribution
            cat = entry["category"]
            stats["categories"][cat] = stats["categories"].get(cat, 0) + 1
            
            # Severity
            sev = entry["severity"]
            if sev in stats["severity_distribution"]:
                stats["severity_distribution"][sev] += 1
            
            # Vaccine
            vac = entry["vaccine"]
            if vac in stats["vaccine_availability"]:
                stats["vaccine_availability"][vac] += 1
            
            # System
            sys = entry["system"]
            stats["systems"][sys] = stats["systems"].get(sys, 0) + 1
            
            # Transmission
            trans = entry["transmission"]
            stats["transmissions"][trans] = stats["transmissions"].get(trans, 0) + 1
        
        return stats


def main():
    """Main execution."""
    generator = MedicalDatasetGenerator()
    
    # Generate dataset
    generator.generate_dataset()
    
    # Save files
    json_file = generator.to_json(
        "c:\\Users\\Sevvanthi\\Desktop\\DISEASE PREDICTION\\medical_dataset.json"
    )
    csv_file = generator.to_csv(
        "c:\\Users\\Sevvanthi\\Desktop\\DISEASE PREDICTION\\medical_dataset_expanded.csv"
    )
    
    # Print statistics
    stats = generator.get_statistics()
    print("\n" + "="*60)
    print("📊 DATASET STATISTICS")
    print("="*60)
    print(f"\nTotal Entries: {stats['total_entries']:,}")
    print(f"\nCategory Distribution:")
    for cat, count in sorted(stats['categories'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / stats['total_entries']) * 100
        print(f"  • {cat}: {count:,} ({pct:.1f}%)")
    
    print(f"\nSeverity Distribution:")
    for sev, count in stats['severity_distribution'].items():
        pct = (count / stats['total_entries']) * 100
        print(f"  • {sev}: {count:,} ({pct:.1f}%)")
    
    print(f"\nVaccine Availability:")
    for status, count in stats['vaccine_availability'].items():
        pct = (count / stats['total_entries']) * 100
        print(f"  • {status}: {count:,} ({pct:.1f}%)")
    
    print(f"\nTop Affected Systems:")
    for sys, count in sorted(stats['systems'].items(), key=lambda x: x[1], reverse=True)[:5]:
        pct = (count / stats['total_entries']) * 100
        print(f"  • {sys}: {count:,} ({pct:.1f}%)")
    
    print(f"\nTransmission Types:")
    for trans, count in sorted(stats['transmissions'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / stats['total_entries']) * 100
        print(f"  • {trans}: {count:,} ({pct:.1f}%)")
    
    print("\n" + "="*60)
    print("✅ Dataset generation complete!")
    print(f"📁 JSON: {json_file}")
    print(f"📁 CSV: {csv_file}")
    print("="*60)


if __name__ == "__main__":
    main()
