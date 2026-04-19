"""
Integration Guide: Advanced Disease Prediction System
Shows how to integrate all enhanced components
"""

from advanced_disease_predictor import AdvancedDiseasePredictor
from enhanced_disease_database import (
    AgeGroup, Gender, EnvironmentalFactor, DiseaseCategory, PatientProfile
)
from enhanced_dataset_generator import EnhancedDatasetGenerator
import json
from typing import Dict, List


class IntegratedDiseasePredictionSystem:
    """Unified system combining all enhanced features"""
    
    def __init__(self):
        self.predictor = AdvancedDiseasePredictor()
        
    def predict_from_user_input(
        self,
        symptoms_input: Dict,
        patient_demographics: Dict,
        environmental_info: Dict = None,
        negative_symptoms_input: List[str] = None
    ) -> Dict:
        """
        Main prediction method - accepts user input and returns structured results
        
        Args:
            symptoms_input: Dictionary with symptom information
                {
                    'symptoms': [
                        {
                            'name': 'fever',
                            'duration': '3-7 days',
                            'severity': 'moderate',
                            'location': 'whole body',
                            'pattern': 'continuous',
                            'onset_order': 1
                        },
                        ...
                    ]
                }
            
            patient_demographics: Patient information
                {
                    'age_group': 'adult',  # Or specific: 'child', 'elderly', etc.
                    'gender': 'male',
                    'medical_history': ['diabetes', 'hypertension'],
                    'medications': [],
                    'allergies': []
                }
            
            environmental_info: Environmental factors
                {
                    'location': 'tropical/urban/rural',
                    'factors': ['crowded living', 'poor sanitation']
                }
            
            negative_symptoms_input: Symptoms that are NOT present
                ['productive cough', 'rash']
        
        Returns:
            Structured prediction results with explanations
        """
        
        try:
            # Validate and convert inputs
            symptoms = symptoms_input.get('symptoms', [])
            
            # Create patient profile
            age_group = self._parse_age_group(patient_demographics.get('age_group'))
            gender = self._parse_gender(patient_demographics.get('gender'))
            
            patient = PatientProfile(
                age_group=age_group,
                gender=gender,
                medical_history=patient_demographics.get('medical_history', []),
                current_medications=patient_demographics.get('medications', []),
                allergies=patient_demographics.get('allergies', [])
            )
            
            # Parse environmental factors
            env_factors = environmental_info.get('factors', []) if environmental_info else []
            
            # Parse negative symptoms
            negative_symptoms = negative_symptoms_input or []
            
            # Extract onset order from symptoms
            onset_order = {}
            for symptom in symptoms:
                if 'onset_order' in symptom and symptom['onset_order']:
                    onset_order[symptom['name']] = symptom['onset_order']
            
            # Run prediction
            results = self.predictor.predict(
                symptoms=symptoms,
                patient_profile=patient,
                environmental_factors=env_factors,
                negative_symptoms=negative_symptoms,
                onset_order=onset_order if onset_order else None
            )
            
            # Format results
            return {
                'status': 'success',
                'predictions': [
                    {
                        'rank': rank + 1,
                        'disease_name': disease_name,
                        'probability_percent': probability,
                        'category': details['category'],
                        'confidence_level': self._get_confidence_level(probability),
                        'explanation': self.predictor.get_diagnosis_explanation(disease_name, details)
                    }
                    for rank, (disease_name, probability, details) in enumerate(results[:10])
                ],
                'summary': {
                    'top_diagnosis': results[0][0] if results else None,
                    'confidence': results[0][1] if results else 0,
                    'total_differentials': len(results),
                    'patient_info': patient.to_dict(),
                    'environmental_factors': env_factors
                }
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'error_type': type(e).__name__
            }
    
    def _parse_age_group(self, age_input: str) -> AgeGroup:
        """Parse age group from user input"""
        if isinstance(age_input, AgeGroup):
            return age_input
        
        age_mapping = {
            'infant': AgeGroup.INFANT,
            'toddler': AgeGroup.TODDLER,
            'child': AgeGroup.CHILD,
            'adolescent': AgeGroup.ADOLESCENT,
            'young adult': AgeGroup.YOUNG_ADULT,
            'adult': AgeGroup.ADULT,
            'middle-aged': AgeGroup.MIDDLE_AGED,
            'elderly': AgeGroup.ELDERLY,
        }
        
        age_lower = str(age_input).lower().strip()
        
        # Try exact match
        if age_lower in age_mapping:
            return age_mapping[age_lower]
        
        # Try partial match
        for key, value in age_mapping.items():
            if age_lower in key or key in age_lower:
                return value
        
        # Default
        return AgeGroup.ADULT
    
    def _parse_gender(self, gender_input: str):
        """Parse gender from user input"""
        if isinstance(gender_input, Gender):
            return gender_input
        
        gender_lower = str(gender_input).lower().strip()
        
        if 'male' in gender_lower:
            return Gender.MALE
        elif 'female' in gender_lower:
            return Gender.FEMALE
        else:
            return Gender.OTHER
    
    def _get_confidence_level(self, probability: float) -> str:
        """Get confidence level description"""
        if probability >= 70:
            return "High"
        elif probability >= 40:
            return "Moderate"
        elif probability >= 20:
            return "Low"
        else:
            return "Very Low"
    
    def generate_training_dataset(
        self,
        records_per_disease: int = 50,
        output_prefix: str = 'enhanced'
    ) -> Dict:
        """Generate training dataset for ML models"""
        
        generator = EnhancedDatasetGenerator()
        
        print("Generating enhanced dataset for ML training...")
        dataset = generator.generate_dataset(
            records_per_disease=records_per_disease,
            include_variations=True,
            output_file=f'{output_prefix}_medical_dataset.json'
        )
        
        return {
            'status': 'success',
            'total_records': len(dataset),
            'unique_diseases': len(set(r['disease_name'] for r in dataset)),
            'output_files': [
                f'{output_prefix}_medical_dataset.json',
                f'{output_prefix}_medical_dataset.csv'
            ],
            'summary': generator.generate_summary_report()
        }
    
    def get_disease_information(self, disease_name: str) -> Dict:
        """Get detailed information about a specific disease"""
        
        disease = self.predictor.disease_database.get(disease_name.lower())
        
        if not disease:
            return {
                'status': 'error',
                'message': f'Disease "{disease_name}" not found in database'
            }
        
        return {
            'status': 'success',
            'disease': disease.to_dict()
        }
    
    def calculate_symptom_timeline(
        self,
        symptoms: List[Dict]
    ) -> Dict:
        """Analyze symptom timeline and progression"""
        
        # Sort by onset order
        symptoms_sorted = sorted(
            symptoms,
            key=lambda x: x.get('onset_order', 999)
        )
        
        timeline = {
            'symptom_sequence': [s['name'] for s in symptoms_sorted if s.get('onset_order')],
            'total_symptoms': len(symptoms),
            'symptoms_by_onset': [
                {
                    'position': i + 1,
                    'symptom': s['name'],
                    'duration': s.get('duration', 'unknown'),
                    'severity': s.get('severity', 'unknown')
                }
                for i, s in enumerate(symptoms_sorted)
            ]
        }
        
        return timeline


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

