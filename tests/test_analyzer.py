"""
Test and Demo Script for Enhanced Disease Analyzer
Run this to test the disease prediction system with various symptom patterns.
"""

from backend.disease_analyzer import create_analyzer, DISEASE_DATABASE


def print_separator(title: str = ""):
    """Print a formatted separator."""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'-'*70}\n")


def test_disease_analyzer():
    """Run comprehensive tests of the disease analyzer."""
    
    analyzer = create_analyzer()
    
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "DISEASE PREDICTION SYSTEM - TEST SUITE" + " "*16 + "║")
    print("╚" + "="*68 + "╝")
    
    # Test 1: Classic Flu Symptoms
    print_separator("TEST 1: Classic Influenza Pattern")
    test_case_1 = ["fever", "cough", "sore throat", "headache", "muscle body aches", "fatigue or weakness"]
    print(f"Input Symptoms: {', '.join(test_case_1)}")
    predictions, confidence_note = analyzer.analyze_symptoms(test_case_1)
    
    if predictions:
        for pred in predictions:
            print(f"\n🔹 Rank #{pred['rank']}: {pred['disease']}")
            print(f"   Category: {pred['category']}")
            print(f"   Confidence: {pred['confidence']}%")
            print(f"   Severity: {pred['severity']}")
            print(f"   Matched Symptoms: {', '.join(pred['matched_symptoms'])}")
            print(f"   Medical Reasoning: {pred['medical_reasoning'][:100]}...")
    
    print(f"\nConfidence Assessment: {confidence_note}")
    print(f"Urgency Level: {analyzer.suggest_medical_attention(predictions)}")
    
    # Test 2: Vector-Borne Disease (Dengue)
    print_separator("TEST 2: Dengue/Breakbone Fever Pattern")
    test_case_2 = ["fever", "joint pain", "headache", "rash", "muscle body aches"]
    print(f"Input Symptoms: {', '.join(test_case_2)}")
    predictions, confidence_note = analyzer.analyze_symptoms(test_case_2)
    
    if predictions:
        for pred in predictions[:2]:  # Show top 2
            print(f"\n🔹 Rank #{pred['rank']}: {pred['disease']}")
            print(f"   Confidence: {pred['confidence']}%")
            print(f"   Recommendations: {pred['recommendations'][:80]}...")
    
    print(f"\nConfidence Assessment: {confidence_note}")
    
    # Test 3: Cardiac Emergency
    print_separator("TEST 3: Cardiac Emergency Pattern")
    test_case_3 = ["chest pain", "shortness of breath", "fatigue or weakness"]
    print(f"Input Symptoms: {', '.join(test_case_3)}")
    predictions, confidence_note = analyzer.analyze_symptoms(test_case_3)
    
    if predictions:
        top_pred = predictions[0]
        print(f"\n🔹 Primary Prediction: {top_pred['disease']}")
        print(f"   Confidence: {top_pred['confidence']}%")
        print(f"   Severity: {top_pred['severity']}")
        print(f"   Medical Analysis:\n   {top_pred['medical_reasoning']}")
    
    urgency = analyzer.suggest_medical_attention(predictions)
    print(f"\n⚠️  URGENCY: {urgency}")
    
    # Test 4: Insufficient Symptoms (Should fail gracefully)
    print_separator("TEST 4: Insufficient Symptoms (Edge Case)")
    test_case_4 = ["cough"]
    print(f"Input Symptoms: {', '.join(test_case_4)}")
    predictions, error_msg = analyzer.analyze_symptoms(test_case_4)
    
    if not predictions and error_msg:
        print(f"\n✓ Correctly detected insufficient input")
        print(f"System Response: {error_msg}")
    
    # Test 5: Gastrointestinal Symptoms
    print_separator("TEST 5: Digestive System - Food Poisoning vs Gastroenteritis")
    test_case_5 = ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever"]
    print(f"Input Symptoms: {', '.join(test_case_5)}")
    predictions, confidence_note = analyzer.analyze_symptoms(test_case_5)
    
    if predictions:
        for pred in predictions[:2]:
            print(f"\n🔹 {pred['disease']} (Confidence: {pred['confidence']}%)")
            print(f"   Matched: {', '.join(pred['matched_symptoms'])}")
            print(f"   Supporting: {', '.join(pred['unmatched_primary'][:3])} (if present)")
    
    # Test 6: Respiratory Infection
    print_separator("TEST 6: Respiratory Infection - Common Cold vs COVID-19")
    test_case_6 = ["runny nose", "sore throat", "cough", "fatigue or weakness"]
    print(f"Input Symptoms: {', '.join(test_case_6)}")
    predictions, confidence_note = analyzer.analyze_symptoms(test_case_6)
    
    if predictions:
        for pred in predictions:
            print(f"\n🔹 {pred['disease']} ({pred['category']})")
            print(f"   Confidence: {pred['confidence']}%")
            print(f"   Severity: {pred['severity']}")
    
    # Test 7: Neurological - Anxiety vs Cardiac
    print_separator("TEST 7: Cardiac vs Anxiety - Chest Pain Differential")
    test_case_7 = ["chest pain", "anxiety", "sweating", "palpitations"]
    print(f"Input Symptoms: {', '.join(test_case_7)}")
    predictions, confidence_note = analyzer.analyze_symptoms(test_case_7)
    
    if predictions:
        print("\nNote: Both conditions can present similarly - medical evaluation crucial for differentiation")
        for pred in predictions[:2]:
            print(f"\n🔹 {pred['disease']}")
            print(f"   Confidence: {pred['confidence']}%")
            print(f"   Key Distinguisher: {pred['medical_reasoning'][:100]}...")
    
    # Test 8: Vector-Borne Database Check
    print_separator("TEST 8: Database Summary - Available Diseases by Category")
    
    categories = {}
    for disease_name, disease in DISEASE_DATABASE.items():
        cat = disease.category.value
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(disease.name)
    
    for category in sorted(categories.keys()):
        diseases = categories[category]
        print(f"\n{category} ({len(diseases)} diseases):")
        for disease in diseases:
            print(f"  • {disease}")
    
    print(f"\n{'='*70}")
    print(f"Total Diseases in Database: {analyzer.total_diseases}")
    print(f"{'='*70}\n")


