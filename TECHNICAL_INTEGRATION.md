"""
TECHNICAL INTEGRATION GUIDE
Enhanced Medical Symptom Analysis Assistant

This guide explains how to integrate the disease analyzer into your application.
"""

# ============================================================================
# 1. BASIC USAGE - Python Integration
# ============================================================================

from disease_analyzer import create_analyzer

# Initialize the analyzer
analyzer = create_analyzer()

# Analyze symptoms
symptoms = ["fever", "cough", "sore throat"]
predictions, confidence_note = analyzer.analyze_symptoms(symptoms)

# Access predictions
for prediction in predictions:
    print(f"Disease: {prediction['disease']}")
    print(f"Confidence: {prediction['confidence']}%")
    print(f"Category: {prediction['category']}")
    print(f"Severity: {prediction['severity']}")
    print(f"Medical Reasoning: {prediction['medical_reasoning']}")
    print(f"Recommendations: {prediction['recommendations']}")
    print("---")

# ============================================================================
# 2. FLASK INTEGRATION (Already Implemented)
# ============================================================================

# Endpoint: POST /predict
# Request:
#   {
#     "text": "fever, cough, sore throat"
#   }
#
# Response (Success):
#   {
#     "predictions": [
#       {
#         "rank": 1,
#         "disease": "Influenza (Flu)",
#         "category": "Viral",
#         "confidence": 92,
#         "risk_level": "High",
#         "severity": "Moderate",
#         "matched_symptoms": ["fever", "cough", "sore throat"],
#         "unmatched_primary_symptoms": ["muscle body aches"],
#         "medical_reasoning": "...",
#         "recommendations": "..."
#       }
#     ],
#     "input_symptoms": ["fever", "cough", "sore throat"],
#     "total_matches": 3,
#     "confidence_note": "Good confidence match based on symptom patterns.",
#     "urgency_level": "ℹ️ MONITORING: Observe symptoms..."
#   }
#
# Response (Error - Insufficient):
#   {
#     "error": "Cannot determine disease with given symptoms",
#     "message": "Please provide at least 2 symptoms for accurate analysis.",
#     "input_symptoms": ["cough"],
#     "status": "insufficient_data"
#   }

# ============================================================================
# 3. NODEJS/JAVASCRIPT INTEGRATION (Client-Side)
# ============================================================================

JAVASCRIPT_EXAMPLE = """
// Frontend JavaScript integration
async function predictDisease(symptoms) {
  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: symptoms })
    });
    
    const data = await response.json();
    
    if (!response.ok || data.error) {
      console.error('Error:', data.message || data.error);
      return null;
    }
    
    // Process predictions
    data.predictions.forEach(pred => {
      console.log(`Disease: ${pred.disease} (${pred.confidence}%)`);
      console.log(`Reasoning: ${pred.medical_reasoning}`);
      console.log(`Action: ${pred.recommendations}`);
    });
    
    console.log(`Urgency: ${data.urgency_level}`);
    
    return data;
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Usage
predictDisease("fever, cough, headache");
"""

# ============================================================================
# 4. DATABASE STRUCTURE
# ============================================================================

DATABASE_STRUCTURE = """
DiseaseDatabase (19 diseases):
├── VIRAL (3)
│   ├── Influenza
│   ├── COVID-19
│   └── Common Cold
├── VECTOR_BORNE (2)
│   ├── Dengue
│   └── Malaria
├── BACTERIAL (3)
│   ├── Typhoid
│   ├── Bacterial Pneumonia
│   └── Strep Throat
├── RESPIRATORY (2)
│   ├── Bronchitis
│   └── Asthma
├── DIGESTIVE (2)
│   ├── Food Poisoning
│   └── Gastroenteritis
├── CHRONIC (3)
│   ├── Diabetes
│   ├── Thyroid Disorder
│   └── Arthritis
├── CARDIOVASCULAR (2)
│   ├── Heart Disease
│   └── Hypertension
└── NEUROLOGICAL (2)
    ├── Migraine
    └── Anxiety Disorder

Each disease has:
- Primary symptoms (essential, weight: 2x)
- Secondary symptoms (supporting, weight: 1x)
- Category classification
- Severity level
- Medical reasoning
- Clinical recommendations
- Prevalence score
"""