def example_1_simple_prediction():
    """Example 1: Simple flu-like symptom prediction"""
    
    print("\n" + "="*70)
    print("EXAMPLE 1: Simple Flu-like Symptoms")
    print("="*70 + "\n")
    
    system = IntegratedDiseasePredictionSystem()
    
    symptoms_input = {
        'symptoms': [
            {
                'name': 'fever',
                'duration': '3-7 days',
                'severity': 'moderate',
                'location': 'whole body',
                'pattern': 'continuous',
                'onset_order': 1
            },
            {
                'name': 'cough',
                'duration': '1-2 weeks',
                'severity': 'moderate',
                'location': 'chest',
                'pattern': 'continuous',
                'onset_order': 2
            },
            {
                'name': 'muscle aches',
                'duration': '3-7 days',
                'severity': 'moderate',
                'location': 'full body',
                'onset_order': 1
            },
            {
                'name': 'headache',
                'duration': '3-7 days',
                'severity': 'moderate',
                'location': 'head',
                'onset_order': 1
            }
        ]
    }
    
    patient_info = {
        'age_group': 'adult',
        'gender': 'male',
        'medical_history': ['asthma'],
        'medications': ['albuterol inhaler'],
        'allergies': []
    }
    
    environmental_info = {
        'factors': ['crowded living', 'winter season']
    }
    
    negative_symptoms = ['loss of taste', 'loss of smell', 'severe abdominal pain']
    
    results = system.predict_from_user_input(
        symptoms_input=symptoms_input,
        patient_demographics=patient_info,
        environmental_info=environmental_info,
        negative_symptoms_input=negative_symptoms
    )
    
    print("RESULTS:")
    print(json.dumps(results, indent=2))
    
    return results


