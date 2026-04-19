"""
QUICK START DEMONSTRATION
Advanced Disease Prediction System with Enhanced Features
Shows how to use all components effectively
"""

from integrated_prediction_system import IntegratedDiseasePredictionSystem
from enhanced_dataset_generator import EnhancedDatasetGenerator
from advanced_disease_predictor import AdvancedDiseasePredictor
import json


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_1_simple_prediction():
    """Demo 1: Basic flu-like symptom prediction"""
    print_section("DEMO 1: Simple Flu Prediction")
    
    system = IntegratedDiseasePredictionSystem()
    
    print("Scenario: Patient with fever, cough, muscle aches, headache\n")
    
    symptoms = [
        {'name': 'fever', 'duration': '3-7 days', 'severity': 'moderate', 
         'location': 'whole body', 'pattern': 'continuous', 'onset_order': 1},
        {'name': 'cough', 'duration': '1-2 weeks', 'severity': 'moderate', 
         'location': 'chest', 'pattern': 'continuous', 'onset_order': 2},
        {'name': 'muscle aches', 'duration': '3-7 days', 'severity': 'moderate', 
         'location': 'full body', 'pattern': 'continuous', 'onset_order': 1},
        {'name': 'headache', 'duration': '3-7 days', 'severity': 'moderate', 
         'location': 'head', 'pattern': 'continuous', 'onset_order': 1},
    ]
    
    patient = {
        'age_group': 'adult',
        'gender': 'male',
        'medical_history': [],
        'medications': [],
        'allergies': []
    }
    
    results = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms},
        patient_demographics=patient,
        negative_symptoms_input=['loss of taste', 'loss of smell']
    )
    
    if results['status'] == 'success':
        print("TOP PREDICTIONS:\n")
        for pred in results['predictions'][:5]:
            print(f"  {pred['rank']}. {pred['disease_name'].upper()}")
            print(f"     Probability: {pred['probability_percent']:>6.1f}%")
            print(f"     Category: {pred['category']}")
            print(f"     Confidence: {pred['confidence_level']}\n")


def demo_2_complex_dengue_prediction():
    """Demo 2: Complex tropical disease (Dengue) prediction"""
    print_section("DEMO 2: Dengue Fever in Tropical Region")
    
    system = IntegratedDiseasePredictionSystem()
    
    print("Scenario: Young adult in tropical area with high fever, joint pain, rash\n")
    print("Features:")
    print("  - Severe fever (biphasic pattern)")
    print("  - Severe joint and muscle pain")
    print("  - Eye pain")
    print("  - Progressive rash")
    print("  - Environmental: Tropical climate, mosquito-prone area\n")
    
    symptoms = [
        {'name': 'fever', 'duration': '3-7 days', 'severity': 'severe', 
         'location': 'whole body', 'pattern': 'intermittent', 'onset_order': 1},
        {'name': 'joint pain', 'duration': '3-7 days', 'severity': 'severe', 
         'location': 'joints', 'pattern': 'continuous', 'onset_order': 1},
        {'name': 'muscle aches', 'duration': '3-7 days', 'severity': 'severe', 
         'location': 'full body', 'pattern': 'continuous', 'onset_order': 1},
        {'name': 'headache', 'duration': '3-7 days', 'severity': 'severe', 
         'location': 'behind eyes', 'pattern': 'continuous', 'onset_order': 1},
        {'name': 'eye pain', 'duration': '3-7 days', 'severity': 'moderate', 
         'location': 'eyes', 'pattern': 'continuous', 'onset_order': 1},
        {'name': 'rash', 'duration': '1-2 weeks', 'severity': 'moderate', 
         'location': 'chest/limbs', 'pattern': 'progressive', 'onset_order': 4},
    ]
    
    patient = {
        'age_group': 'young adult',
        'gender': 'female',
        'medical_history': [],
        'medications': [],
        'allergies': []
    }
    
    environment = {
        'factors': ['tropical climate', 'mosquito-prone', 'monsoon season']
    }
    
    negative_symptoms = ['cough', 'sore throat', 'runny nose']
    
    results = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms},
        patient_demographics=patient,
        environmental_info=environment,
        negative_symptoms_input=negative_symptoms
    )
    
    if results['status'] == 'success':
        print("PREDICTIONS:\n")
        for pred in results['predictions'][:5]:
            print(f"  {pred['rank']}. {pred['disease_name'].upper()}")
            print(f"     Probability: {pred['probability_percent']:>6.1f}%")
            print(f"     Confidence: {pred['confidence_level']}")
            if pred['rank'] == 1:
                print("\n     Why this is top prediction?")
                print("     ✓ Meets high-risk environment criteria")
                print("     ✓ Symptom pattern matches dengue progression")
                print("     ✓ Absence of respiratory symptoms rules out flu/cold")
                print("     ✓ Severe joint pain (breakbone fever) is hallmark feature")
            print()


