import csv
import re
from collections import Counter
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash

DATA_FILE = Path("data.csv")
FALLBACK_DATA_FILE = Path("Healthcare.csv")
HISTORY_FILE = Path("History.csv")
USERS_FILE = Path("users.csv")

HISTORY_HEADER = ["username", "symptoms", "predicted_disease", "confidence", "risk_level", "timestamp"]
USER_HEADER = ["username", "password_hash"]


def ensure_users_file() -> None:
    if users_file_missing():
        with USERS_FILE.open("w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(USER_HEADER)
            writer.writerow(["admin", generate_password_hash("admin123")])

    # Ensure the default demo user exists for easy access
    existing_users = []
    with USERS_FILE.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        existing_users = [row["username"] for row in reader if row.get("username")]

    if "sevvanthi" not in existing_users:
        with USERS_FILE.open("a", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["sevvanthi", generate_password_hash("ts@08")])


def users_file_missing() -> bool:
    return not USERS_FILE.exists() or USERS_FILE.stat().st_size == 0


def load_users() -> Dict[str, str]:
    ensure_users_file()
    with USERS_FILE.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return {row["username"]: row["password_hash"] for row in reader if row.get("username")}


def save_user(username: str, password_hash: str) -> None:
    ensure_users_file()
    with USERS_FILE.open("a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, password_hash])


def update_password(username: str, new_password_hash: str) -> None:
    ensure_users_file()
    rows = []
    with USERS_FILE.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader if row.get("username")]

    with USERS_FILE.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(USER_HEADER)
        for row in rows:
            if row["username"] == username:
                writer.writerow([username, new_password_hash])
            else:
                writer.writerow([row["username"], row["password_hash"]])


def load_data() -> pd.DataFrame:
    file_path = DATA_FILE if DATA_FILE.exists() else FALLBACK_DATA_FILE
    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found. Please add '{DATA_FILE.name}' or '{FALLBACK_DATA_FILE.name}' in the project folder."
        )

    df = pd.read_csv(file_path)
    clean_rows = []
    symptom_columns = [col for col in df.columns if col.lower().startswith("symptom")]

    for _, row in df.iterrows():
        row_data = row.to_dict()
        disease = str(row_data.get("disease", row_data.get("Disease", "Unknown"))).strip()
        symptoms: List[str] = []

        if "Symptoms" in row_data and pd.notna(row_data["Symptoms"]):
            symptoms_text = str(row_data["Symptoms"])
            symptoms += split_symptom_text(symptoms_text)

        for col in symptom_columns:
            value = row_data.get(col, None)
            if pd.notna(value):
                symptoms.append(str(value))

        if not symptoms:
            for value in row_data.values():
                if isinstance(value, str) and "," in value and "disease" not in str(value).lower():
                    symptoms += split_symptom_text(value)
                    break

        normalized_symptoms = [
            normalize_symptom_with_synonyms(sym, SYMPTOM_SYNONYMS)
            for sym in symptoms
            if normalize_symptom_with_synonyms(sym, SYMPTOM_SYNONYMS)
        ]
        clean_rows.append({"disease": disease, "symptoms": sorted(set(normalized_symptoms))})

    return pd.DataFrame(clean_rows)


def split_symptom_text(text: str) -> List[str]:
    text = str(text).strip()
    tokens = re.split(r"[,;+\\n]+", text)
    return [normalize_symptom_with_synonyms(token, SYMPTOM_SYNONYMS) for token in tokens if normalize_symptom_with_synonyms(token, SYMPTOM_SYNONYMS)]


def normalize_symptom(symptom: str) -> str:
    return " ".join(str(symptom).strip().lower().split())


