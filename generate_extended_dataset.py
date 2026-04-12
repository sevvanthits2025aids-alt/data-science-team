import csv
import random
import json

# Base disease data with medical accuracy
BASE_DISEASES = {
    # ===== VIRUSES =====
    "Influenza": {
        "category": "Virus",
        "severity": "Medium",
        "base_symptoms": ["fever", "cough", "sore throat", "fatigue", "body aches", "headache"],
        "causes": ["Influenza virus infection", "Seasonal transmission", "Airborne droplets"]
    },
    "COVID-19": {
        "category": "Virus",
        "severity": "High",
        "base_symptoms": ["fever", "cough", "fatigue", "loss of taste/smell", "shortness of breath", "body aches"],
        "causes": ["SARS-CoV-2 virus", "Respiratory transmission", "Close contact"]
    },
    "Common Cold": {
        "category": "Virus",
        "severity": "Low",
        "base_symptoms": ["runny nose", "sore throat", "cough", "sneezing", "mild fever", "fatigue"],
        "causes": ["Rhinovirus infection", "Multiple viral strains", "Airborne or contact transmission"]
    },
    "HIV/AIDS": {
        "category": "Virus",
        "severity": "High",
        "base_symptoms": ["fever", "fatigue", "weight loss", "night sweats", "swollen lymph nodes", "persistent cough"],
        "causes": ["HIV virus infection", "Unprotected sex", "Shared needles", "Mother-to-child transmission"]
    },
    "Hepatitis B": {
        "category": "Virus",
        "severity": "High",
        "base_symptoms": ["fatigue", "jaundice", "abdominal pain", "nausea", "loss of appetite", "dark urine"],
        "causes": ["Hepatitis B virus", "Blood contact", "Sexual transmission", "Mother-to-child"]
    },
    "Hepatitis C": {
        "category": "Virus",
        "severity": "Medium",
        "base_symptoms": ["fatigue", "jaundice", "abdominal pain", "nausea", "loss of appetite", "joint pain"],
        "causes": ["Hepatitis C virus", "Blood contact", "Shared needles", "Healthcare exposure"]
    },
    "Ebola": {
        "category": "Virus",
        "severity": "High",
        "base_symptoms": ["fever", "severe headache", "muscle pain", "weakness", "diarrhea", "vomiting", "hemorrhage"],
        "causes": ["Ebola virus", "Contact with infected body fluids", "Animal transmission"]
    },
    "Zika Virus": {
        "category": "Virus",
        "severity": "Medium",
        "base_symptoms": ["fever", "rash", "joint pain", "conjunctivitis", "headache", "muscle pain"],
        "causes": ["Zika virus", "Mosquito transmission", "Sexual transmission"]
    },
    "Dengue": {
        "category": "Virus",
        "severity": "High",
        "base_symptoms": ["high fever", "severe headache", "pain behind eyes", "joint pain", "muscle pain", "rash", "bleeding"],
        "causes": ["Dengue virus", "Mosquito transmission", "Aedes mosquito bite"]
    },
    "Measles": {
        "category": "Virus",
        "severity": "High",
        "base_symptoms": ["fever", "cough", "runny nose", "red eyes", "rash", "white spots in mouth"],
        "causes": ["Measles virus", "Airborne transmission", "Unvaccinated exposure"]
    },
    "Chickenpox": {
        "category": "Virus",
        "severity": "Medium",
        "base_symptoms": ["fever", "fatigue", "loss of appetite", "rash", "blisters", "itching"],
        "causes": ["Varicella-zoster virus", "Airborne transmission", "Direct contact"]
    },
    "Mumps": {
        "category": "Virus",
        "severity": "Medium",
        "base_symptoms": ["fever", "headache", "muscle pain", "fatigue", "loss of appetite", "swollen salivary glands"],
        "causes": ["Mumps virus", "Airborne transmission", "Saliva contact"]
    },
    "Rubella": {
        "category": "Virus",
        "severity": "Medium",
        "base_symptoms": ["fever", "rash", "swollen lymph nodes", "joint pain", "headache", "runny nose"],
        "causes": ["Rubella virus", "Airborne transmission", "Congenital transmission"]
    },
    "Norovirus": {
        "category": "Virus",
        "severity": "Medium",
        "base_symptoms": ["nausea", "vomiting", "diarrhea", "stomach cramps", "fever", "headache"],
        "causes": ["Norovirus infection", "Contaminated food/water", "Person-to-person contact"]
    },
    "Rotavirus": {
        "category": "Virus",
        "severity": "High",
        "base_symptoms": ["severe diarrhea", "vomiting", "fever", "abdominal pain", "dehydration"],
        "causes": ["Rotavirus infection", "Fecal-oral transmission", "Contaminated surfaces"]
    },

    # ===== BACTERIA =====
    "Tuberculosis": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["persistent cough", "chest pain", "coughing blood", "fatigue", "weight loss", "fever", "night sweats"],
        "causes": ["Mycobacterium tuberculosis", "Airborne transmission", "Close contact with infected person"]
    },
    "Pneumonia": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["cough", "fever", "chills", "shortness of breath", "chest pain", "fatigue", "nausea"],
        "causes": ["Bacterial infection (Streptococcus, etc.)", "Viral infection", "Fungal infection", "Aspiration"]
    },
    "Strep Throat": {
        "category": "Bacteria",
        "severity": "Medium",
        "base_symptoms": ["sore throat", "fever", "swollen lymph nodes", "white patches on tonsils", "difficulty swallowing", "rash"],
        "causes": ["Streptococcus bacteria", "Direct contact", "Airborne droplets"]
    },
    "Urinary Tract Infection": {
        "category": "Bacteria",
        "severity": "Medium",
        "base_symptoms": ["frequent urination", "burning sensation", "cloudy urine", "strong urine odor", "pelvic pain", "fever"],
        "causes": ["E. coli bacteria", "Poor hygiene", "Sexual activity", "Catheter use"]
    },
    "Salmonella": {
        "category": "Bacteria",
        "severity": "Medium",
        "base_symptoms": ["diarrhea", "fever", "abdominal cramps", "nausea", "vomiting", "headache"],
        "causes": ["Salmonella bacteria", "Contaminated food", "Undercooked poultry/eggs", "Poor food handling"]
    },
    "E. coli Infection": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["severe diarrhea", "abdominal pain", "bloody diarrhea", "vomiting", "fever", "fatigue"],
        "causes": ["E. coli bacteria", "Contaminated food/water", "Undercooked meat", "Poor sanitation"]
    },
    "Chlamydia": {
        "category": "Bacteria",
        "severity": "Medium",
        "base_symptoms": ["painful urination", "abnormal discharge", "pelvic pain", "testicular pain", "rectal pain", "sore throat"],
        "causes": ["Chlamydia trachomatis", "Sexual transmission", "Mother-to-child during birth"]
    },
    "Gonorrhea": {
        "category": "Bacteria",
        "severity": "Medium",
        "base_symptoms": ["painful urination", "abnormal discharge", "pelvic pain", "testicular pain", "rectal pain", "sore throat"],
        "causes": ["Neisseria gonorrhoeae", "Sexual transmission", "Mother-to-child during birth"]
    },
    "Syphilis": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["chancre sore", "rash", "fever", "fatigue", "hair loss", "joint pain", "neurological symptoms"],
        "causes": ["Treponema pallidum", "Sexual transmission", "Congenital transmission"]
    },
    "Lyme Disease": {
        "category": "Bacteria",
        "severity": "Medium",
        "base_symptoms": ["bulls-eye rash", "fever", "headache", "fatigue", "joint pain", "muscle pain", "swollen lymph nodes"],
        "causes": ["Borrelia burgdorferi", "Tick bite", "Deer tick transmission"]
    },
    "Tetanus": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["muscle stiffness", "lockjaw", "difficulty swallowing", "muscle spasms", "fever", "sweating"],
        "causes": ["Clostridium tetani", "Wound contamination", "Soil exposure", "Rust exposure"]
    },
    "Pertussis": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["severe cough", "whooping sound", "vomiting after cough", "fever", "runny nose", "fatigue"],
        "causes": ["Bordetella pertussis", "Airborne transmission", "Close contact"]
    },
    "Leprosy": {
        "category": "Bacteria",
        "severity": "Medium",
        "base_symptoms": ["skin lesions", "numbness", "muscle weakness", "eye problems", "enlarged nerves", "chronic nasal congestion"],
        "causes": ["Mycobacterium leprae", "Prolonged close contact", "Armadillo transmission"]
    },
    "Anthrax": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["fever", "fatigue", "chest pain", "shortness of breath", "nausea", "vomiting", "skin ulcers"],
        "causes": ["Bacillus anthracis", "Contact with infected animals", "Biological weapon"]
    },
    "Botulism": {
        "category": "Bacteria",
        "severity": "High",
        "base_symptoms": ["double vision", "blurred vision", "drooping eyelids", "slurred speech", "difficulty swallowing", "muscle weakness"],
        "causes": ["Clostridium botulinum toxin", "Contaminated food", "Wound infection", "Infant intestinal infection"]
    },

    # ===== DISEASES =====
    "Diabetes Type 1": {
        "category": "Disease",
        "severity": "High",
        "base_symptoms": ["frequent urination", "increased thirst", "extreme hunger", "fatigue", "slow-healing sores", "frequent infections"],
        "causes": ["Autoimmune destruction of insulin-producing cells", "Genetic predisposition", "Environmental triggers"]
    },
    "Diabetes Type 2": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["frequent urination", "increased thirst", "increased hunger", "fatigue", "slow-healing sores", "frequent infections", "blurred vision"],
        "causes": ["Insulin resistance", "Genetic factors", "Obesity", "Sedentary lifestyle", "Poor diet"]
    },
    "Hypertension": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["headache", "dizziness", "blurred vision", "chest pain", "shortness of breath", "nosebleeds"],
        "causes": ["Genetic factors", "Obesity", "High salt intake", "Stress", "Lack of exercise", "Smoking"]
    },
    "Coronary Artery Disease": {
        "category": "Disease",
        "severity": "High",
        "base_symptoms": ["chest pain", "shortness of breath", "fatigue", "dizziness", "nausea", "sweating"],
        "causes": ["Atherosclerosis", "High cholesterol", "Hypertension", "Smoking", "Diabetes", "Family history"]
    },
    "Asthma": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["wheezing", "coughing", "shortness of breath", "chest tightness", "fatigue", "difficulty sleeping"],
        "causes": ["Genetic factors", "Allergens", "Air pollution", "Respiratory infections", "Exercise", "Stress"]
    },
    "Chronic Obstructive Pulmonary Disease": {
        "category": "Disease",
        "severity": "High",
        "base_symptoms": ["chronic cough", "shortness of breath", "wheezing", "chest tightness", "fatigue", "frequent respiratory infections"],
        "causes": ["Smoking", "Air pollution", "Genetic factors", "Occupational exposure", "Respiratory infections"]
    },
    "Alzheimer's Disease": {
        "category": "Disease",
        "severity": "High",
        "base_symptoms": ["memory loss", "confusion", "difficulty with familiar tasks", "mood changes", "difficulty with problem-solving", "disorientation"],
        "causes": ["Genetic factors", "Age", "Family history", "Cardiovascular disease", "Head trauma", "Lifestyle factors"]
    },
    "Parkinson's Disease": {
        "category": "Disease",
        "severity": "High",
        "base_symptoms": ["tremor", "stiffness", "bradykinesia", "postural instability", "difficulty walking", "speech changes"],
        "causes": ["Genetic factors", "Age", "Environmental toxins", "Head trauma", "Vascular disease"]
    },
    "Rheumatoid Arthritis": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["joint pain", "joint swelling", "joint stiffness", "fatigue", "fever", "weight loss"],
        "causes": ["Autoimmune disorder", "Genetic factors", "Environmental triggers", "Hormonal factors", "Infections"]
    },
    "Osteoarthritis": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["joint pain", "joint stiffness", "reduced range of motion", "joint swelling", "crepitus", "muscle weakness"],
        "causes": ["Age", "Joint injury", "Obesity", "Genetic factors", "Repetitive joint use"]
    },
    "Multiple Sclerosis": {
        "category": "Disease",
        "severity": "High",
        "base_symptoms": ["fatigue", "difficulty walking", "numbness", "weakness", "vision problems", "dizziness", "bladder problems"],
        "causes": ["Autoimmune disorder", "Genetic factors", "Environmental factors", "Vitamin D deficiency", "Smoking"]
    },
    "Epilepsy": {
        "category": "Disease",
        "severity": "High",
        "base_symptoms": ["seizures", "loss of consciousness", "convulsions", "confusion", "fatigue", "headache"],
        "causes": ["Genetic factors", "Brain injury", "Infections", "Stroke", "Brain tumors", "Developmental disorders"]
    },
    "Migraine": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["severe headache", "nausea", "vomiting", "sensitivity to light", "sensitivity to sound", "aura"],
        "causes": ["Genetic factors", "Hormonal changes", "Stress", "Certain foods", "Sleep changes", "Environmental factors"]
    },
    "Depression": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["persistent sadness", "loss of interest", "fatigue", "sleep changes", "appetite changes", "difficulty concentrating"],
        "causes": ["Genetic factors", "Brain chemistry", "Stress", "Trauma", "Medical conditions", "Substance abuse"]
    },
    "Anxiety Disorder": {
        "category": "Disease",
        "severity": "Medium",
        "base_symptoms": ["excessive worry", "restlessness", "fatigue", "difficulty concentrating", "irritability", "muscle tension"],
        "causes": ["Genetic factors", "Brain chemistry", "Stress", "Trauma", "Medical conditions", "Substance abuse"]
    },

    # ===== DISORDERS =====
    "Attention Deficit Hyperactivity Disorder": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["inattention", "hyperactivity", "impulsivity", "disorganization", "forgetfulness", "difficulty following instructions"],
        "causes": ["Genetic factors", "Brain structure differences", "Environmental factors", "Prenatal exposure to toxins", "Low birth weight"]
    },
    "Autism Spectrum Disorder": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["social communication difficulties", "repetitive behaviors", "sensory sensitivities", "restricted interests", "delayed language development"],
        "causes": ["Genetic factors", "Environmental factors", "Prenatal exposure", "Complications during pregnancy", "Advanced parental age"]
    },
    "Bipolar Disorder": {
        "category": "Disorder",
        "severity": "High",
        "base_symptoms": ["mood swings", "mania", "depression", "irritability", "impulsivity", "sleep disturbances"],
        "causes": ["Genetic factors", "Brain chemistry", "Stress", "Trauma", "Substance abuse", "Medical conditions"]
    },
    "Schizophrenia": {
        "category": "Disorder",
        "severity": "High",
        "base_symptoms": ["hallucinations", "delusions", "disorganized thinking", "negative symptoms", "cognitive difficulties", "emotional flatness"],
        "causes": ["Genetic factors", "Brain chemistry", "Brain structure", "Stress", "Drug use", "Prenatal complications"]
    },
    "Obsessive-Compulsive Disorder": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["obsessions", "compulsions", "anxiety", "time-consuming rituals", "interference with daily life", "distress"],
        "causes": ["Genetic factors", "Brain chemistry", "Learning experiences", "Stress", "Trauma", "Infections"]
    },
    "Post-Traumatic Stress Disorder": {
        "category": "Disorder",
        "severity": "High",
        "base_symptoms": ["flashbacks", "nightmares", "avoidance", "hypervigilance", "emotional numbness", "irritability"],
        "causes": ["Traumatic events", "Severe stress", "Genetic factors", "Brain chemistry changes", "Lack of social support"]
    },
    "Eating Disorders": {
        "category": "Disorder",
        "severity": "High",
        "base_symptoms": ["restrictive eating", "binge eating", "purging", "body image distortion", "fear of gaining weight", "obsession with food"],
        "causes": ["Genetic factors", "Psychological factors", "Cultural pressures", "Trauma", "Low self-esteem", "Perfectionism"]
    },
    "Sleep Apnea": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["loud snoring", "daytime sleepiness", "morning headaches", "irritability", "difficulty concentrating", "dry mouth"],
        "causes": ["Obesity", "Neck anatomy", "Age", "Family history", "Smoking", "Alcohol use"]
    },
    "Fibromyalgia": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["widespread pain", "fatigue", "sleep disturbances", "cognitive difficulties", "headaches", "irritable bowel syndrome"],
        "causes": ["Genetic factors", "Infections", "Physical trauma", "Stress", "Abnormal pain processing", "Hormonal changes"]
    },
    "Chronic Fatigue Syndrome": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["severe fatigue", "post-exertional malaise", "sleep problems", "pain", "cognitive issues", "sore throat"],
        "causes": ["Viral infections", "Immune system issues", "Hormonal imbalances", "Stress", "Genetic factors"]
    },
    "Irritable Bowel Syndrome": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["abdominal pain", "bloating", "gas", "diarrhea", "constipation", "mucus in stool"],
        "causes": ["Gut-brain axis dysfunction", "Infections", "Food intolerances", "Stress", "Genetic factors", "Gut microbiota changes"]
    },
    "Restless Legs Syndrome": {
        "category": "Disorder",
        "severity": "Low",
        "base_symptoms": ["urge to move legs", "uncomfortable sensations", "worse at night", "sleep disturbances", "daytime fatigue", "difficulty concentrating"],
        "causes": ["Genetic factors", "Iron deficiency", "Pregnancy", "Chronic diseases", "Medications", "Caffeine"]
    },
    "Tourette Syndrome": {
        "category": "Disorder",
        "severity": "Medium",
        "base_symptoms": ["motor tics", "vocal tics", "involuntary movements", "involuntary sounds", "obsessive behaviors", "attention difficulties"],
        "causes": ["Genetic factors", "Brain chemistry", "Environmental factors", "Complications during pregnancy", "Infections"]
    },
    "Dyslexia": {
        "category": "Disorder",
        "severity": "Low",
        "base_symptoms": ["reading difficulties", "spelling problems", "letter reversal", "slow reading speed", "poor comprehension", "phonological awareness issues"],
        "causes": ["Genetic factors", "Brain structure differences", "Prenatal exposure", "Early childhood experiences"]
    },
    "Dyscalculia": {
        "category": "Disorder",
        "severity": "Low",
        "base_symptoms": ["math difficulties", "number sense problems", "calculation errors", "difficulty understanding math concepts", "poor spatial reasoning", "memory issues with numbers"],
        "causes": ["Genetic factors", "Brain structure differences", "Prenatal exposure", "Learning experiences", "Neurological factors"]
    },
    "Sickle Cell Anemia": {
        "category": "Disorder",
        "severity": "High",
        "base_symptoms": ["pain crises", "fatigue", "shortness of breath", "delayed growth", "frequent infections", "jaundice"],
        "causes": ["Genetic mutation", "Inherited from both parents", "African ancestry", "Mediterranean ancestry"]
    }
}