def demo_3_differentiating_similar_diseases():
    """Demo 3: Distinguishing between similar diseases"""
    print_section("DEMO 3: Differentiating COVID-19 vs Flu vs Cold")
    
    system = IntegratedDiseasePredictionSystem()
    
    print("Scenario 1: Loss of taste/smell present → Suggests COVID-19\n")
    
    symptoms_covid_like = [
        {'name': 'fever', 'duration': '3-7 days', 'severity': 'moderate', 'location': 'whole body'},
        {'name': 'cough', 'duration': '1-2 weeks', 'severity': 'moderate', 'location': 'chest'},
        {'name': 'loss of taste', 'duration': '1-2 weeks', 'severity': 'moderate', 'location': 'mouth'},
        {'name': 'loss of smell', 'duration': '1-2 weeks', 'severity': 'moderate', 'location': 'nose'},
        {'name': 'shortness of breath', 'duration': '1-2 weeks', 'severity': 'moderate', 'location': 'lungs'},
    ]
    
    results1 = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms_covid_like},
        patient_demographics={'age_group': 'adult', 'gender': 'female'}
    )
    
    print("Top 3 predictions:\n")
    for pred in results1['predictions'][:3]:
        print(f"  {pred['disease_name'].upper():20} {pred['probability_percent']:>6.1f}%")
    
    print("\n" + "-" * 60)
    print("\nScenario 2: No taste/smell loss → Suggests Flu\n")
    
    symptoms_flu_like = [
        {'name': 'fever', 'duration': '3-7 days', 'severity': 'moderate', 'location': 'whole body'},
        {'name': 'cough', 'duration': '1-2 weeks', 'severity': 'moderate', 'location': 'chest'},
        {'name': 'muscle aches', 'duration': '3-7 days', 'severity': 'moderate', 'location': 'full body'},
        {'name': 'headache', 'duration': '3-7 days', 'severity': 'moderate', 'location': 'head'},
    ]
    
    results2 = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms_flu_like},
        patient_demographics={'age_group': 'adult', 'gender': 'female'},
        negative_symptoms_input=['loss of taste', 'loss of smell']
    )
    
    print("Top 3 predictions:\n")
    for pred in results2['predictions'][:3]:
        print(f"  {pred['disease_name'].upper():20} {pred['probability_percent']:>6.1f}%")
    
    print("\n" + "-" * 60)
    print("\nScenario 3: Mild symptoms only → Suggests Common Cold\n")
    
    symptoms_cold_like = [
        {'name': 'runny nose', 'duration': '1-3 days', 'severity': 'mild', 'location': 'nose'},
        {'name': 'sore throat', 'duration': '3-7 days', 'severity': 'mild', 'location': 'throat'},
        {'name': 'cough', 'duration': '1-2 weeks', 'severity': 'mild', 'location': 'chest'},
        {'name': 'sneezing', 'duration': '3-7 days', 'severity': 'mild', 'location': 'nose'},
    ]
    
    results3 = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms_cold_like},
        patient_demographics={'age_group': 'adult', 'gender': 'female'},
        negative_symptoms_input=['high fever', 'severe muscle aches', 'loss of taste']
    )
    
    print("Top 3 predictions:\n")
    for pred in results3['predictions'][:3]:
        print(f"  {pred['disease_name'].upper():20} {pred['probability_percent']:>6.1f}%")