def clean_input(user_input: str) -> List[str]:
    """Clean and parse user input for symptom extraction with improved accuracy."""
    if not user_input or not user_input.strip():
        return []

    # Convert to lowercase and trim
    cleaned = user_input.lower().strip()
    
    # Replace common separators with commas
    cleaned = re.sub(r"[\+\/\\\\;]", ",", cleaned)
    
    # Remove unnecessary words
    stop_words = r"\b(i have|i've|i am|i'm|i\s+feel|and|with|plus|also|my|the|a|an|please|kind of|kindoff|just|very|extremely|slightly|somewhat|severe|moderate|mild|sometimes|occasionally)\b"
    cleaned = re.sub(stop_words, " ", cleaned)
    
    # Remove special characters but keep spaces and commas
    cleaned = re.sub(r"[^a-z0-9,\s]", " ", cleaned)
    
    # Normalize whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    
    # Split by comma and clean individually
    symptoms_raw = cleaned.split(",")
    symptoms: List[str] = []
    
    for symptom in symptoms_raw:
        normalized = normalize_symptom_with_synonyms(symptom, SYMPTOM_SYNONYMS)
        if normalized and len(normalized) > 1:  # Skip single letter or empty
            symptoms.append(normalized)
    
    # Remove duplicates while preserving order
    seen = set()
    final_symptoms = []
    for symptom in symptoms:
        if symptom not in seen:
            seen.add(symptom)
            final_symptoms.append(symptom)
    
    return sorted(set(final_symptoms))


CRITICAL_SYMPTOMS = {"fever": 2, "bleeding": 2, "breathlessness": 2, "shortness of breath": 2, "chest pain": 2, "seizure": 2}

# Symptom synonyms and aliases for better matching
SYMPTOM_SYNONYMS = {
    "fever": {"high temperature", "high body temperature", "temperature", "hot", "99.5 f", "100 f", "elevated temp"},
    "cough": {"coughing", "dry cough", "persistent cough"},
    "sore throat": {"throat pain", "throat irritation", "scratchy throat"},
    "headache": {"head pain", "migraine", "headaches"},
    "muscle body aches": {"muscle ache", "body ache", "aches", "muscle pain", "body pain"},
    "fatigue or weakness": {"fatigue", "weakness", "tired", "tiredness", "weak"},
    "diarrhea": {"diarrhoea", "loose motion"},
    "vomiting": {"vomit", "nausea and vomit"},
    "weight loss": {"lose weight", "weight reduction"},
    "back pain": {"backache", "lower back pain"},
    "shortness of breath": {"breathlessness", "difficulty breathing", "hard to breathe", "cant breathe"},
    "chest pain": {"chest discomfort", "pain in chest"},
    "anxiety": {"anxious", "panic"},
    "depression": {"depressed", "sad"},
    "dizziness": {"dizzy", "vertigo", "lightheaded"},
    "nausea": {"feeling sick", "queasy"},
    "appetite loss": {"loss of appetite", "no appetite", "dont want to eat"},
    "swelling": {"swollen", "edema"},
    "rash": {"skin rash", "eruption"},
}


def normalize_symptom_with_synonyms(symptom: str, symptom_synonyms: dict) -> str:
    """Convert symptom to canonical form using synonym mapping."""
    normalized = normalize_symptom(symptom)
    
    # Check if this symptom is a canonical form
    if normalized in symptom_synonyms:
        return normalized
    
    # Check if this symptom is a synonym
    for canonical, synonyms in symptom_synonyms.items():
        if normalized in synonyms:
            return canonical
    
    return normalized


def calculate_disease_score(user_symptoms: List[str], disease_symptoms: set, critical_symptom_weights: dict) -> int:
    """Calculate weighted confidence score for disease matching."""
    regular_matches = len(set(user_symptoms) & disease_symptoms)
    
    # Weight critical symptoms higher
    weighted_score = 0
    for symptom in user_symptoms:
        if symptom in disease_symptoms:
            weight = critical_symptom_weights.get(symptom, 1)
            weighted_score += weight
    
    return weighted_score


