"""
Flask API Routes for Enhanced Disease Prediction System
Add these routes to your app.py
"""

from flask import Flask, request, jsonify
from integrated_prediction_system import IntegratedDiseasePredictionSystem
from advanced_disease_predictor import AdvancedDiseasePredictor
import json

# Initialize system
prediction_system = IntegratedDiseasePredictionSystem()


# ============================================================================
# ENHANCED PREDICTION ROUTES
# ============================================================================

def setup_enhanced_prediction_routes(app: Flask):
    """Setup enhanced prediction routes"""
    
    # Route 1: Advanced Prediction with All Features
    @app.route('/api/predict/advanced', methods=['POST'])
    def predict_advanced():
        """
        Advanced prediction with all enhanced features
        
        Request JSON:
        {
            "symptoms": [
                {
                    "name": "fever",
                    "duration": "3-7 days",
                    "severity": "moderate",
                    "location": "whole body",
                    "pattern": "continuous",
                    "onset_order": 1
                }
            ],
            "patient": {
                "age_group": "adult",
                "gender": "male",
                "medical_history": ["diabetes"],
                "medications": [],
                "allergies": []
            },
            "environment": {
                "factors": ["crowded living", "poor air quality"]
            },
            "negative_symptoms": ["cough", "rash"]
        }
        """
        try:
            data = request.json
            
            results = prediction_system.predict_from_user_input(
                symptoms_input={'symptoms': data.get('symptoms', [])},
                patient_demographics=data.get('patient', {}),
                environmental_info=data.get('environment', {}),
                negative_symptoms_input=data.get('negative_symptoms', [])
            )
            
            return jsonify(results), 200 if results['status'] == 'success' else 400
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    # Route 2: Get Disease Information
    @app.route('/api/disease/<disease_name>', methods=['GET'])
    def get_disease(disease_name):
        """Get detailed information about a disease"""
        try:
            result = prediction_system.get_disease_information(disease_name)
            return jsonify(result), 200 if result['status'] == 'success' else 404
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    # Route 3: List All Diseases
    @app.route('/api/diseases', methods=['GET'])
    def list_diseases():
        """List all diseases in database"""
        try:
            predictor = AdvancedDiseasePredictor()
            diseases = []
            for disease_name, disease_profile in predictor.disease_database.items():
                diseases.append({
                    'name': disease_name,
                    'category': disease_profile.category.value,
                    'severity': disease_profile.severity_level.value,
                    'prevalence': disease_profile.prevalence_score
                })
            
            diseases.sort(key=lambda x: x['prevalence'], reverse=True)
            
            return jsonify({
                'status': 'success',
                'total_diseases': len(diseases),
                'diseases': diseases
            }), 200
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    # Route 4: Symptom Timeline Analysis
    @app.route('/api/analyze/timeline', methods=['POST'])
    def analyze_timeline():
        """Analyze symptom progression timeline"""
        try:
            data = request.json
            symptoms = data.get('symptoms', [])
            
            result = prediction_system.calculate_symptom_timeline(symptoms)
            
            return jsonify({
                'status': 'success',
                'timeline': result
            }), 200
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    # Route 5: Disease Comparison
    @app.route('/api/compare-diseases', methods=['POST'])
    def compare_diseases():
        """Compare symptoms and features of multiple diseases"""
        try:
            data = request.json
            disease_names = data.get('diseases', [])
            
            predictor = AdvancedDiseasePredictor()
            comparison = {
                'diseases': [],
                'common_symptoms': [],
                'unique_symptoms': {}
            }
            
            disease_profiles = []
            for disease_name in disease_names:
                disease = predictor.disease_database.get(disease_name.lower())
                if disease:
                    disease_profiles.append({
                        'name': disease_name,
                        'profile': disease
                    })
                    comparison['diseases'].append({
                        'name': disease_name,
                        'category': disease.category.value,
                        'severity': disease.severity_level.value
                    })
            
            if len(disease_profiles) >= 2:
                # Find common symptoms
                all_symptoms = []
                for dp in disease_profiles:
                    symptoms = set([s.name for s in dp['profile'].primary_symptoms] + 
                                 [s.name for s in dp['profile'].secondary_symptoms])
                    all_symptoms.append(symptoms)
                
                common = set.intersection(*all_symptoms) if all_symptoms else set()
                comparison['common_symptoms'] = list(common)
                
                # Find unique symptoms
                for i, dp in enumerate(disease_profiles):
                    symbols = set([s.name for s in dp['profile'].primary_symptoms] + 
                                [s.name for s in dp['profile'].secondary_symptoms])
                    others = set()
                    for j, other_dp in enumerate(disease_profiles):
                        if i != j:
                            others.update([s.name for s in other_dp['profile'].primary_symptoms] + 
                                        [s.name for s in other_dp['profile'].secondary_symptoms])
                    unique = symbols - others
                    comparison['unique_symptoms'][dp['name']] = list(unique)
            
            return jsonify({
                'status': 'success',
                'comparison': comparison
            }), 200
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    # Route 6: Differential Diagnosis Suggestions
    @app.route('/api/differential-diagnosis', methods=['POST'])
    def differential_diagnosis():
        """Get differential diagnosis suggestions"""
        try:
            data = request.json
            symptoms = data.get('symptoms', [])
            
            # Run prediction to get top differentials
            results = prediction_system.predict_from_user_input(
                symptoms_input={'symptoms': symptoms},
                patient_demographics=data.get('patient', {}),
                environmental_info=data.get('environment', {})
            )
            
            if results['status'] == 'success':
                # Filter for top 5-7 differentials
                differentials = results['predictions'][:7]
                
                return jsonify({
                    'status': 'success',
                    'differential_diagnosis': [
                        {
                            'rank': d['rank'],
                            'disease': d['disease_name'],
                            'probability': d['probability_percent'],
                            'confidence': d['confidence_level'],
                            'category': d['category'],
                            'next_steps': self._get_next_steps(d['disease_name'])
                        }
                        for d in differentials
                    ]
                }), 200
            else:
                return jsonify(results), 400
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    # Route 7: Symptom Metadata (available symptoms, durations, severities)
    @app.route('/api/metadata/symptoms', methods=['GET'])
    def get_symptom_metadata():
        """Get metadata about available symptoms and their properties"""
        try:
            predictor = AdvancedDiseasePredictor()
            
            symptom_data = {
                'durations': [
                    'hours', '1-3 days', '3-7 days', '1-2 weeks', 
                    '2-4 weeks', '1-3 months', '3+ months'
                ],
                'severities': ['mild', 'moderate', 'severe', 'critical'],
                'patterns': ['continuous', 'intermittent', 'progressive', 'recurring'],
                'body_locations': [
                    'head', 'neck', 'chest', 'abdomen', 'back', 'joints',
                    'limbs', 'skin', 'throat', 'lungs', 'heart', 'stomach',
                    'intestines', 'eyes', 'ears', 'nose', 'mouth'
                ],
                'common_symptoms': list(set(
                    [s.name for d in predictor.disease_database.values() 
                     for s in d.primary_symptoms]
                )),
                'age_groups': [
                    'infant', 'toddler', 'child', 'adolescent',
                    'young adult', 'adult', 'middle-aged', 'elderly'
                ]
            }
            
            return jsonify({
                'status': 'success',
                'metadata': symptom_data
            }), 200
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    # Route 8: Risk Assessment
    @app.route('/api/risk-assessment', methods=['POST'])
    def risk_assessment():
        """Assess health risks based on patient profile and environment"""
        try:
            data = request.json
            
            predictor = AdvancedDiseasePredictor()
            patient_info = data.get('patient', {})
            env_factors = data.get('environment', {}).get('factors', [])
            
            # Identify high-risk diseases
            high_risk_diseases = []
            
            for disease_name, disease_profile in predictor.disease_database.items():
                risk_score = 0.0
                
                # Age-based risk
                age_group = patient_info.get('age_group', 'adult')
                age_obj = prediction_system._parse_age_group(age_group)
                if age_obj in disease_profile.high_risk_age_groups:
                    risk_score += 0.3
                
                # Medical history risk
                medical_history = patient_info.get('medical_history', [])
                for risk_factor in disease_profile.medical_history_risk_factors:
                    if any(risk_factor.lower() in h.lower() for h in medical_history):
                        risk_score += 0.25
                
                # Environmental risk
                for env_factor in disease_profile.environmental_factors:
                    if any(env_factor.value.lower() in str(f).lower() for f in env_factors):
                        risk_score += 0.2
                
                if risk_score > 0:
                    high_risk_diseases.append({
                        'disease': disease_name,
                        'risk_score': min(risk_score, 1.0),
                        'category': disease_profile.category.value,
                        'prevention': 'Consult healthcare provider for screening'
                    })
            
            high_risk_diseases.sort(key=lambda x: x['risk_score'], reverse=True)
            
            return jsonify({
                'status': 'success',
                'high_risk_diseases': high_risk_diseases[:10],
                'total_assessed': len(high_risk_diseases),
                'recommendation': 'Consider regular health checkups' if high_risk_diseases else 'Low risk profile'
            }), 200
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
    
    
    return app