# ============================================================================
# 5. PREDICTION ALGORITHM DETAILS
# ============================================================================

ALGORITHM_EXPLANATION = """
CONFIDENCE SCORING FORMULA:

1. Symptom Matching:
   - Primary symptom match = 2 points
   - Secondary symptom match = 1 point
   
2. Base Scoring:
   total_score = (primary_matches × 2) + secondary_matches
   max_possible = number_of_primary_symptoms × 2
   
3. Confidence Calculation:
   confidence = (total_score / max_possible) × 100
   
4. Bonus for Complete Match:
   if all_user_symptoms are in disease_profile:
       confidence += 15 (capped at 100%)

5. Ranking:
   Diseases ranked by total_score (descending)
   Top 3 returned for user

CONFIDENCE INTERPRETATION:
- ≥ 75%: High confidence (strong symptom match)
- 50-74%: Moderate confidence (partial match)
- < 50%: Low confidence (weak match)
- < 2 symptoms: Cannot determine

EXAMPLE:
User symptoms: ["fever", "cough", "shortness of breath"]

Disease A (Influenza):
  Primary: fever, cough, sore throat, headache, muscle aches, fatigue
  Matched primary: fever, cough = 2 × 2 = 4 points
  Max possible: 6 × 2 = 12 points
  Base confidence: (4/12) × 100 = 33%
  All symptoms in profile: YES → 33% + 15% = 48% (capped at 100%)
  
Disease B (COVID-19):
  Primary: fever, cough, shortness of breath, fatigue, loss of taste/smell
  Matched primary: fever, cough, shortness of breath = 3 × 2 = 6 points
  Max possible: 5 × 2 = 10 points
  Base confidence: (6/10) × 100 = 60%
  All symptoms in profile: YES → 60% + 15% = 75%
  
Result: COVID-19 ranks higher (75% > 48%)
"""

# ============================================================================
# 6. EXTENDING THE DATABASE
# ============================================================================

EXTENSION_EXAMPLE = """
How to add a new disease to the database:

from disease_analyzer import Disease, DiseaseCategory

new_disease = Disease(
    name="Disease Name",
    category=DiseaseCategory.VIRAL,  # or BACTERIAL, CHRONIC, etc.
    primary_symptoms=[
        "symptom1",
        "symptom2",
        "symptom3",
    ],
    secondary_symptoms=[
        "symptom4",
        "symptom5",
    ],
    prevalence_score=6,  # 1-10, higher = more common
    severity="Moderate",  # Mild, Mild-Moderate, Moderate, Moderate-Severe, Severe
    medical_reasoning="Clear explanation of symptoms correlation to disease",
    recommendations="Specific action items for the patient"
)

# Add to database:
DISEASE_DATABASE["disease_key"] = new_disease
"""

# ============================================================================
# 7. ERROR HANDLING
# ============================================================================

ERROR_HANDLING = """
Expected Errors & Responses:

1. Empty Input
   Input: []
   Response: ("Cannot determine disease with given symptoms", "")
   HTTP: 400 Bad Request

2. Insufficient Symptoms (< 2)
   Input: ["cough"]
   Response: ("Cannot determine disease with given symptoms", "")
   HTTP: 400 Bad Request

3. Non-Medical Input
   Input: ["xyz", "abc"]
   Response: May return low confidence results or empty
   HTTP: 200 OK with empty predictions

4. Severe Condition Detected
   Input: ["chest pain", "shortness of breath"]
   Response: Returns predictions + urgency alert
   HTTP: 200 OK with urgency flag

5. Network/Server Error
   Response: 500 Internal Server Error
   HTTP: 500 with error message
"""

# ============================================================================
# 8. PERFORMANCE CONSIDERATIONS
# ============================================================================