def predict_disease(user_symptoms: List[str], data: pd.DataFrame) -> Tuple[List[Tuple[str, int, List[str]]], str]:
    """Return top 3 diseases with their match percentages."""
    if not user_symptoms:
        return [], "No symptoms provided"

    disease_scores: Dict[str, Tuple[int, List[str], set]] = {}
    user_set = set(user_symptoms)

    for _, row in data.iterrows():
        disease = row["disease"]
        row_symptoms = set(row["symptoms"])
        if not row_symptoms:
            continue

        # Calculate weighted score
        weighted_score = calculate_disease_score(user_symptoms, row_symptoms, CRITICAL_SYMPTOMS)
        
        # Calculate traditional confidence percentage
        match_count = len(user_set & row_symptoms)
        confidence = round((match_count / len(row_symptoms)) * 100) if len(row_symptoms) > 0 else 0
        
        # Store with weighted score for ranking
        if disease not in disease_scores or weighted_score > disease_scores[disease][0]:
            matched_symptoms = sorted(user_set & row_symptoms)
            disease_scores[disease] = (weighted_score, matched_symptoms, confidence)

    # Sort by weighted score and get top 3
    sorted_diseases = sorted(
        disease_scores.items(),
        key=lambda x: (x[1][0], x[1][2]),
        reverse=True
    )[:3]

    # Format results as list of tuples: (disease_name, confidence%, matched_symptoms)
    results = [
        (disease, disease_scores[disease][2], disease_scores[disease][1])
        for disease, _ in sorted_diseases
    ]

    return results, ""


def choose_advice(disease: str) -> str:
    advice_map = {
        "flu": "Rest, drink fluids, and monitor your temperature. Contact a doctor if symptoms worsen.",
        "covid-19": "Self-isolate, stay hydrated, and get a medical test if breathing becomes difficult.",
        "heart disease": "Seek medical advice promptly and avoid heavy physical strain.",
        "bronchitis": "Rest, avoid smoke, and use warm fluids to ease breathing.",
        "diabetes": "Maintain a healthy diet and consult your physician for a tailored plan.",
        "arthritis": "Gentle exercise and pain management can help. Check with a doctor for care.",
        "stroke": "Seek emergency medical care immediately if symptoms are severe.",
    }
    return advice_map.get(disease.lower(), "Take rest, drink fluids, and consult a doctor if symptoms worsen.")


def save_history(username: str, symptoms: List[str], disease: str, confidence: int, risk_level: str) -> None:
    ensure_history_file()
    with HISTORY_FILE.open("a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            username,
            ", ".join(symptoms),
            disease,
            f"{confidence}%",
            risk_level,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ])


def ensure_history_file() -> None:
    if not HISTORY_FILE.exists() or HISTORY_FILE.stat().st_size == 0:
        with HISTORY_FILE.open("w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(HISTORY_HEADER)


def load_history_records(username: Optional[str] = None) -> List[Dict[str, str]]:
    if not HISTORY_FILE.exists() or HISTORY_FILE.stat().st_size == 0:
        return []

    with HISTORY_FILE.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        records = []
        for row in reader:
            if not row.get("username"):
                continue
            if username and row.get("username") != username:
                continue
            records.append({
                "username": row.get("username", ""),
                "symptoms": row.get("symptoms", ""),
                "predicted_disease": row.get("predicted_disease", ""),
                "confidence": row.get("confidence", ""),
                "risk_level": row.get("risk_level", ""),
                "timestamp": row.get("timestamp", ""),
            })
    return records


def get_metrics(username: Optional[str] = None) -> Dict[str, Any]:
    records = load_history_records(username)
    total_predictions = len(records)
    recent_disease = records[-1]["predicted_disease"] if records else "None"
    health_status = "Stable" if total_predictions == 0 else "Monitoring"
    return {
        "total_predictions": total_predictions,
        "recent_disease": recent_disease,
        "health_status": health_status,
    }


def get_analytics_data(records: List[Dict[str, str]]) -> Dict[str, Any]:
    disease_counts = Counter([record["predicted_disease"] or "Unknown" for record in records])
    risk_counts = Counter([record["risk_level"] or "Low" for record in records])
    trend_counts = Counter([record["timestamp"][:10] for record in records if record.get("timestamp")])

    trend_labels = sorted(trend_counts.keys())
    trend_values = [trend_counts[label] for label in trend_labels]

    return {
        "disease_labels": list(disease_counts.keys())[:8],
        "disease_values": list(disease_counts.values())[:8],
        "risk_labels": ["Low", "Medium", "High"],
        "risk_values": [risk_counts.get("Low", 0), risk_counts.get("Medium", 0), risk_counts.get("High", 0)],
        "trend_labels": trend_labels,
        "trend_values": trend_values,
    }


def get_risk_level(confidence: int) -> str:
    if confidence >= 75:
        return "High"
    if confidence >= 50:
        return "Medium"
    return "Low"
