"""
Advanced Disease Predictor with Enhanced Features
Uses weighted symptoms, patient profiles, environmental factors, and negative symptoms
Provides probability-based results with improved accuracy
"""

from typing import Dict, List, Tuple, Optional
import json
from enhanced_disease_database import (
    ENHANCED_DISEASE_DATABASE,
    DiseaseProfile,
    PatientProfile,
    SymptomDetail,
    SymptomSeverity,
    SymptomPattern,
    DiseaseCategory,
    AgeGroup,
    EnvironmentalFactor,
)


class AdvancedDiseasePredictor:
    """Advanced predictor using weighted features and patient context"""
    
    def __init__(self):
        self.disease_database = ENHANCED_DISEASE_DATABASE
        self.prediction_history: List[Dict] = []
        
    def calculate_symptom_match_score(
        self, 
        symptom_detail: SymptomDetail,
        reported_symptom: Dict,
        patient_profile: PatientProfile
    ) -> float:
        """
        Calculate match score for a symptom based on reported details vs expected profile
        
        Args:
            symptom_detail: Expected symptom from disease profile
            reported_symptom: Reported symptom with details
            patient_profile: Patient information
            
        Returns:
            Score between 0-1 (1 = perfect match)
        """
        score = 0.0
        
        # Base weight from symptom importance
        base_weight = symptom_detail.weight
        
        # Duration match (30% of score)
        duration_match = 0.5
        if 'duration' in reported_symptom:
            if reported_symptom['duration'].lower() == symptom_detail.duration.value:
                duration_match = 1.0
            elif self._duration_compatible(reported_symptom['duration'], symptom_detail.duration.value):
                duration_match = 0.8
        score += duration_match * 0.3 * base_weight
        
        # Severity match (25% of score)
        severity_match = 0.5
        if 'severity' in reported_symptom:
            if reported_symptom['severity'].lower() == symptom_detail.severity.value:
                severity_match = 1.0
            elif self._severity_compatible(reported_symptom['severity'], symptom_detail.severity.value):
                severity_match = 0.7
        score += severity_match * 0.25 * base_weight
        
        # Body location match (20% of score)
        location_match = 0.5
        if 'location' in reported_symptom:
            if reported_symptom['location'].lower() in symptom_detail.body_location.lower():
                location_match = 1.0
            elif self._location_compatible(reported_symptom['location'], symptom_detail.body_location):
                location_match = 0.7
        score += location_match * 0.2 * base_weight
        
        # Pattern match (15% of score) - if reported
        pattern_match = 1.0  # Default to high if not reported
        if 'pattern' in reported_symptom:
            if reported_symptom['pattern'].lower() == symptom_detail.pattern.value:
                pattern_match = 1.0
            elif self._pattern_compatible(reported_symptom['pattern'], symptom_detail.pattern.value):
                pattern_match = 0.8
            else:
                pattern_match = 0.5
        score += pattern_match * 0.15 * base_weight
        
        # Onset order bonus (10% of score) - if applicable
        onset_bonus = 0.0
        if 'onset_order' in reported_symptom and symptom_detail.onset_order > 0:
            if reported_symptom['onset_order'] == symptom_detail.onset_order:
                onset_bonus = 1.0
            elif abs(reported_symptom['onset_order'] - symptom_detail.onset_order) <= 1:
                onset_bonus = 0.7
        score += onset_bonus * 0.1 * base_weight
        
        # Normalize to 0-1
        score = min(score, base_weight)
        
        return score
    
    def _duration_compatible(self, reported: str, expected: str) -> bool:
        """Check if reported duration is reasonably close to expected"""
        duration_ranges = {
            'hours': [0, 24],
            '1-3 days': [1, 3],
            '3-7 days': [3, 7],
            '1-2 weeks': [7, 14],
            '2-4 weeks': [14, 28],
            '1-3 months': [28, 90],
            '3+ months': [90, 999]
        }
        
        reported_lower = reported.lower()
        expected_lower = expected.lower()
        
        # Allow 1 level difference
        durations = list(duration_ranges.keys())
        if reported_lower in durations and expected_lower in durations:
            diff = abs(durations.index(reported_lower) - durations.index(expected_lower))
            return diff <= 1
        
        return False
    
    def _severity_compatible(self, reported: str, expected: str) -> bool:
        """Check if reported severity is reasonably close to expected"""
        severity_levels = ['mild', 'moderate', 'severe', 'critical']
        
        reported_lower = reported.lower()
        expected_lower = expected.lower()
        
        if reported_lower in severity_levels and expected_lower in severity_levels:
            diff = abs(severity_levels.index(reported_lower) - severity_levels.index(expected_lower))
            return diff <= 1
        
        return False
    
    def _location_compatible(self, reported: str, expected: str) -> bool:
        """Check if body location is compatible"""
        reported_lower = reported.lower()
        expected_lower = expected.lower()
        
        # Exact match
        if reported_lower in expected_lower or expected_lower in reported_lower:
            return True
        
        # Check common location mappings
        location_mappings = {
            'chest': ['lungs', 'thorax', 'ribs'],
            'head': ['temples', 'forehead', 'skull'],
            'belly': ['abdomen', 'stomach', 'intestines'],
            'throat': ['pharynx', 'larynx', 'trachea'],
            'legs': ['thighs', 'calves', 'shins', 'lower limbs'],
            'joints': ['knees', 'elbows', 'shoulders', 'hips'],
        }
        
        for key, values in location_mappings.items():
            if reported_lower.startswith(key) or expected_lower.startswith(key):
                if any(v in expected_lower or v in reported_lower for v in values):
                    return True
        
        return False
    
    def _pattern_compatible(self, reported: str, expected: str) -> bool:
        """Check if symptom pattern is compatible"""
        pattern_compatibility = {
            'continuous': ['progressive', 'recurring'],
            'intermittent': ['recurring'],
            'progressive': ['continuous'],
            'recurring': ['intermittent', 'progressive'],
        }
        
        reported_lower = reported.lower()
        expected_lower = expected.lower()
        
        if reported_lower == expected_lower:
            return True
        
        if reported_lower in pattern_compatibility:
            return expected_lower in pattern_compatibility[reported_lower]
        
        return False
    
    def assess_negative_symptoms(
        self, 
        disease_profile: DiseaseProfile,
        reported_symptoms: List[str]
    ) -> float:
        """
        Assess impact of negative symptoms (symptoms that should NOT be present)
        
        Returns penalty score (0 = no penalty, 1 = complete exclusion)
        """
        reported_lower = [s.lower() for s in reported_symptoms]
        
        penalty = 0.0
        for neg_symptom in disease_profile.negative_symptoms:
            if neg_symptom.lower() in reported_lower:
                penalty += 0.3  # Heavy penalty for negative symptoms
        
        # Cap penalty at 0.95 (never completely exclude based on negative symptoms alone)
        return min(penalty, 0.95)
    
    def assess_patient_risk_factors(
        self, 
        disease_profile: DiseaseProfile,
        patient_profile: PatientProfile
    ) -> float:
        """
        Calculate patient profile compatibility score
        
        Returns bonus/penalty between -0.5 and 0.5
        """
        score = 0.0
        
        # Age group match (up to +0.2)
        if patient_profile.age_group in disease_profile.high_risk_age_groups:
            score += 0.2
        
        # Gender match (up to +0.1)
        if disease_profile.high_risk_genders:
            if patient_profile.gender in disease_profile.high_risk_genders:
                score += 0.1
        
        # Medical history risk factors (up to +0.2)
        for risk_factor in disease_profile.medical_history_risk_factors:
            if risk_factor.lower() in [h.lower() for h in patient_profile.medical_history]:
                score += 0.2
        
        # Caps score at reasonable limits
        return score
    
    def assess_environmental_factors(
        self, 
        disease_profile: DiseaseProfile,
        environmental_factors: Optional[List[str]] = None
    ) -> float:
        """
        Calculate environmental factor compatibility
        
        Returns bonus between 0 and 0.3
        """
        if not environmental_factors:
            return 0.0
        
        score = 0.0
        env_factors_lower = [e.lower() for e in environmental_factors]
        
        for disease_env_factor in disease_profile.environmental_factors:
            factor_name = disease_env_factor.value.lower()
            if any(factor_name in e for e in env_factors_lower):
                score += 0.15
        
        return min(score, 0.3)
    
    def check_symptom_progression_order(
        self,
        disease_profile: DiseaseProfile,
        symptoms_with_order: Dict[str, int]
    ) -> float:
        """
        Check if symptom progression order matches expected pattern
        
        Returns bonus between 0 and 0.2
        """
        score = 0.0
        matches = 0
        
        for symptom, order in symptoms_with_order.items():
            if symptom.lower() in disease_profile.symptom_progression_order:
                expected_order = disease_profile.symptom_progression_order.index(symptom.lower()) + 1
                if order == expected_order:
                    matches += 1
        
        if disease_profile.symptom_progression_order and matches > 0:
            score = min(0.2 * (matches / len(disease_profile.symptom_progression_order)), 0.2)
        
        return score
    
    def predict(
        self,
        symptoms: List[Dict],  # List of symptom dicts with name, duration, severity, location, etc.
        patient_profile: Optional[PatientProfile] = None,
        environmental_factors: Optional[List[str]] = None,
        negative_symptoms: Optional[List[str]] = None,
        onset_order: Optional[Dict[str, int]] = None
    ) -> List[Tuple[str, float, Dict]]:
        """
        Predict diseases based on symptoms and context
        
        Args:
            symptoms: List of reported symptoms with details
            patient_profile: Patient demographic and medical info
            environmental_factors: Environmental risk factors
            negative_symptoms: Symptoms that are NOT present
            onset_order: Dictionary mapping symptom names to onset order (1=first, 2=second, etc.)
            
        Returns:
            List of (disease_name, probability, details) tuples sorted by probability
        """
        
        if not patient_profile:
            # Create default patient profile
            patient_profile = PatientProfile(
                age_group=AgeGroup.ADULT,
                gender='not specified'
            )
        
        negative_symptoms = negative_symptoms or []
        environmental_factors = environmental_factors or []
        onset_order = onset_order or {}
        
        disease_scores: Dict[str, float] = {}
        disease_details: Dict[str, Dict] = {}
        
        for disease_name, disease_profile in self.disease_database.items():
            score = 0.0
            details = {
                'category': disease_profile.category.value,
                'primary_symptom_matches': [],
                'secondary_symptom_matches': [],
                'negative_symptom_penalties': 0.0,
                'patient_risk_factors': 0.0,
                'environmental_factors': 0.0,
                'progression_bonus': 0.0,
                'prevalence_contribution': 0.0,
            }
            
            # Match primary symptoms (60% weight)
            primary_score = 0.0
            for primary_symptom in disease_profile.primary_symptoms:
                best_match = 0.0
                for reported in symptoms:
                    match = self.calculate_symptom_match_score(
                        primary_symptom, reported, patient_profile
                    )
                    best_match = max(best_match, match)
                
                if best_match > 0:
                    details['primary_symptom_matches'].append({
                        'symptom': primary_symptom.name,
                        'score': best_match
                    })
                    primary_score += best_match
            
            if disease_profile.primary_symptoms:
                primary_score = min(primary_score / len(disease_profile.primary_symptoms), 1.0)
            score += primary_score * 0.6
            
            # Match secondary symptoms (20% weight)
            secondary_score = 0.0
            for secondary_symptom in disease_profile.secondary_symptoms:
                best_match = 0.0
                for reported in symptoms:
                    match = self.calculate_symptom_match_score(
                        secondary_symptom, reported, patient_profile
                    )
                    best_match = max(best_match, match)
                
                if best_match > 0:
                    details['secondary_symptom_matches'].append({
                        'symptom': secondary_symptom.name,
                        'score': best_match
                    })
                    secondary_score += best_match
            
            if disease_profile.secondary_symptoms:
                secondary_score = min(secondary_score / len(disease_profile.secondary_symptoms), 1.0)
            score += secondary_score * 0.2
            
            # Negative symptoms penalty (applied to diagnosis confidence)
            neg_penalty = self.assess_negative_symptoms(disease_profile, negative_symptoms)
            details['negative_symptom_penalties'] = neg_penalty
            score *= (1.0 - neg_penalty)
            
            # Patient risk factors (5% weight)
            risk_bonus = self.assess_patient_risk_factors(disease_profile, patient_profile)
            details['patient_risk_factors'] = risk_bonus
            score += risk_bonus * 0.05
            
            # Environmental factors (5% weight)
            env_bonus = self.assess_environmental_factors(disease_profile, environmental_factors)
            details['environmental_factors'] = env_bonus
            score += env_bonus * 0.05
            
            # Symptom progression order (5% weight)
            if onset_order:
                progression_bonus = self.check_symptom_progression_order(disease_profile, onset_order)
                details['progression_bonus'] = progression_bonus
                score += progression_bonus
            
            # Prevalence score contribution (ensure common diseases get fair chance)
            prevalence_contribution = (disease_profile.prevalence_score / 10.0) * 0.05
            details['prevalence_contribution'] = prevalence_contribution
            score += prevalence_contribution
            
            disease_scores[disease_name] = max(0.0, min(score, 1.0))
            disease_details[disease_name] = details
        
        # Convert to probabilities using softmax
        probabilities = self._softmax(list(disease_scores.values()))
        
        # Create result list
        results = []
        for disease_name, prob in zip(disease_scores.keys(), probabilities):
            if prob > 0.01:  # Only include predictions > 1%
                results.append((
                    disease_name,
                    prob * 100,  # Convert to percentage
                    disease_details[disease_name]
                ))
        
        # Sort by probability (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Store in history
        self.prediction_history.append({
            'symptoms': symptoms,
            'patient_profile': patient_profile.to_dict() if patient_profile else None,
            'results': [(name, prob) for name, prob, _ in results]
        })
        
        return results
    
    def _softmax(self, scores: List[float]) -> List[float]:
        """Convert raw scores to probabilities using softmax"""
        import math
        
        if not scores:
            return []
        
        # Subtract max for numerical stability
        max_score = max(scores)
        exp_scores = [math.exp(s - max_score) for s in scores]
        sum_exp = sum(exp_scores)
        
        if sum_exp == 0:
            return [1.0 / len(scores) for _ in scores]
        
        return [e / sum_exp for e in exp_scores]
    
    def get_diagnosis_explanation(
        self,
        disease_name: str,
        prediction_details: Dict
    ) -> str:
        """Generate explanation for why a disease was predicted"""
        disease_profile = self.disease_database.get(disease_name)
        if not disease_profile:
            return ""
        
        explanation = f"""
        DISEASE: {disease_profile.disease_name}
        Category: {disease_profile.category.value}
        
        MEDICAL EXPLANATION:
        {disease_profile.medical_explanation}
        
        MATCHING SYMPTOMS:
        Primary Symptoms:
        """
        
        for match in prediction_details['primary_symptom_matches']:
            explanation += f"\n  - {match['symptom']} (match score: {match['score']:.1%})"
        
        explanation += f"\n\nSecondary Symptoms:"
        for match in prediction_details['secondary_symptom_matches']:
            explanation += f"\n  - {match['symptom']} (match score: {match['score']:.1%})"
        
        explanation += f"""
        
        KEY CLINICAL FEATURES:
        - Severity Level: {disease_profile.severity_level.value}
        - Typical Onset: {disease_profile.typical_onset}
        - Incubation Period: {disease_profile.incubation_period_min_days}-{disease_profile.incubation_period_max_days} days
        - Recovery Time: {disease_profile.recovery_time_min_days}-{disease_profile.recovery_time_max_days} days
        
        DIAGNOSTIC TESTS RECOMMENDED:
        """
        
        for test in disease_profile.diagnostic_tests:
            explanation += f"\n  - {test}"
        
        explanation += f"""
        
        TREATMENT OPTIONS:
        """
        
        for treatment in disease_profile.treatment_options[:3]:  # Top 3 treatments
            explanation += f"\n  - {treatment}"
        
        explanation += f"""
        
        DIFFERENTIAL DIAGNOSES TO CONSIDER:
        """
        
        for diff_diag in disease_profile.differential_diagnoses[:3]:
            explanation += f"\n  - {diff_diag}"
        
        explanation += f"""
        
        POSSIBLE COMPLICATIONS:
        """
        
        for complication in disease_profile.complications[:3]:
            explanation += f"\n  - {complication}"
        
        return explanation
        
    def format_results_as_table(
        self,
        results: List[Tuple[str, float, Dict]],
        top_n: int = 10
    ) -> str:
        """Format prediction results as table"""
        output = "\n" + "="*80 + "\n"
        output += "DISEASE PREDICTION RESULTS (Probability-Based)\n"
        output += "="*80 + "\n"
        output += f"{'Rank':<6} {'Disease Name':<30} {'Probability':<15} {'Category':<15}\n"
        output += "-"*80 + "\n"
        
        for rank, (disease_name, probability, details) in enumerate(results[:top_n], 1):
            output += f"{rank:<6} {disease_name:<30} {probability:>6.2f}%          {details['category']:<15}\n"
        
        output += "="*80 + "\n"
        
        return output


