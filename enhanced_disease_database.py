"""
Advanced Disease Database with Enhanced Features
Includes symptom details, body locations, timeline, patient profiles, and environmental factors
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


class DiseaseCategory(Enum):
    """Disease classification"""
    VIRAL = "Viral"
    BACTERIAL = "Bacterial"
    CHRONIC = "Chronic"
    PARASITIC = "Parasitic"
    GENETIC = "Genetic"
    AUTOIMMUNE = "Autoimmune"
    METABOLIC = "Metabolic"
    NEUROLOGICAL = "Neurological"
    CARDIOVASCULAR = "Cardiovascular"
    RESPIRATORY = "Respiratory"
    DIGESTIVE = "Digestive"
    DERMATOLOGICAL = "Dermatological"


class SymptomDuration(Enum):
    """Symptom duration classification"""
    HOURS = "hours"
    ONE_TO_THREE_DAYS = "1-3 days"
    THREE_TO_SEVEN_DAYS = "3-7 days"
    ONE_TO_TWO_WEEKS = "1-2 weeks"
    TWO_TO_FOUR_WEEKS = "2-4 weeks"
    ONE_TO_THREE_MONTHS = "1-3 months"
    CHRONIC = "3+ months"


class SymptomSeverity(Enum):
    """Symptom severity levels"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class SymptomPattern(Enum):
    """Symptom patterns"""
    CONTINUOUS = "continuous"
    INTERMITTENT = "intermittent"
    PROGRESSIVE = "progressive"
    RECURRING = "recurring"


class AgeGroup(Enum):
    """Patient age groups"""
    INFANT = "infant (0-1 years)"
    TODDLER = "toddler (1-3 years)"
    CHILD = "child (4-11 years)"
    ADOLESCENT = "adolescent (12-17 years)"
    YOUNG_ADULT = "young adult (18-25 years)"
    ADULT = "adult (26-50 years)"
    MIDDLE_AGED = "middle-aged (51-65 years)"
    ELDERLY = "elderly (65+ years)"