def _get_next_steps(disease_name: str) -> List[str]:
    """Get recommended next steps for a disease"""
    
    next_steps_map = {
        'influenza': [
            'Confirm with rapid flu test',
            'Start antivirals if within 48 hours of onset',
            'Rest and stay hydrated',
            'Isolate from others for 5-7 days'
        ],
        'covid-19': [
            'Take COVID-19 PCR or antigen test',
            'Isolate immediately',
            'Monitor oxygen saturation',
            'Consider monoclonal antibody treatment if high-risk'
        ],
        'common cold': [
            'Supportive care: rest, fluids',
            'Over-the-counter symptom relief',
            'No specific treatment needed'
        ],
        'pneumonia': [
            'Immediate chest X-ray',
            'Blood culture and sputum test',
            'Start antibiotics',
            'Monitor for complications'
        ],
        'dengue': [
            'Dengue serological test (IgM/IgG)',
            'Monitor platelet count',
            'Careful fluid management',
            'Watch for hemorrhagic fever signs'
        ],
    }
    
    return next_steps_map.get(disease_name.lower(), [
        'Consult healthcare provider',
        'Confirm diagnosis with appropriate tests',
        'Follow treatment recommendations'
    ])


# ============================================================================
# EXAMPLE: How to integrate into your app.py
# ============================================================================