# Additional symptoms to create variations
ADDITIONAL_SYMPTOMS = [
    "nausea", "vomiting", "dizziness", "weakness", "chills", "sweating", "loss of appetite",
    "weight loss", "weight gain", "insomnia", "sleepiness", "anxiety", "depression",
    "irritability", "confusion", "memory problems", "difficulty concentrating",
    "muscle weakness", "joint swelling", "skin rash", "itching", "hair loss",
    "vision changes", "hearing loss", "tinnitus", "nosebleeds", "bruising easily",
    "frequent urination", "painful urination", "blood in urine", "constipation",
    "heart palpitations", "irregular heartbeat", "swelling in legs", "coughing up blood",
    "difficulty swallowing", "hoarseness", "bad breath", "tooth pain", "jaw pain",
    "neck pain", "back pain", "abdominal pain", "chest pain", "arm pain", "leg pain",
    "headache", "migraine", "fever", "night sweats", "cold sweats", "hot flashes",
    "tremors", "seizures", "numbness", "tingling", "burning sensation", "sensitivity to touch",
    "light sensitivity", "sound sensitivity", "smell changes", "taste changes",
    "dry mouth", "excessive thirst", "frequent thirst", "dehydration", "edema",
    "lymphedema", "ascites", "pleural effusion", "pericardial effusion", "anemia",
    "easy bruising", "bleeding gums", "petechiae", "purpura", "thrombosis",
    "phlebitis", "varicose veins", "hemorrhoids", "rectal bleeding", "hematemesis",
    "melena", "hemoptysis", "epistaxis", "menorrhagia", "metrorrhagia",
    "amenorrhea", "dysmenorrhea", "infertility", "erectile dysfunction",
    "loss of libido", "gynecomastia", "hirsutism", "acne", "psoriasis", "eczema",
    "dermatitis", "cellulitis", "abscess", "ulcer", "gangrene", "necrosis",
    "osteoporosis", "arthritis", "gout", "bursitis", "tendinitis", "sprains",
    "strains", "fractures", "dislocations", "hernias", "hydrocele", "varicocele",
    "prostatitis", "cystitis", "pyelonephritis", "glomerulonephritis", "nephrotic syndrome",
    "acute renal failure", "chronic renal failure", "uremia", "dialysis", "transplant",
    "hepatitis", "cirrhosis", "ascites", "varices", "encephalopathy", "jaundice",
    "gallstones", "cholecystitis", "pancreatitis", "diabetes", "hypoglycemia",
    "hyperglycemia", "thyroid problems", "goiter", "hyperthyroidism", "hypothyroidism",
    "adrenal insufficiency", "cushing syndrome", "pituitary disorders", "growth hormone deficiency",
    "acromegaly", "diabetes insipidus", "SIADH", "electrolyte imbalances",
    "acid-base disorders", "respiratory acidosis", "respiratory alkalosis",
    "metabolic acidosis", "metabolic alkalosis", "shock", "sepsis", "DIC",
    "thrombocytopenia", "thrombocytosis", "leukopenia", "leukocytosis", "anemia",
    "polycythemia", "thalassemia", "hemophilia", "von willebrand disease",
    "immune deficiency", "autoimmune diseases", "allergies", "asthma", "COPD",
    "pneumonia", "bronchitis", "emphysema", "pleurisy", "pneumothorax",
    "hemothorax", "atelectasis", "ARDS", "pulmonary embolism", "deep vein thrombosis",
    "stroke", "TIA", "aneurysm", "AVM", "hydrocephalus", "meningitis", "encephalitis",
    "brain abscess", "epilepsy", "parkinsonism", "alzheimer disease", "dementia",
    "delirium", "coma", "brain death", "spinal cord injury", "peripheral neuropathy",
    "myasthenia gravis", "guillain-barre syndrome", "multiple sclerosis", "ALS",
    "muscular dystrophy", "myopathy", "rhabdomyolysis", "compartment syndrome",
    "tendon rupture", "ligament tear", "meniscus tear", "rotator cuff tear",
    "ACL tear", "MCL tear", "PCL tear", "LCL tear", "Achilles tendon rupture",
    "plantar fasciitis", "shin splints", "stress fractures", "avascular necrosis",
    "osteomyelitis", "septic arthritis", "rheumatic fever", "endocarditis",
    "pericarditis", "myocarditis", "cardiomyopathy", "congenital heart disease",
    "valvular heart disease", "arrhythmias", "heart block", "bundle branch block",
    "WPW syndrome", "long QT syndrome", "brugada syndrome", "hypertrophic cardiomyopathy",
    "dilated cardiomyopathy", "restrictive cardiomyopathy", "takotsubo cardiomyopathy",
    "peripheral artery disease", "Buerger disease", "Raynaud phenomenon",
    "venous insufficiency", "lymphedema", "elephantiasis", "filariasis",
    "schistosomiasis", "malaria", "trypanosomiasis", "leishmaniasis", "toxoplasmosis",
    "cryptosporidiosis", "giardiasis", "amebiasis", "ascariasis", "hookworm",
    "strongyloidiasis", "trichuriasis", "enterobiasis", "taeniasis", "cysticercosis",
    "echinococcosis", "fascioliasis", "opisthorchiasis", "clonorchiasis",
    " paragonimiasis", "schistosomiasis", "fasciolopsiasis", "metagonimiasis",
    "heterophyiasis", "echinostomiasis", "angiostrongyliasis", "gnathostomiasis",
    "sparganosis", "diphyllobothriasis", "hymenolepiasis", "dipylidiasis",
    "mesocestoidosis", "anoplocephaliasis", "moniezia", "thysanosoma",
    "avitelina", "raillietina", "inermicapsifer", "bertiella", "andrya",
    "linstowia", "skrjabinia", "stilesia", "thysaniezia", "citotaenia",
    "choanotaenia", "davainea", "raillietina", "hymenolepis", "echinococcus",
    "taenia", "diphyllobothrium", "spirometra", "multiceps", "granulosus",
    "alveococcus", "oligarthrus", "macracanthorhynchus", "moniliformis",
    "gigantorhynchus", "prosthenorchis", "oncicola", "macracanthorhynchus",
    "moniliformis", "gigantorhynchus", "prosthenorchis", "oncicola"
]