def test_symptom_matching():
    """Test symptom normalization and matching."""
    
    print_separator("Symptom Normalization & Matching Examples")
    
    analyzer = create_analyzer()
    
    # Test different input formats for the same symptoms
    test_inputs = [
        ["fever", "cough"],
        ["high temperature", "persistent cough"],  
        ["99.5 f", "dry cough"],
        ["fever, cough"],  # This would be cleaned once
    ]
    
    print("Testing how system handles various input formats:\n")
    
    for i, symptoms in enumerate(test_inputs[:2]):  # Skip already-joined ones
        print(f"Input Format {i+1}: {symptoms}")
        predictions, _ = analyzer.analyze_symptoms(symptoms)
        if predictions:
            print(f"  → Top Match: {predictions[0]['disease']} ({predictions[0]['confidence']}%)\n")


def test_edge_cases():
    """Test edge cases and error handling."""
    
    print_separator("Edge Case Testing")
    
    analyzer = create_analyzer()
    
    test_cases = [
        ([], "Empty input"),
        (["xyz"], "Non-medical symptom"),
        (["fever"], "Single symptom"),
        (["fever", "cough", "shortness of breath", "chest pain"], "Multiple valid symptoms"),
    ]
    
    for symptoms, description in test_cases:
        print(f"\nTest: {description}")
        print(f"Input: {symptoms if symptoms else 'EMPTY'}")
        predictions, msg = analyzer.analyze_symptoms(symptoms)
        
        if predictions:
            print(f"✓ Prediction: {predictions[0]['disease']}")
        else:
            print(f"✗ Message: {msg}")


def interactive_test():
    """Interactive testing mode - enter symptoms and get predictions."""
    
    print_separator("INTERACTIVE TEST MODE")
    print("Enter symptoms (comma-separated) and get predictions.")
    print("Type 'quit' to exit.\n")
    
    analyzer = create_analyzer()
    
    while True:
        user_input = input("\nEnter symptoms: ").strip()
        
        if user_input.lower() == 'quit':
            print("Exiting interactive mode...")
            break
        
        if not user_input:
            print("Please enter at least one symptom.")
            continue
        
        # Parse symptoms
        symptoms = [s.strip() for s in user_input.split(',') if s.strip()]
        
        print(f"\nAnalyzing {len(symptoms)} symptom(s)...")
        predictions, confidence_note = analyzer.analyze_symptoms(symptoms)
        
        if not predictions:
            print(f"❌ {confidence_note}")
        else:
            print(f"\n{'✓ PREDICTIONS':^70}")
            print(f"{'-'*70}")
            
            for pred in predictions:
                print(f"\n#{pred['rank']}: {pred['disease']} ({pred['severity']})")
                print(f"    Confidence: {pred['confidence']}% | Category: {pred['category']}")
                print(f"    Matched: {', '.join(pred['matched_symptoms'][:5])}")
                print(f"    Reason: {pred['medical_reasoning'][:100]}...")
            
            print(f"\n📊 Confidence Note: {confidence_note}")
            print(f"📋 Urgency: {analyzer.suggest_medical_attention(predictions)}")


if __name__ == "__main__":
    import sys
    
    print("\n")
    print("        🏥 ENHANCED DISEASE PREDICTION SYSTEM - TEST SUITE 🏥")
    print("        " + "="*60)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_test()
    elif len(sys.argv) > 1 and sys.argv[1] == "--edge-cases":
        test_edge_cases()
    elif len(sys.argv) > 1 and sys.argv[1] == "--symptoms":
        test_symptom_matching()
    else:
        test_disease_analyzer()
        print("\n💡 Tips:")
        print("  • Run with --interactive for interactive testing")
        print("  • Run with --edge-cases to test error handling")
        print("  • Run with --symptoms to test symptom normalization")