"""
# In your app.py, add this before app.run():

from flask_integrated_routes import setup_enhanced_prediction_routes

app = Flask(__name__)
# ... other app setup ...

# Setup enhanced prediction routes
setup_enhanced_prediction_routes(app)

# ... rest of your app setup ...
app.run(debug=True)


# EXAMPLE API CALLS:

# 1. Advanced Prediction:
curl -X POST http://localhost:5000/api/predict/advanced \\
  -H "Content-Type: application/json" \\
  -d '{
    "symptoms": [
      {"name": "fever", "duration": "3-7 days", "severity": "moderate", "location": "whole body"},
      {"name": "cough", "duration": "1-2 weeks", "severity": "moderate", "location": "chest"}
    ],
    "patient": {"age_group": "adult", "gender": "male"},
    "environment": {"factors": ["crowded living"]},
    "negative_symptoms": ["loss of taste"]
  }'

# 2. Get Disease Information:
curl http://localhost:5000/api/disease/influenza

# 3. List All Diseases:
curl http://localhost:5000/api/diseases

# 4. Differential Diagnosis:
curl -X POST http://localhost:5000/api/differential-diagnosis \\
  -H "Content-Type: application/json" \\
  -d '{"symptoms": [{"name": "fever"}]}'

# 5. Risk Assessment:
curl -X POST http://localhost:5000/api/risk-assessment \\
  -H "Content-Type: application/json" \\
  -d '{"patient": {"age_group": "elderly"}, "environment": {"factors": ["crowded"]}}'

"""