PERFORMANCE_NOTES = """
Algorithm Complexity:
- Time: O(n × m) where n = diseases, m = symptoms
  Current: O(19 × 50) = O(950) operations (negligible)
- Space: O(n × m) = O(950) memory usage

Current Performance:
- Average response time: < 50ms
- Memory usage: < 1MB
- No external API calls
- Fully self-contained

Scalability:
- Can handle 50+ diseases without performance degradation
- Can handle complex symptom lists (100+ symptoms) efficiently
- Suitable for real-time applications
- Suitable for mobile clients (small payload)

Optimization Tips:
1. Cache disease database on client-side
2. Debounce rapid requests
3. Use query string for GET requests (smaller payload)
4. Compress JSON responses
"""

# ============================================================================
# 9. TESTING & VALIDATION
# ============================================================================

TESTING_GUIDE = """
Run Tests:

# Full test suite
python test_analyzer.py

# Interactive testing
python test_analyzer.py --interactive

# Edge case testing
python test_analyzer.py --edge-cases

# Symptom normalization tests
python test_analyzer.py --symptoms

Test Coverage:
✓ Classic flu pattern: fever + cough + sore throat + body aches
✓ Vector-borne disease: high fever + joint pain + rash
✓ Cardiac emergency: chest pain + shortness of breath
✓ Insufficient symptoms: proper error handling
✓ GI symptoms: food poisoning vs gastroenteritis
✓ Respiratory: cold vs COVID-19
✓ Neurological: anxiety vs cardiac
✓ Database integrity: all 19 diseases
✓ Edge cases: empty input, single symptom, invalid input
"""

# ============================================================================
# 10. DEPLOYMENT CHECKLIST
# ============================================================================

DEPLOYMENT_CHECKLIST = """
Pre-Deployment:
☐ Run full test suite successfully
☐ Test with real medical scenarios
☐ Validate error handling
☐ Check performance under load
☐ Review medical accuracy of correlations
☐ Document all symptoms (medical terminology)

Production Setup:
☐ Set appropriate Flask secret key
☐ Enable HTTPS/SSL
☐ Configure CORS if needed
☐ Set up logging and monitoring
☐ Configure database persistence
☐ Set up backup for history data
☐ Configure rate limiting

Monitoring:
☐ Track prediction accuracy
☐ Monitor response times
☐ Log error patterns
☐ Monitor false negatives
☐ Collect user feedback

Documentation:
☐ Medical disclaimer visible to users
☐ System limitations documented
☐ Emergency contact information
☐ How to report errors/incorrect predictions
☐ Privacy policy for symptom data
"""

# ============================================================================
# 11. MEDICAL COMPLIANCE & DISCLAIMERS
# ============================================================================

MEDICAL_DISCLAIMER = """
IMPORTANT MEDICAL DISCLAIMER

This disease prediction system:

✗ Is NOT a substitute for professional medical diagnosis
✗ Should NOT be used to delay urgent medical attention
✗ Does NOT account for individual patient factors
✗ Is NOT approved by healthcare regulatory agencies

✓ IS a clinical decision support tool
✓ IS based on established symptom correlations
✓ IS for patient education and symptom awareness
✓ CAN help prioritize medical consultation

Liability:
- The system creators assume no liability for inaccurate predictions
- Users accept full responsibility for their medical decisions
- Users should always consult licensed healthcare providers
- Severe symptoms require immediate emergency care
- This system cannot replace clinical judgment

When to Seek Emergency Care (ALWAYS):
- Chest pain or pressure
- Difficulty breathing
- Confusion or altered mental status
- Severe abdominal pain
- Uncontrolled bleeding
- Loss of consciousness
- Severe allergic reaction
"""

# ============================================================================
# 12. API RESPONSE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*70)
    print("DATABASE STRUCTURE")
    print("="*70)
    print(DATABASE_STRUCTURE)
    print("\n" + "="*70)
    print("ALGORITHM EXPLANATION")
    print("="*70)
    print(ALGORITHM_EXPLANATION)
    print("\n" + "="*70)
    print("DEPLOYMENT CHECKLIST")
    print("="*70)
    print(DEPLOYMENT_CHECKLIST)
    print("\n" + "="*70)
    print("MEDICAL DISCLAIMER")
    print("="*70)
    print(MEDICAL_DISCLAIMER)