class Gender(Enum):
    """Patient gender"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    NOT_APPLICABLE = "n/a"


class EnvironmentalFactor(Enum):
    """Environmental risk factors"""
    TROPICAL_CLIMATE = "tropical/subtropical"
    TEMPERATE_CLIMATE = "temperate"
    COLD_CLIMATE = "cold climate"
    URBAN = "urban area"
    RURAL = "rural area"
    HIGH_ALTITUDE = "high altitude"
    COASTAL = "coastal area"
    POOR_SANITATION = "poor sanitation"
    CROWDED_LIVING = "crowded living"
    MOSQUITO_PRONE = "mosquito-prone"
    TICK_PRONE = "tick-prone"
    CONTAMINATED_WATER = "contaminated water"
    HIGH_POLLEN = "high pollen"
    WORKPLACE_HAZARD = "workplace hazard"
    POOR_AIR_QUALITY = "poor air quality"


@dataclass
class SymptomDetail:
    """Enhanced symptom with detailed characteristics"""
    name: str
    duration: SymptomDuration
    severity: SymptomSeverity
    pattern: SymptomPattern
    body_location: str  # e.g., "chest", "abdomen", "head", "joints", "throat"
    weight: float = 1.0  # Importance score (0.5 - 2.0)
    onset_order: int = 0  # Order of appearance (1=first, 2=second, etc.)
    associated_findings: List[str] = field(default_factory=list)  # Related findings
    affected_by: List[str] = field(default_factory=list)  # What makes it worse/better
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'duration': self.duration.value,
            'severity': self.severity.value,
            'pattern': self.pattern.value,
            'body_location': self.body_location,
            'weight': self.weight,
            'onset_order': self.onset_order,
            'associated_findings': self.associated_findings,
            'affected_by': self.affected_by
        }


@dataclass
class PatientProfile:
    """Patient demographic and medical information"""
    age_group: AgeGroup
    gender: Gender
    medical_history: List[str] = field(default_factory=list)  # e.g., ["diabetes", "hypertension"]
    current_medications: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)
    vaccination_status: Dict[str, bool] = field(default_factory=dict)
    immune_status: str = "normal"  # normal, immunocompromised, immunoenhanced
    pregnancy_status: str = "not applicable"  # not applicable, first trimester, etc.
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'age_group': self.age_group.value,
            'gender': self.gender.value,
            'medical_history': self.medical_history,
            'current_medications': self.current_medications,
            'allergies': self.allergies,
            'vaccination_status': self.vaccination_status,
            'immune_status': self.immune_status,
            'pregnancy_status': self.pregnancy_status
        }


@dataclass
class DiseaseProfile:
    """Comprehensive disease profile with all enhanced features"""
    disease_name: str
    category: DiseaseCategory
    primary_symptoms: List[SymptomDetail]  # Most specific symptoms
    secondary_symptoms: List[SymptomDetail]  # Supporting symptoms
    negative_symptoms: List[str]  # Important symptoms that should NOT be present
    severity_level: SymptomSeverity
    prevalence_score: int = 5  # 1-10 scale
    
    # Timeline and progression
    typical_onset: str = ""  # e.g., "sudden", "gradual"
    incubation_period_min_days: int = 0
    incubation_period_max_days: int = 0
    symptom_progression_order: List[str] = field(default_factory=list)  # Expected order
    
    # Patient factors
    high_risk_age_groups: List[AgeGroup] = field(default_factory=list)
    high_risk_genders: List[Gender] = field(default_factory=list)  # If gender-specific
    medical_history_risk_factors: List[str] = field(default_factory=list)  # Comorbidities
    
    # Environmental factors
    environmental_factors: List[EnvironmentalFactor] = field(default_factory=list)
    seasonal_pattern: str = ""  # e.g., "year-round", "winter", "summer", "monsoon"
    transmission_route: str = ""  # e.g., "airborne", "waterborne", "vector", "contact"
    
    # Clinical information
    diagnostic_tests: List[str] = field(default_factory=list)
    treatment_options: List[str] = field(default_factory=list)
    complications: List[str] = field(default_factory=list)
    recovery_time_min_days: int = 0
    recovery_time_max_days: int = 0
    
    # Medical reasoning
    medical_explanation: str = ""
    differential_diagnoses: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'disease_name': self.disease_name,
            'category': self.category.value,
            'primary_symptoms': [s.to_dict() for s in self.primary_symptoms],
            'secondary_symptoms': [s.to_dict() for s in self.secondary_symptoms],
            'negative_symptoms': self.negative_symptoms,
            'severity_level': self.severity_level.value,
            'prevalence_score': self.prevalence_score,
            'typical_onset': self.typical_onset,
            'incubation_period': f"{self.incubation_period_min_days}-{self.incubation_period_max_days} days",
            'symptom_progression_order': self.symptom_progression_order,
            'high_risk_age_groups': [ag.value for ag in self.high_risk_age_groups],
            'high_risk_genders': [g.value for g in self.high_risk_genders],
            'medical_history_risk_factors': self.medical_history_risk_factors,
            'environmental_factors': [ef.value for ef in self.environmental_factors],
            'seasonal_pattern': self.seasonal_pattern,
            'transmission_route': self.transmission_route,
            'diagnostic_tests': self.diagnostic_tests,
            'treatment_options': self.treatment_options,
            'complications': self.complications,
            'recovery_time': f"{self.recovery_time_min_days}-{self.recovery_time_max_days} days",
            'medical_explanation': self.medical_explanation,
            'differential_diagnoses': self.differential_diagnoses
        }


# ============================================================================
# COMPREHENSIVE ENHANCED DISEASE DATABASE
# ============================================================================

ENHANCED_DISEASE_DATABASE: Dict[str, DiseaseProfile] = {
    # ========== VIRAL INFECTIONS ==========
    "influenza": DiseaseProfile(
        disease_name="Influenza (Flu)",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=[
            SymptomDetail(name="fever", duration=SymptomDuration.THREE_TO_SEVEN_DAYS, 
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=2.0, onset_order=1),
            SymptomDetail(name="cough", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="chest/throat", weight=1.8, onset_order=1),
            SymptomDetail(name="muscle aches", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="full body", weight=1.9, onset_order=1,
                         associated_findings=["malaise", "decreased activity"]),
            SymptomDetail(name="headache", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="head/temples", weight=1.5, onset_order=1),
        ],
        secondary_symptoms=[
            SymptomDetail(name="sore throat", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="throat", weight=1.2, onset_order=2),
            SymptomDetail(name="chills", duration=SymptomDuration.HOURS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="whole body", weight=1.0, onset_order=1),
            SymptomDetail(name="fatigue", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.3, onset_order=2),
        ],
        negative_symptoms=["loss of taste", "loss of smell", "diarrhea"],
        severity_level=SymptomSeverity.MODERATE,
        prevalence_score=9,
        typical_onset="sudden",
        incubation_period_min_days=1,
        incubation_period_max_days=4,
        symptom_progression_order=["fever", "muscle aches", "headache", "cough", "sore throat"],
        high_risk_age_groups=[AgeGroup.INFANT, AgeGroup.ELDERLY, AgeGroup.MIDDLE_AGED],
        high_risk_genders=[],
        medical_history_risk_factors=["asthma", "COPD", "heart disease", "diabetes"],
        environmental_factors=[EnvironmentalFactor.CROWDED_LIVING, EnvironmentalFactor.POOR_AIR_QUALITY],
        seasonal_pattern="winter",
        transmission_route="airborne",
        diagnostic_tests=["rapid flu test", "PCR test", "culture test"],
        treatment_options=["antiviral medications (oseltamivir, zanamivir)", "rest", "hydration", "NSAIDs"],
        complications=["pneumonia", "bronchitis", "secondary bacterial infection"],
        recovery_time_min_days=5,
        recovery_time_max_days=14,
        medical_explanation="Influenza virus causes rapid onset respiratory infection with systemic symptoms. The combination of sudden fever + muscle aches + headache at onset is classic for flu. Cough follows.",
        differential_diagnoses=["COVID-19", "common cold", "bacterial pneumonia", "RSV"],
    ),
    
    "covid-19": DiseaseProfile(
        disease_name="COVID-19",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=[
            SymptomDetail(name="fever", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.8, onset_order=1),
            SymptomDetail(name="cough", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="chest/throat", weight=1.9, onset_order=2),
            SymptomDetail(name="loss of taste", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="mouth", weight=2.0, onset_order=3,
                         associated_findings=["ageusia", "anosmia"]),
            SymptomDetail(name="loss of smell", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="nose/brain", weight=2.0, onset_order=3,
                         associated_findings=["anosmia"]),
            SymptomDetail(name="shortness of breath", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="lungs/chest", weight=2.0, onset_order=3),
        ],
        secondary_symptoms=[
            SymptomDetail(name="headache", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="head", weight=1.2, onset_order=2),
            SymptomDetail(name="fatigue", duration=SymptomDuration.TWO_TO_FOUR_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="whole body", weight=1.5, onset_order=2),
            SymptomDetail(name="muscle aches", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="full body", weight=1.0, onset_order=2),
            SymptomDetail(name="diarrhea", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="abdomen", weight=0.8, onset_order=4),
        ],
        negative_symptoms=["severe vomiting", "severe abdominal pain"],
        severity_level=SymptomSeverity.MODERATE,
        prevalence_score=7,
        typical_onset="gradual",
        incubation_period_min_days=2,
        incubation_period_max_days=14,
        symptom_progression_order=["fever", "cough", "fatigue", "loss of taste/smell", "shortness of breath"],
        high_risk_age_groups=[AgeGroup.ELDERLY, AgeGroup.MIDDLE_AGED],
        high_risk_genders=[],
        medical_history_risk_factors=["obesity", "diabetes", "hypertension", "heart disease", "lung disease"],
        environmental_factors=[EnvironmentalFactor.CROWDED_LIVING, EnvironmentalFactor.HIGH_POPULATION],
        seasonal_pattern="year-round",
        transmission_route="airborne/aerosol",
        diagnostic_tests=["COVID-19 PCR test", "rapid antigen test", "antibody test"],
        treatment_options=["supportive care", "oxygen therapy", "antivirals (paxlovid)", "monoclonal antibodies"],
        complications=["pneumonia", "sepsis", "blood clots", "myocarditis", "long COVID"],
        recovery_time_min_days=7,
        recovery_time_max_days=21,
        medical_explanation="COVID-19 presents with gradual onset respiratory symptoms. Distinctive features include loss of taste/smell early in course and progressive shortness of breath. More variable progression than flu.",
        differential_diagnoses=["influenza", "common cold", "pneumonia", "RSV"],
    ),
    
    "common cold": DiseaseProfile(
        disease_name="Common Cold",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=[
            SymptomDetail(name="runny nose", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="nose", weight=2.0, onset_order=1),
            SymptomDetail(name="sore throat", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="throat", weight=1.8, onset_order=1),
            SymptomDetail(name="cough", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="chest/throat", weight=1.6, onset_order=2),
            SymptomDetail(name="sneezing", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="nose", weight=1.5, onset_order=1),
        ],
        secondary_symptoms=[
            SymptomDetail(name="headache", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="head", weight=0.8, onset_order=3),
            SymptomDetail(name="mild fever", duration=SymptomDuration.HOURS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="whole body", weight=0.7, onset_order=3),
            SymptomDetail(name="fatigue", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=0.9, onset_order=3),
        ],
        negative_symptoms=["high fever", "loss of taste", "loss of smell", "severe muscle aches"],
        severity_level=SymptomSeverity.MILD,
        prevalence_score=10,
        typical_onset="gradual",
        incubation_period_min_days=1,
        incubation_period_max_days=3,
        symptom_progression_order=["runny nose", "sore throat", "mild cough", "sneezing"],
        high_risk_age_groups=[],
        high_risk_genders=[],
        medical_history_risk_factors=[],
        environmental_factors=[EnvironmentalFactor.CROWDED_LIVING, EnvironmentalFactor.POOR_AIR_QUALITY],
        seasonal_pattern="winter more common but year-round",
        transmission_route="airborne/contact",
        diagnostic_tests=["clinical diagnosis", "viral culture (if needed)"],
        treatment_options=["supportive care", "OTC cold remedies", "zinc lozenges within 24 hours", "rest"],
        recovery_time_min_days=3,
        recovery_time_max_days=10,
        medical_explanation="Most common viral infection causing mild upper respiratory symptoms. Absence of high fever and muscle aches distinguishes from flu.",
        differential_diagnoses=["influenza", "allergic rhinitis", "RSV"],
    ),
    
    "dengue": DiseaseProfile(
        disease_name="Dengue Fever",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=[
            SymptomDetail(name="fever", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.BIPHASIC,
                         body_location="whole body", weight=2.0, onset_order=1,
                         associated_findings=["high temperature >39°C"]),
            SymptomDetail(name="joint pain", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="joints/limbs", weight=2.0, onset_order=1,
                         affected_by=["can completely incapacitate patients"]),
            SymptomDetail(name="muscle aches", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="full body", weight=2.0, onset_order=1),
            SymptomDetail(name="headache", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="behind eyes/full head", weight=1.9, onset_order=1),
            SymptomDetail(name="eye pain", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="eyes/behind eyes", weight=1.7, onset_order=1),
            SymptomDetail(name="rash", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="chest/limbs", weight=1.6, onset_order=4),
        ],
        secondary_symptoms=[
            SymptomDetail(name="nausea", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="stomach", weight=0.9, onset_order=2),
            SymptomDetail(name="vomiting", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.INTERMITTENT,
                         body_location="stomach", weight=0.8, onset_order=2),
            SymptomDetail(name="fatigue", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.2, onset_order=3),
        ],
        negative_symptoms=["cough", "sore throat", "runny nose"],
        severity_level=SymptomSeverity.SEVERE,
        prevalence_score=7,
        typical_onset="sudden",
        incubation_period_min_days=3,
        incubation_period_max_days=14,
        symptom_progression_order=["fever", "severe joint/muscle pain", "headache", "eye pain", "rash"],
        high_risk_age_groups=[AgeGroup.CHILD, AgeGroup.YOUNG_ADULT, AgeGroup.ADULT],
        high_risk_genders=[],
        medical_history_risk_factors=["secondary dengue infection"],
        environmental_factors=[EnvironmentalFactor.TROPICAL_CLIMATE, EnvironmentalFactor.MOSQUITO_PRONE],
        seasonal_pattern="monsoon season in tropical areas",
        transmission_route="mosquito vector (Aedes)",
        diagnostic_tests=["dengue serology (IgM/IgG)", "NS1 antigen test", "PCR"],
        treatment_options=["supportive care", "hydration", "NSAIDs", "careful monitoring for hemorrhagic progression"],
        complications=["dengue hemorrhagic fever", "dengue shock syndrome", "internal bleeding"],
        recovery_time_min_days=7,
        recovery_time_max_days=14,
        medical_explanation="Dengue from Aedes mosquito causes sudden high fever with severe joint/muscle pain (breakbone fever). Characteristic eye pain and biphasic fever pattern. Rash appears after fever breaks.",
        differential_diagnoses=["malaria", "chikungunya", "Zika", "yellow fever"],
    ),
    
    "malaria": DiseaseProfile(
        disease_name="Malaria",
        category=DiseaseCategory.PARASITIC,
        primary_symptoms=[
            SymptomDetail(name="fever", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.RECURRING,
                         body_location="whole body", weight=2.0, onset_order=1,
                         associated_findings=["cyclic pattern: every 48-72 hours"]),
            SymptomDetail(name="chills", duration=SymptomDuration.HOURS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.INTERMITTENT,
                         body_location="whole body", weight=1.9, onset_order=1),
            SymptomDetail(name="sweating", duration=SymptomDuration.HOURS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.INTERMITTENT,
                         body_location="whole body", weight=1.8, onset_order=1),
            SymptomDetail(name="headache", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="head/temples", weight=1.7, onset_order=1),
            SymptomDetail(name="muscle aches", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="full body", weight=1.5, onset_order=1),
        ],
        secondary_symptoms=[
            SymptomDetail(name="fatigue", duration=SymptomDuration.TWO_TO_FOUR_WEEKS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.4, onset_order=2),
            SymptomDetail(name="nausea", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.INTERMITTENT,
                         body_location="stomach", weight=0.9, onset_order=2),
            SymptomDetail(name="vomiting", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.INTERMITTENT,
                         body_location="stomach", weight=0.8, onset_order=2),
            SymptomDetail(name="diarrhea", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="abdomen", weight=0.7, onset_order=3),
        ],
        negative_symptoms=["productive cough", "sore throat", "runny nose"],
        severity_level=SymptomSeverity.SEVERE,
        prevalence_score=7,
        typical_onset="gradual",
        incubation_period_min_days=7,
        incubation_period_max_days=30,
        symptom_progression_order=["fever cycles", "chills", "sweating", "muscle aches", "headache"],
        high_risk_age_groups=[AgeGroup.CHILD, AgeGroup.INFANT],
        high_risk_genders=[],
        medical_history_risk_factors=["sickle cell disease (partial protection)"],
        environmental_factors=[EnvironmentalFactor.TROPICAL_CLIMATE, EnvironmentalFactor.MOSQUITO_PRONE, EnvironmentalFactor.RURAL],
        seasonal_pattern="varies by region, often with rainy season",
        transmission_route="mosquito vector (Anopheles)",
        diagnostic_tests=["blood smear microscopy", "malaria antigen test", "PCR"],
        treatment_options=["antimalarials (artemisinin-based combination therapy)", "supportive care"],
        complications=["cerebral malaria", "severe anemia", "acute kidney injury", "pulmonary edema"],
        recovery_time_min_days=14,
        recovery_time_max_days=30,
        medical_explanation="Malaria from mosquito causes cyclic fever pattern (every 48-72 hours depending on species). Chills followed by fever followed by sweating cycle.",
        differential_diagnoses=["dengue", "typhoid", "yellow fever", "influenza"],
    ),
    
    # ========== BACTERIAL INFECTIONS ==========
    "strep throat": DiseaseProfile(
        disease_name="Streptococcal Pharyngitis (Strep Throat)",
        category=DiseaseCategory.BACTERIAL,
        primary_symptoms=[
            SymptomDetail(name="sore throat", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="throat/pharynx", weight=2.0, onset_order=1,
                         associated_findings=["redness", "exudate", "enlarged tonsils"]),
            SymptomDetail(name="fever", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.9, onset_order=1),
            SymptomDetail(name="headache", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="head", weight=1.5, onset_order=1),
            SymptomDetail(name="difficulty swallowing", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="throat", weight=1.8, onset_order=1),
        ],
        secondary_symptoms=[
            SymptomDetail(name="muscle aches", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="full body", weight=1.0, onset_order=2),
            SymptomDetail(name="swollen lymph nodes", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="neck", weight=1.4, onset_order=2),
            SymptomDetail(name="belly pain/nausea", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="abdomen", weight=0.8, onset_order=3),
        ],
        negative_symptoms=["cough", "runny nose", "sneezing"],
        severity_level=SymptomSeverity.MODERATE,
        prevalence_score=8,
        typical_onset="sudden",
        incubation_period_min_days=1,
        incubation_period_max_days=3,
        symptom_progression_order=["sore throat", "fever", "difficulty swallowing", "headache"],
        high_risk_age_groups=[AgeGroup.CHILD, AgeGroup.ADOLESCENT],
        high_risk_genders=[],
        medical_history_risk_factors=[],
        environmental_factors=[EnvironmentalFactor.CROWDED_LIVING],
        seasonal_pattern="winter more common",
        transmission_route="respiratory droplets",
        diagnostic_tests=["rapid strep test", "throat culture", "rapid molecular test"],
        treatment_options=["antibiotics (penicillin or amoxicillin)", "supportive care", "throat lozenges"],
        complications=["acute rheumatic fever", "post-streptococcal glomerulonephritis", "abscess", "scarlet fever"],
        recovery_time_min_days=5,
        recovery_time_max_days=10,
        medical_explanation="Group A Streptococcus causes sudden severe sore throat with fever but notably WITHOUT cough/runny nose (unlike viral pharyngitis). Absence of respiratory symptoms is key differentiator.",
        differential_diagnoses=["viral sore throat", "mononucleosis", "influenza"],
    ),
    
    "pneumonia": DiseaseProfile(
        disease_name="Bacterial Pneumonia",
        category=DiseaseCategory.BACTERIAL,
        primary_symptoms=[
            SymptomDetail(name="cough", duration=SymptomDuration.ONE_TO_FOUR_WEEKS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="chest/throat", weight=2.0, onset_order=1,
                         associated_findings=["productive with purulent or rusty sputum"]),
            SymptomDetail(name="fever", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.9, onset_order=1),
            SymptomDetail(name="chest pain", duration=SymptomDuration.ONE_TO_FOUR_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="chest", weight=1.7, onset_order=2,
                         affected_by=["worse with breathing or coughing"]),
            SymptomDetail(name="shortness of breath", duration=SymptomDuration.ONE_TO_FOUR_WEEKS,
                         severity=SymptomSeverity.SEVERE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="lungs/chest", weight=1.9, onset_order=2),
        ],
        secondary_symptoms=[
            SymptomDetail(name="headache", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="head", weight=0.9, onset_order=2),
            SymptomDetail(name="muscle aches", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="full body", weight=0.8, onset_order=2),
            SymptomDetail(name="fatigue", duration=SymptomDuration.TWO_TO_FOUR_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.3, onset_order=3),
            SymptomDetail(name="abdominal pain", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="abdomen", weight=0.6, onset_order=3),
        ],
        negative_symptoms=[],
        severity_level=SymptomSeverity.SEVERE,
        prevalence_score=7,
        typical_onset="gradual",
        incubation_period_min_days=1,
        incubation_period_max_days=3,
        symptom_progression_order=["fever", "cough", "chest pain", "shortness of breath"],
        high_risk_age_groups=[AgeGroup.ELDERLY, AgeGroup.INFANT],
        high_risk_genders=[],
        medical_history_risk_factors=["COPD", "asthma", "heart disease", "diabetes", "smoking"],
        environmental_factors=[],
        seasonal_pattern="year-round but more in winter",
        transmission_route="respiratory droplets/airborne",
        diagnostic_tests=["chest X-ray", "sputum culture", "blood culture", "rapid bacterial tests"],
        treatment_options=["antibiotics (variety depending on organism)", "supportive care", "oxygen therapy"],
        complications=["sepsis", "respiratory failure", "pleural effusion", "empyema", "acute respiratory distress syndrome"],
        recovery_time_min_days=14,
        recovery_time_max_days=30,
        medical_explanation="Bacterial pneumonia causes productive cough with fever, chest pain, and shortness of breath. Productive cough distinguishes from viral pneumonia.",
        differential_diagnoses=["viral pneumonia", "aspiration pneumonia", "pulmonary embolism"],
    ),
    
    # ========== CHRONIC DISEASES ==========
    "type 2 diabetes": DiseaseProfile(
        disease_name="Type 2 Diabetes Mellitus",
        category=DiseaseCategory.METABOLIC,
        primary_symptoms=[
            SymptomDetail(name="increased thirst", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="mouth/whole body", weight=1.8, onset_order=1),
            SymptomDetail(name="increased urination", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="urinary tract", weight=1.8, onset_order=1),
            SymptomDetail(name="fatigue", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.6, onset_order=2),
            SymptomDetail(name="slow wound healing", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="skin/wounds", weight=1.5, onset_order=3),
        ],
        secondary_symptoms=[
            SymptomDetail(name="blurred vision", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="eyes", weight=1.2, onset_order=3),
            SymptomDetail(name="numbness in feet", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="feet/lower legs", weight=1.1, onset_order=4),
            SymptomDetail(name="yeast infections", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.RECURRING,
                         body_location="groins/skin folds", weight=0.9, onset_order=4),
        ],
        negative_symptoms=["acute fever", "sudden onset"],
        severity_level=SymptomSeverity.MODERATE,
        prevalence_score=8,
        typical_onset="very gradual",
        incubation_period_min_days=0,
        incubation_period_max_days=0,
        symptom_progression_order=["increased thirst", "increased urination", "fatigue", "slow healing", "complications"],
        high_risk_age_groups=[AgeGroup.ADULT, AgeGroup.MIDDLE_AGED, AgeGroup.ELDERLY],
        high_risk_genders=[],
        medical_history_risk_factors=["obesity", "family history", "hypertension", "sedentary lifestyle"],
        environmental_factors=[EnvironmentalFactor.POOR_DIET, EnvironmentalFactor.SEDENTARY],
        seasonal_pattern="year-round",
        transmission_route="n/a (metabolic)",
        diagnostic_tests=["fasting blood glucose", "HbA1c", "oral glucose tolerance test", "random blood glucose"],
        treatment_options=["oral medications (metformin, sulfonylureas, DPP-4 inhibitors)", "insulin therapy", "diet/exercise"],
        complications=["diabetic neuropathy", "diabetic retinopathy", "diabetic nephropathy", "cardiovascular disease"],
        recovery_time_min_days=0,
        recovery_time_max_days=0,
        medical_explanation="Type 2 diabetes develops gradually with symptoms of hyperglycemia. Often asymptomatic in early stages. Polyuria and polydipsia are cardinal features.",
        differential_diagnoses=["type 1 diabetes", "gestational diabetes", "stress hyperglycemia"],
    ),
    
    "hypertension": DiseaseProfile(
        disease_name="Hypertension (High Blood Pressure)",
        category=DiseaseCategory.CARDIOVASCULAR,
        primary_symptoms=[
            SymptomDetail(name="no symptoms", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="n/a", weight=2.0, onset_order=1,
                         associated_findings=["often called 'silent killer'"]),
            SymptomDetail(name="headache", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.RECURRING,
                         body_location="back of head", weight=0.8, onset_order=2),
            SymptomDetail(name="dizziness", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="head/inner ear", weight=0.7, onset_order=3),
        ],
        secondary_symptoms=[
            SymptomDetail(name="shortness of breath", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="lungs/chest", weight=0.9, onset_order=3),
            SymptomDetail(name="chest discomfort", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.INTERMITTENT,
                         body_location="chest", weight=0.7, onset_order=4),
            SymptomDetail(name="frequent urination", duration=SymptomDuration.CHRONIC,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="urinary tract", weight=0.6, onset_order=4),
        ],
        negative_symptoms=[],
        severity_level=SymptomSeverity.MODERATE,
        prevalence_score=8,
        typical_onset="very gradual",
        incubation_period_min_days=0,
        incubation_period_max_days=0,
        symptom_progression_order=["no symptoms", "occasional headaches", "dizziness"],
        high_risk_age_groups=[AgeGroup.MIDDLE_AGED, AgeGroup.ELDERLY],
        high_risk_genders=[AgeGroup.MALE],
        medical_history_risk_factors=["obesity", "family history", "stress", "smoking", "high sodium diet"],
        environmental_factors=[EnvironmentalFactor.POOR_AIR_QUALITY, EnvironmentalFactor.HIGH_STRESS],
        seasonal_pattern="slightly higher in winter",
        transmission_route="n/a (chronic)",
        diagnostic_tests=["blood pressure monitoring", "ECG", "echocardiogram", "renal function tests"],
        treatment_options=["ACE inhibitors", "beta blockers", "calcium channel blockers", "diuretics", "lifestyle modification"],
        complications=["heart attack", "stroke", "heart failure", "kidney disease"],
        recovery_time_min_days=0,
        recovery_time_max_days=0,
        medical_explanation="Hypertension is often asymptomatic. When symptoms exist, headache and dizziness are most common. Diagnosis requires BP measurement.",
        differential_diagnoses=["anxiety disorder", "anemia", "thyroid disease"],
    ),
    
    # ========== PARASITIC INFECTIONS ==========
    "chicken pox": DiseaseProfile(
        disease_name="Chickenpox (Varicella)",
        category=DiseaseCategory.VIRAL,
        primary_symptoms=[
            SymptomDetail(name="rash", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.PROGRESSIVE,
                         body_location="trunk/face/scalp, spreading to limbs", weight=2.0, onset_order=2,
                         associated_findings=["fluid-filled vesicles", "crops appearing for 3-6 days"]),
            SymptomDetail(name="itching", duration=SymptomDuration.ONE_TO_TWO_WEEKS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="affected skin", weight=1.8, onset_order=2),
            SymptomDetail(name="fever", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MODERATE, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.5, onset_order=1),
            SymptomDetail(name="fatigue", duration=SymptomDuration.THREE_TO_SEVEN_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="whole body", weight=1.0, onset_order=1),
        ],
        secondary_symptoms=[
            SymptomDetail(name="sore throat", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="throat", weight=0.7, onset_order=1),
            SymptomDetail(name="headache", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="head", weight=0.7, onset_order=1),
            SymptomDetail(name="muscle aches", duration=SymptomDuration.ONE_TO_THREE_DAYS,
                         severity=SymptomSeverity.MILD, pattern=SymptomPattern.CONTINUOUS,
                         body_location="full body", weight=0.6, onset_order=1),
        ],
        negative_symptoms=["high fever (usually <39°C)", "severe respiratory symptoms"],
        severity_level=SymptomSeverity.MODERATE,
        prevalence_score=6,
        typical_onset="sudden",
        incubation_period_min_days=10,
        incubation_period_max_days=21,
        symptom_progression_order=["fever", "fatigue", "rash appears", "vesicles become pustules then crust"],
        high_risk_age_groups=[AgeGroup.CHILD, AgeGroup.TODDLER],
        high_risk_genders=[],
        medical_history_risk_factors=["immunocompromised"],
        environmental_factors=[EnvironmentalFactor.CROWDED_LIVING],
        seasonal_pattern="winter/spring more common",
        transmission_route="respiratory droplets/airborne",
        diagnostic_tests=["clinical diagnosis", "varicella serology", "PCR if needed"],
        treatment_options=["supportive care", "antivirals (acyclovir if severe)", "calamine lotion", "antihistamines"],
        complications=["secondary bacterial infection", "encephalitis", "pneumonia", "congenital varicella syndrome"],
        recovery_time_min_days=7,
        recovery_time_max_days=14,
        medical_explanation="Varicella presents with fever followed by characteristic rash that progresses from macules to papules to vesicles to crusts. Rash distribution is key feature.",
        differential_diagnoses=["measles", "rubella", "herpes zoster", "shingles"],
    ),
}


def get_disease_profile(disease_name: str) -> Optional[DiseaseProfile]:
    """Get enhanced disease profile by name"""
    return ENHANCED_DISEASE_DATABASE.get(disease_name.lower())


def list_all_diseases() -> List[str]:
    """Get list of all diseases in database"""
    return list(ENHANCED_DISEASE_DATABASE.keys())


def get_diseases_by_category(category: DiseaseCategory) -> List[str]:
    """Get all diseases in a specific category"""
    return [
        name for name, profile in ENHANCED_DISEASE_DATABASE.items()
        if profile.category == category
    ]

