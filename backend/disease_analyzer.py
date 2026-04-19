"""
Enhanced Medical Symptom Analysis Assistant
Predicts diseases based on symptom patterns with real-world medical correlations.
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import math


class DiseaseCategory(Enum):
    """Disease categories for organization."""
    VIRAL = "Viral"
    BACTERIAL = "Bacterial"
    VECTOR_BORNE = "Vector-Borne"
    RESPIRATORY = "Respiratory"
    DIGESTIVE = "Digestive"
    CHRONIC = "Chronic"
    CARDIOVASCULAR = "Cardiovascular"
    NEUROLOGICAL = "Neurological"
    ENDOCRINE = "Endocrine"
    INFECTIOUS = "Infectious"


@dataclass
class Disease:
    """Disease definition with medical characteristics."""
    name: str
    category: DiseaseCategory
    primary_symptoms: List[str]  # Most common/important symptoms
    secondary_symptoms: List[str]  # Less common but supporting symptoms
    tertiary_symptoms: List[str] = field(default_factory=list)  # Rare but specific symptoms
    prevalence_score: int = 0  # 1-10, higher = more common
    severity: str = "Unknown"  # 'Mild', 'Moderate', 'Severe', 'Critical'
    incubation_period: str = ""  # Typical time from exposure to symptoms
    contagious_period: str = ""  # How long person is contagious
    medical_reasoning: str = ""  # Why these symptoms correlate
    recommendations: str = ""  # What to do
    differential_diagnosis: List[str] = field(default_factory=list)  # Diseases to rule out
    risk_factors: List[str] = field(default_factory=list)  # Who is most at risk


# Comprehensive disease-symptom database with real medical correlations
DISEASE_DATABASE: Dict[str, Disease] = {
    # VIRAL INFECTIONS
    "influenza": Disease(
        name="Influenza (Flu)",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=["fever", "cough", "sore throat", "headache", "muscle body aches", "fatigue or weakness"],
        secondary_symptoms=["chills", "runny nose", "shortness of breath", "nausea", "diarrhea"],
        tertiary_symptoms=["loss of appetite", "sweating", "chest discomfort"],
        prevalence_score=9,
        severity="Moderate",
        incubation_period="1-4 days",
        contagious_period="1 day before symptoms to 5-7 days after",
        medical_reasoning="Influenza virus attacks respiratory tract causing sudden onset fever with systemic muscle aches, headache, and respiratory symptoms. The combination of fever + cough + muscle aches is classic.",
        recommendations="Get flu test, antivirals if early, rest, hydration. See doctor if breathing difficulty develops.",
        differential_diagnosis=["COVID-19", "common cold", "bacterial pneumonia"],
        risk_factors=["Elderly", "pregnant women", "immunocompromised", "healthcare workers"],
    ),
    
    "covid-19": Disease(
        name="COVID-19",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=["fever", "cough", "shortness of breath", "fatigue or weakness", "loss of taste/smell"],
        secondary_symptoms=["headache", "sore throat", "muscle body aches", "nausea", "diarrhea", "chills"],
        prevalence_score=6,
        severity="Moderate-Severe",
        medical_reasoning="COVID-19 presents with similar flu-like symptoms but more prominent respiratory involvement and distinctive loss of taste/smell. More unpredictable progression than flu.",
        recommendations="Get COVID-19 test immediately. Self-isolate. Contact doctor if O2 saturation drops or breathing severely difficult.",
    ),
    
    "common cold": Disease(
        name="Common Cold",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=["runny nose", "sore throat", "cough", "headache"],
        secondary_symptoms=["sneezing", "fatigue or weakness", "mild fever", "nausea"],
        prevalence_score=10,
        severity="Mild",
        medical_reasoning="Most common viral infection. Presents with mild upper respiratory symptoms. Fever is usually absent or mild.",
        recommendations="Supportive care: rest, fluids, zinc lozenges within 24 hours. Symptomatic relief with OTC medications.",
    ),
    
    "dengue": Disease(
        name="Dengue",
        category=DiseaseCategory.VECTOR_BORNE,
        primary_symptoms=["fever", "headache", "muscle body aches", "joint pain", "rash"],
        secondary_symptoms=["nausea", "vomiting", "eye pain", "fatigue or weakness", "diarrhea"],
        prevalence_score=7,
        severity="Moderate-Severe",
        medical_reasoning="Dengue from mosquito bite causes sudden high fever with severe joint/muscle pain (breakbone fever) and characteristic rash after 3-5 days.",
        recommendations="Seek medical care for testing. Monitor for hemorrhagic signs. No specific treatment; supportive care essential.",
    ),
    
    "malaria": Disease(
        name="Malaria",
        category=DiseaseCategory.VECTOR_BORNE,
        primary_symptoms=["fever", "chills", "headache", "muscle body aches", "fatigue or weakness"],
        secondary_symptoms=["nausea", "vomiting", "diarrhea", "sweating", "shortness of breath"],
        prevalence_score=5,
        severity="Moderate-Severe",
        medical_reasoning="Malaria from mosquito bite causes cyclical high fever (often 104°F+) with rigors/chills, body aches, and can rapidly progress to severe illness.",
        recommendations="Get blood test immediately for parasites. Early treatment critical. Seek emergency care if confusion or difficulty breathing.",
    ),
    
    # BACTERIAL INFECTIONS
    "typhoid": Disease(
        name="Typhoid (Enteric Fever)",
        category=DiseaseCategory.BACTERIAL,
        primary_symptoms=["fever", "headache", "muscle body aches", "weakness", "abdominal pain"],
        secondary_symptoms=["rash (rose spots)", "diarrhea", "spleen enlargement", "constipation", "delirium"],
        prevalence_score=4,
        severity="Severe",
        medical_reasoning="Typhoid from contaminated water/food. Presents with rising fever, sustained high fever (104-105°F), headache, and GI symptoms. Rose-colored rash classic.",
        recommendations="Urgent medical evaluation. Blood culture test needed. Antibiotics essential. Hospitalization often required.",
    ),
    
    "bacterial pneumonia": Disease(
        name="Bacterial Pneumonia",
        category=DiseaseCategory.RESPIRATORY,
        primary_symptoms=["fever", "cough", "shortness of breath", "chest pain", "fatigue or weakness"],
        secondary_symptoms=["yellow/green sputum", "chills", "muscle body aches", "headache", "nausea"],
        prevalence_score=6,
        severity="Severe",
        medical_reasoning="Bacterial infection of lung tissue causes fever, productive cough, breathing difficulty, and chest pain from pleural inflammation.",
        recommendations="Get chest X-ray. Blood cultures needed. Antibiotics required. Hospitalization may be needed based on severity.",
    ),
    
    "strep throat": Disease(
        name="Streptococcal Pharyngitis (Strep Throat)",
        category=DiseaseCategory.BACTERIAL,
        primary_symptoms=["sore throat", "fever", "headache", "nausea"],
        secondary_symptoms=["swollen tonsils", "white spots on throat", "rash", "body aches"],
        prevalence_score=7,
        severity="Mild-Moderate",
        medical_reasoning="Group A Streptococcus causes sudden severe sore throat, fever, and white exudate on tonsils. Rapid test distinguishes from viral.",
        recommendations="Get rapid strep test or throat culture. Antibiotics if positive. Pain relief with throat lozenges and warm salt water.",
    ),
    
    # RESPIRATORY CONDITIONS
    "bronchitis": Disease(
        name="Bronchitis",
        category=DiseaseCategory.RESPIRATORY,
        primary_symptoms=["cough", "shortness of breath", "chest discomfort"],
        secondary_symptoms=["fever", "fatigue or weakness", "sore throat", "headache", "phlegm"],
        prevalence_score=7,
        severity="Mild-Moderate",
        medical_reasoning="Inflammation of airways causes persistent cough (dry or productive), shortness of breath, and chest tightness without pneumonia.",
        recommendations="Rest, fluids, cough medicine, avoid smoke/irritants. See doctor if fever worsens or lasts >10 days.",
    ),
    
    "asthma": Disease(
        name="Asthma",
        category=DiseaseCategory.RESPIRATORY,
        primary_symptoms=["shortness of breath", "chest pain", "cough"],
        secondary_symptoms=["wheezing", "tight chest", "difficulty exercising", "fatigue"],
        prevalence_score=6,
        severity="Mild-Severe",
        medical_reasoning="Chronic airway inflammation causes reversible airflow obstruction, presenting with wheezing, cough, and breathing difficulty.",
        recommendations="Use rescue inhaler. Seek emergency care if severe attack. Chest X-ray and spirometry tests recommended.",
    ),
    
    # DIGESTIVE CONDITIONS
    "food poisoning": Disease(
        name="Food Poisoning",
        category=DiseaseCategory.DIGESTIVE,
        primary_symptoms=["nausea", "vomiting", "diarrhea", "abdominal pain"],
        secondary_symptoms=["fever", "headache", "muscle body aches", "fatigue or weakness"],
        prevalence_score=7,
        severity="Mild-Moderate",
        medical_reasoning="Bacterial/viral toxins cause acute GI symptoms with sudden onset usually 1-72 hours after contaminated food ingestion.",
        recommendations="Hydration paramount (oral rehydration salts). Rest. Avoid solid food initially. Seek care if symptoms persist >3 days.",
    ),
    
    "gastroenteritis": Disease(
        name="Gastroenteritis (Stomach Flu)",
        category=DiseaseCategory.DIGESTIVE,
        primary_symptoms=["diarrhea", "vomiting", "abdominal pain", "nausea"],
        secondary_symptoms=["fever", "headache", "muscle body aches", "fatigue or weakness"],
        prevalence_score=8,
        severity="Mild-Moderate",
        medical_reasoning="Viral or bacterial gut inflammation causes diarrhea, vomiting, and stomach pain. Often follows upper respiratory illness.",
        recommendations="Electrolyte replacement critical. Rest. Avoid dairy/fatty foods. Most resolve in 1-3 days.",
    ),
    
    # CHRONIC CONDITIONS
    "diabetes": Disease(
        name="Type 2 Diabetes",
        category=DiseaseCategory.CHRONIC,
        primary_symptoms=["increased thirst", "frequent urination", "fatigue or weakness", "weight loss"],
        secondary_symptoms=["blurred vision", "numbness/tingling", "slow healing wounds", "yeast infections"],
        prevalence_score=7,
        severity="Moderate",
        medical_reasoning="Insulin resistance/deficiency causes elevated blood glucose, leading to polyuria, polydipsia, fatigue, and metabolic complications.",
        recommendations="Blood glucose testing essential. Dietary changes, exercise, may need medication. Regular glucose monitoring.",
    ),
    
    "thyroid disorder": Disease(
        name="Thyroid Disorder (Hypothyroidism)",
        category=DiseaseCategory.CHRONIC,
        primary_symptoms=["fatigue or weakness", "weight gain", "cold intolerance", "dry skin"],
        secondary_symptoms=["depression", "constipation", "hair loss", "memory problems", "muscle aches"],
        prevalence_score=6,
        severity="Mild-Moderate",
        medical_reasoning="Thyroid hormone deficiency reduces metabolic rate, causing fatigue, weight gain, cold sensitivity, and depression.",
        recommendations="TSH and free T4 blood tests. Thyroid hormone replacement therapy if confirmed. Regular monitoring.",
    ),
    
    "arthritis": Disease(
        name="Arthritis (Osteoarthritis/Rheumatoid)",
        category=DiseaseCategory.CHRONIC,
        primary_symptoms=["joint pain", "stiffness", "swelling"],
        secondary_symptoms=["fatigue or weakness", "reduced mobility", "muscle body aches"],
        prevalence_score=5,
        severity="Mild-Moderate",
        medical_reasoning="Joint inflammation and/or cartilage degeneration causes pain, stiffness (worse morning), swelling, and mobility loss.",
        recommendations="Joint imaging (X-ray/MRI). Physical therapy, NSAIDs, heat therapy. Rheumatology referral for RA.",
    ),
    
    # CARDIOVASCULAR
    "heart disease": Disease(
        name="Coronary Heart Disease",
        category=DiseaseCategory.CARDIOVASCULAR,
        primary_symptoms=["chest pain", "shortness of breath", "fatigue or weakness"],
        secondary_symptoms=["nausea", "sweating", "pain in arm/shoulder", "palpitations", "dizziness"],
        prevalence_score=7,
        severity="Severe",
        medical_reasoning="Coronary artery blockage reduces heart blood flow. Classic symptom is chest pain with exertion, relieved by rest.",
        recommendations="EMERGENCY if chest pain/pressure. EKG, cardiac enzymes, angiogram may be needed. Cardiology referral essential.",
    ),
    
    "hypertension": Disease(
        name="High Blood Pressure (Hypertension)",
        category=DiseaseCategory.CARDIOVASCULAR,
        primary_symptoms=["headache", "fatigue or weakness", "dizziness"],
        secondary_symptoms=["blurred vision", "chest discomfort"],
        prevalence_score=8,
        severity="Moderate",
        medical_reasoning="Sustained elevation of blood pressure (often asymptomatic). Can present with headache, fatigue, and dizziness.",
        recommendations="Blood pressure monitoring essential. Lifestyle changes (diet, exercise, sodium reduction). May need antihypertensives.",
    ),
    
    # NEUROLOGICAL
    "migraine": Disease(
        name="Migraine Headache",
        category=DiseaseCategory.NEUROLOGICAL,
        primary_symptoms=["headache", "nausea"],
        secondary_symptoms=["vomiting", "visual disturbances", "light sensitivity", "sound sensitivity"],
        prevalence_score=6,
        severity="Mild-Moderate",
        medical_reasoning="Neurological condition causing severe throbbing headache, often unilateral, with nausea and sensory hypersensitivity.",
        recommendations="Avoid triggers. Pain management with NSAIDs or triptans. Preventive medications if frequent.",
    ),
    
    "anxiety disorder": Disease(
        name="Anxiety Disorder",
        category=DiseaseCategory.NEUROLOGICAL,
        primary_symptoms=["anxiety", "chest pain", "shortness of breath"],
        secondary_symptoms=["palpitations", "sweating", "tremor", "dizziness", "nausea"],
        prevalence_score=7,
        severity="Mild-Moderate",
        medical_reasoning="Excessive worry causes physical symptoms mimicking cardiac distress: chest tightness, sweating, palpitations, breathing difficulty.",
        recommendations="Professional evaluation to rule out cardiac causes. Cognitive behavioral therapy, relaxation techniques. May need SSRIs.",
    ),
}


class DiseaseAnalyzer:
    """Medical symptom analysis assistant with real-world medical correlations."""
    
    MIN_SYMPTOMS_THRESHOLD = 2  # Minimum symptoms needed for confident prediction
    
    def __init__(self):
        self.disease_db = DISEASE_DATABASE
        self.total_diseases = len(self.disease_db)
    
    def analyze_symptoms(
        self, user_symptoms: List[str]
    ) -> Tuple[List[Dict], str]:
        """
        Analyze symptoms and return disease predictions with reasoning.
        
        Args:
            user_symptoms: List of normalized symptoms from user
            
        Returns:
            Tuple of (predictions list, confidence_note)
            - predictions: List of dicts with disease info and reasoning
            - confidence_note: Message about prediction confidence
        """
        # Validate input
        if not user_symptoms or len(user_symptoms) < self.MIN_SYMPTOMS_THRESHOLD:
            return [], "Cannot determine disease with given symptoms"
        
        user_set = set(user_symptoms)
        disease_scores: Dict[str, Dict] = {}
        
        # Score each disease
        for disease_name, disease in self.disease_db.items():
            score_data = self._calculate_disease_match(
                user_set, disease, disease_scores
            )
            if score_data:
                disease_scores[disease_name] = score_data
        
        # Sort by score and get top 3
        sorted_diseases = sorted(
            disease_scores.items(),
            key=lambda x: x[1]["total_score"],
            reverse=True
        )[:3]
        
        if not sorted_diseases:
            return [], "Cannot determine disease with given symptoms"
        
        # Format predictions with reasoning
        predictions = []
        for rank, (disease_name, score_data) in enumerate(sorted_diseases, 1):
            disease = self.disease_db[disease_name]
            predictions.append({
                "rank": rank,
                "disease": disease.name,
                "category": disease.category.value,
                "confidence": score_data["confidence"],
                "matched_symptoms": score_data["matched_symptoms"],
                "unmatched_primary": score_data["unmatched_primary"],
                "severity": disease.severity,
                "medical_reasoning": disease.medical_reasoning,
                "recommendations": disease.recommendations,
                "total_score": score_data["total_score"],
            })
        
        # Determine confidence level
        top_confidence = predictions[0]["confidence"] if predictions else 0
        if top_confidence < 50:
            confidence_note = "Low confidence prediction. Symptoms are insufficient or non-specific. Consult healthcare provider."
        elif top_confidence < 70:
            confidence_note = "Moderate confidence. Additional symptoms or medical tests may help confirm."
        else:
            confidence_note = "Good confidence match based on symptom patterns."
        
        return predictions, confidence_note
    
    def _calculate_disease_match(
        self, user_symptoms: set, disease: Disease, existing_scores: Dict
    ) -> Optional[Dict]:
        """Calculate matching score for a disease against user symptoms with enhanced medical accuracy."""

        primary_set = set(disease.primary_symptoms)
        secondary_set = set(disease.secondary_symptoms)
        tertiary_set = set(disease.tertiary_symptoms or [])
        all_disease_symptoms = primary_set | secondary_set | tertiary_set

        # Find matched symptoms across all levels
        matched_primary = user_symptoms & primary_set
        matched_secondary = user_symptoms & secondary_set
        matched_tertiary = user_symptoms & tertiary_set
        unmatched_primary = primary_set - user_symptoms

        # Enhanced scoring system
        # Primary symptoms: 3 points (most important)
        # Secondary symptoms: 2 points (supporting)
        # Tertiary symptoms: 1 point (specific but rare)
        primary_matches = len(matched_primary)
        secondary_matches = len(matched_secondary)
        tertiary_matches = len(matched_tertiary)

        total_matches = (primary_matches * 3) + (secondary_matches * 2) + tertiary_matches

        # Calculate base confidence score
        # Weight by symptom importance and disease specificity
        max_possible = (len(primary_set) * 3) + (len(secondary_set) * 2) + len(tertiary_set)
        base_confidence = round((total_matches / max_possible) * 100) if max_possible > 0 else 0

        # Apply prevalence bonus (common diseases get slight boost)
        prevalence_bonus = disease.prevalence_score / 2  # 0-5 points

        # Specificity bonus: diseases with more unique symptoms get higher scores
        specificity_bonus = 0
        if len(all_disease_symptoms) > 0:
            unique_match_ratio = len(user_symptoms & all_disease_symptoms) / len(user_symptoms) if user_symptoms else 0
            specificity_bonus = unique_match_ratio * 20  # Up to 20 points

        # Symptom completeness bonus
        completeness_bonus = 0
        if primary_matches >= len(primary_set) * 0.7:  # 70% of primary symptoms
            completeness_bonus = 15
        elif primary_matches >= len(primary_set) * 0.5:  # 50% of primary symptoms
            completeness_bonus = 10

        # Calculate final confidence
        confidence = base_confidence + prevalence_bonus + specificity_bonus + completeness_bonus
        confidence = min(round(confidence), 100)  # Cap at 100%

        # Apply severity-based adjustments
        if disease.severity in ["Severe", "Critical"]:
            # Boost severe diseases slightly to ensure they're not missed
            confidence = min(confidence + 5, 100)

        # Calculate accuracy level based on confidence and symptom matches
        accuracy_level = self._determine_accuracy_level(
            confidence, primary_matches, secondary_matches, len(user_symptoms)
        )

        matched_symptoms = sorted(matched_primary | matched_secondary | matched_tertiary)

        return {
            "confidence": confidence,
            "accuracy_level": accuracy_level,
            "matched_symptoms": matched_symptoms,
            "unmatched_primary": sorted(unmatched_primary),
            "primary_matches": primary_matches,
            "secondary_matches": secondary_matches,
            "tertiary_matches": tertiary_matches,
            "total_score": total_matches,
            "prevalence_bonus": prevalence_bonus,
            "specificity_bonus": specificity_bonus,
            "completeness_bonus": completeness_bonus,
        }

    def _determine_accuracy_level(self, confidence: float, primary_matches: int,
                                secondary_matches: int, total_user_symptoms: int) -> str:
        """Determine accuracy level based on multiple factors."""

        # High accuracy: Strong confidence + good primary symptom coverage
        if confidence >= 80 and primary_matches >= 2:
            return "High"
        elif confidence >= 70 and (primary_matches >= 1 or secondary_matches >= 3):
            return "High-Moderate"
        elif confidence >= 60 and total_user_symptoms >= 3:
            return "Moderate"
        elif confidence >= 45 and total_user_symptoms >= 2:
            return "Moderate-Low"
        else:
            return "Low"
    
    def get_disease_info(self, disease_name: str) -> Optional[Disease]:
        """Get detailed information about a specific disease."""
        for disease in self.disease_db.values():
            if disease.name.lower() == disease_name.lower():
                return disease
        return None
    
    def suggest_medical_attention(self, predictions: List[Dict]) -> str:
        """Suggest urgency level of medical attention based on predictions."""
        if not predictions:
            return "Cannot determine. Please provide more symptoms."
        
        top_disease = predictions[0]
        severity = top_disease.get("severity", "Unknown")
        
        if severity == "Severe":
            return "🚨 URGENT: This condition requires immediate medical attention. Seek emergency care if symptoms worsen."
        elif severity == "Moderate-Severe":
            return "⚠️ IMPORTANT: Schedule doctor's appointment soon. Consider urgent care if symptoms progress rapidly."
        else:
            return "ℹ️ MONITORING: Observe symptoms. Consult doctor if symptoms persist beyond 7-10 days or worsen."


def create_analyzer() -> DiseaseAnalyzer:
    """Factory function to create analyzer instance."""
    return DiseaseAnalyzer()