# Example usage function
def example_prediction():
    """Example of how to use the advanced predictor"""
    
    predictor = AdvancedDiseasePredictor()
    
    # Example 1: Patient with flu-like symptoms
    symptoms = [
        {'name': 'fever', 'duration': '3-7 days', 'severity': 'moderate', 
         'location': 'whole body'},
        {'name': 'cough', 'duration': '1-2 weeks', 'severity': 'moderate', 
         'location': 'chest'},
        {'name': 'muscle aches', 'duration': '3-7 days', 'severity': 'moderate', 
         'location': 'full body'},
        {'name': 'headache', 'duration': '3-7 days', 'severity': 'moderate', 
         'location': 'head'},
    ]
    
    patient = PatientProfile(
        age_group=AgeGroup.ADULT,
        gender='male',
        medical_history=['asthma'],
        vaccination_status={'flu': False}
    )
    
    negative_symptoms = ['loss of taste', 'loss of smell', 'severe abdominal pain']
    
    results = predictor.predict(
        symptoms=symptoms,
        patient_profile=patient,
        negative_symptoms=negative_symptoms,
        environmental_factors=['crowded living']
    )
    
    print(predictor.format_results_as_table(results, top_n=5))
    
    # Print explanation for top diagnosis
    if results:
        top_disease, top_prob, top_details = results[0]
        print(predictor.get_diagnosis_explanation(top_disease, top_details))


if __name__ == "__main__":
    example_prediction()