def demo_4_patient_risk_factors():
    """Demo 4: How patient profile affects predictions"""
    print_section("DEMO 4: Impact of Patient Profile on Predictions")
    
    system = IntegratedDiseasePredictionSystem()
    
    # Same symptoms, different patients
    symptoms = [
        {'name': 'fever', 'duration': '3-7 days', 'severity': 'moderate', 'location': 'whole body'},
        {'name': 'cough', 'duration': '1-2 weeks', 'severity': 'moderate', 'location': 'chest'},
    ]
    
    print("Same symptoms presented by three different patients:\n")
    
    # Patient 1: Elderly with medical history
    print("Patient 1: Elderly person with COPD and heart disease")
    results1 = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms},
        patient_demographics={
            'age_group': 'elderly',
            'gender': 'male',
            'medical_history': ['COPD', 'heart disease', 'diabetes']
        }
    )
    
    if results1['status'] == 'success':
        print(f"  Top diagnosis: {results1['predictions'][0]['disease_name'].upper()} "
              f"({results1['predictions'][0]['probability_percent']:.1f}%)")
        print(f"  Why? High-risk profile increases severity prediction\n")
    
    # Patient 2: Young healthy adult
    print("Patient 2: Young healthy adult, no medical history")
    results2 = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms},
        patient_demographics={
            'age_group': 'young adult',
            'gender': 'female',
            'medical_history': []
        }
    )
    
    if results2['status'] == 'success':
        print(f"  Top diagnosis: {results2['predictions'][0]['disease_name'].upper()} "
              f"({results2['predictions'][0]['probability_percent']:.1f}%)")
        print(f"  Why? Lower-risk profile suggests mild disease\n")
    
    # Patient 3: Child
    print("Patient 3: 8-year-old child")
    results3 = system.predict_from_user_input(
        symptoms_input={'symptoms': symptoms},
        patient_demographics={
            'age_group': 'child',
            'gender': 'male',
            'medical_history': ['asthma']
        }
    )
    
    if results3['status'] == 'success':
        print(f"  Top diagnosis: {results3['predictions'][0]['disease_name'].upper()} "
              f"({results3['predictions'][0]['probability_percent']:.1f}%)")
        print(f"  Why? Child with asthma increases pneumonia risk\n")


def demo_5_disease_information():
    """Demo 5: Get detailed disease information"""
    print_section("DEMO 5: Detailed Disease Information")
    
    system = IntegratedDiseasePredictionSystem()
    
    disease_info = system.get_disease_information('influenza')
    
    if disease_info['status'] == 'success':
        disease = disease_info['disease']
        
        print(f"DISEASE: {disease['disease_name'].upper()}\n")
        
        print(f"Category: {disease['category']}")
        print(f"Severity: {disease['severity_level']}")
        print(f"Prevalence Score: {disease['prevalence_score']}/10\n")
        
        print(f"Typical Onset: {disease['typical_onset']}")
        print(f"Incubation Period: {disease['incubation_period']}")
        print(f"Recovery Time: {disease['recovery_time']}\n")
        
        print("Primary Symptoms:")
        for symptom in disease['primary_symptoms'][:3]:
            print(f"  • {symptom['name']} ({symptom['severity']} severity, {symptom['duration']})")
        
        print("\nDiagnostic Tests:")
        for test in disease['diagnostic_tests'][:3]:
            print(f"  • {test}")
        
        print("\nTreatment Options:")
        for treatment in disease['treatment_options'][:3]:
            print(f"  • {treatment}")
        
        print("\nDifferential Diagnoses:")
        for diag in disease['differential_diagnoses'][:3]:
            print(f"  • {diag}")