def generate_symptom_variations(base_symptoms, num_variations=50):
    """Generate multiple symptom combinations for a disease"""
    variations = []
    base_count = len(base_symptoms)

    for i in range(num_variations):
        # Start with base symptoms
        symptoms = base_symptoms.copy()

        # Add 1-3 additional symptoms randomly
        num_additional = random.randint(1, 3)
        additional = random.sample(ADDITIONAL_SYMPTOMS, num_additional)
        symptoms.extend(additional)

        # Remove 0-2 symptoms randomly to create variation
        if len(symptoms) > base_count:
            num_remove = random.randint(0, min(2, len(symptoms) - base_count))
            if num_remove > 0:
                symptoms = random.sample(symptoms, len(symptoms) - num_remove)

        # Shuffle and deduplicate
        symptoms = list(set(symptoms))
        random.shuffle(symptoms)

        variations.append(symptoms)

    return variations

def generate_dataset():
    """Generate the complete dataset with 15,000+ entries"""
    dataset = []
    target_entries = 15000
    diseases_list = list(BASE_DISEASES.keys())

    # Calculate entries per disease to reach target
    entries_per_disease = target_entries // len(diseases_list)
    remaining_entries = target_entries % len(diseases_list)

    print(f"Generating dataset with {len(diseases_list)} diseases...")
    print(f"Target: {target_entries} entries")
    print(f"Entries per disease: {entries_per_disease}")

    for disease_name in diseases_list:
        disease_info = BASE_DISEASES[disease_name]
        base_symptoms = disease_info["base_symptoms"]

        # Generate variations
        num_variations = entries_per_disease
        if remaining_entries > 0:
            num_variations += 1
            remaining_entries -= 1

        symptom_variations = generate_symptom_variations(base_symptoms, num_variations)

        for symptoms in symptom_variations:
            entry = {
                "Disease Name": disease_name,
                "Category": disease_info["category"],
                "Symptoms": "; ".join(symptoms),
                "Severity": disease_info["severity"],
                "Causes": "; ".join(disease_info["causes"])
            }
            dataset.append(entry)

    # Shuffle the dataset
    random.shuffle(dataset)

    print(f"Generated {len(dataset)} entries")
    return dataset

def save_to_csv(dataset, filename="extended_medical_dataset.csv"):
    """Save dataset to CSV file"""
    if not dataset:
        print("No data to save!")
        return

    fieldnames = ["Disease Name", "Category", "Symptoms", "Severity", "Causes"]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)

    print(f"Dataset saved to {filename}")
    print(f"Total entries: {len(dataset)}")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)

    # Generate dataset
    dataset = generate_dataset()

    # Save to CSV
    save_to_csv(dataset)