def example_2_complex_prediction():
    """Example 2: Complex prediction with detailed patient profile"""
    
    print("\n" + "="*70)
    print("EXAMPLE 2: Complex Prediction with Detailed Profile")
    print("="*70 + "\n")
    
    system = IntegratedDiseasePredictionSystem()
    
    # Dengue-like presentation
    symptoms_input = {
        'symptoms': [
            {
                'name': 'fever',
                'duration': '3-7 days',
                'severity': 'severe',
                'location': 'whole body',
                'pattern': 'intermittent',
                'onset_order': 1
            },
            {
                'name': 'joint pain',
                'duration': '3-7 days',
                'severity': 'severe',
                'location': 'joints',
                'pattern': 'continuous',
                'onset_order': 1
            },
            {
                'name': 'muscle aches',
                'duration': '3-7 days',
                'severity': 'severe',
                'location': 'full body',
                'onset_order': 1
            },
            {
                'name': 'headache',
                'duration': '3-7 days',
                'severity': 'severe',
                'location': 'behind eyes',
                'pattern': 'continuous',
                'onset_order': 1
            },
            {
                'name': 'rash',
                'duration': '1-2 weeks',
                'severity': 'moderate',
                'location': 'trunk/limbs',
                'pattern': 'progressive',
                'onset_order': 4
            }
        ]
    }
    
    patient_info = {
        'age_group': 'young adult',
        'gender': 'female',
        'medical_history': [],
        'medications': [],
        'allergies': ['penicillin']
    }
    
    environmental_info = {
        'factors': ['tropical climate', 'mosquito-prone', 'monsoon season']
    }
    
    negative_symptoms = ['cough', 'sore throat', 'runny nose']
    
    results = system.predict_from_user_input(
        symptoms_input=symptoms_input,
        patient_demographics=patient_info,
        environmental_info=environmental_info,
        negative_symptoms_input=negative_symptoms
    )
    
    print("RESULTS:")
    if results['status'] == 'success':
        for prediction in results['predictions'][:5]:
            print(f"\n{prediction['rank']}. {prediction['disease_name'].upper()}")
            print(f"   Probability: {prediction['probability_percent']:.1f}%")
            print(f"   Confidence: {prediction['confidence_level']}")
            print(f"   Category: {prediction['category']}")
    
    return results


def example_3_generate_dataset():
    """Example 3: Generate training dataset"""
    
    print("\n" + "="*70)
    print("EXAMPLE 3: Generate Enhanced Training Dataset")
    print("="*70 + "\n")
    
    system = IntegratedDiseasePredictionSystem()
    
    result = system.generate_training_dataset(
        records_per_disease=30,
        output_prefix='example_enhanced'
    )
    
    print(result['summary'])
    print(f"\nDataset generation result: {result['status']}")
    print(f"Total records: {result['total_records']}")
    print(f"Unique diseases: {result['unique_diseases']}")


if __name__ == "__main__":
    # Run examples
    example_1_simple_prediction()
    example_2_complex_prediction()
    # example_3_generate_dataset()  # Uncomment to generate dataset