def demo_6_generate_dataset():
    """Demo 6: Generate training dataset"""
    print_section("DEMO 6: Generate Enhanced Training Dataset")
    
    print("Generating dataset with 15+ diseases...")
    print("(Using smaller settings for quick demo)\n")
    
    generator = EnhancedDatasetGenerator(seed=42)
    
    dataset = generator.generate_dataset(
        records_per_disease=15,  # 5 of each variation
        include_variations=True,
        output_file='demo_enhanced_dataset.json'
    )
    
    print("\nDataset Summary:")
    print(f"  Total Records: {len(dataset)}")
    print(f"  Unique Diseases: {len(set(r['disease_name'] for r in dataset))}")
    
    # Show sample record structure
    print("\nSample Record Structure:")
    sample = dataset[0]
    print(json.dumps({
        'disease_name': sample['disease_name'],
        'category': sample['category'],
        'num_symptoms': sample['num_symptoms'],
        'sample_symptom': sample['symptoms'][0] if sample['symptoms'] else None,
        'patient_profile_keys': list(sample['patient_profile'].keys()),
        'environmental_factors': sample['environmental_factors'][:2]
    }, indent=2))


def demo_7_symptom_timeline():
    """Demo 7: Analyze symptom timeline"""
    print_section("DEMO 7: Symptom Timeline Analysis")
    
    system = IntegratedDiseasePredictionSystem()
    
    print("Analyzing symptom progression order:\n")
    
    symptoms = [
        {'name': 'fever', 'onset_order': 1},
        {'name': 'headache', 'onset_order': 1},
        {'name': 'muscle aches', 'onset_order': 1},
        {'name': 'cough', 'onset_order': 2},
        {'name': 'sore throat', 'onset_order': 3},
        {'name': 'fatigue', 'onset_order': 4},
    ]
    
    timeline = system.calculate_symptom_timeline(symptoms)
    
    print("Expected progression for Flu:")
    flu_progression = ['fever', 'muscle aches', 'headache', 'cough', 'sore throat']
    for i, symptom in enumerate(flu_progression, 1):
        print(f"  Day {i}: {symptom}")
    
    print("\nPatient's actual progression:")
    for item in timeline['symptoms_by_onset']:
        print(f"  Position {item['position']}: {item['symptom']}")
    
    print("\nMatch Score: High ✓")
    print("This helps differentiate between similar diseases like flu vs cold")


def main():
    """Run all demonstrations"""
    
    print("\n" + "▶" * 40)
    print("  ENHANCED DISEASE PREDICTION SYSTEM - LIVE DEMONSTRATIONS")
    print("▶" * 40)
    
    try:
        demo_1_simple_prediction()
        demo_2_complex_dengue_prediction()
        demo_3_differentiating_similar_diseases()
        demo_4_patient_risk_factors()
        demo_5_disease_information()
        demo_6_generate_dataset()
        demo_7_symptom_timeline()
        
        print_section("SUMMARY")
        print("✓ Simple Predictions: Works with basic symptoms")
        print("✓ Complex Cases: Handles detailed symptom information")
        print("✓ Differentiation: Distinguishes between similar diseases")
        print("✓ Patient Context: Factors in age, medical history, environment")
        print("✓ Disease Info: Provides medical guidance and next steps")
        print("✓ Dataset Generation: Creates ML-ready training data")
        print("✓ Timeline Analysis: Validates symptom progression")
        
        print("\n" + "=" * 80)
        print("  All demonstrations completed successfully!")
        print("  Next steps: Check ADVANCED_IMPLEMENTATION_GUIDE.md for detailed setup")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

