"""
Enhanced Dataset Generator
Generates realistic, medically accurate disease-symptom combinations
with symptom details, patient profiles, and environmental factors
"""

import csv
import json
import random
from typing import List, Dict, Tuple
from datetime import datetime
from enhanced_disease_database import (
    ENHANCED_DISEASE_DATABASE,
    DiseaseProfile,
    SymptomDetail,
    AgeGroup,
    Gender,
    EnvironmentalFactor,
)


class EnhancedDatasetGenerator:
    """Generate realistic medical datasets with advanced features"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.disease_database = ENHANCED_DISEASE_DATABASE
        self.generated_records: List[Dict] = []
        
    def generate_symptom_detail(
        self, 
        symptom_detail: SymptomDetail,
        variation: float = 0.1  # Allow 10% variation from expected
    ) -> Dict:
        """
        Generate realistic symptom details based on disease profile
        with controlled variation
        """
        return {
            'name': symptom_detail.name,
            'duration': symptom_detail.duration.value,
            'severity': symptom_detail.severity.value,
            'pattern': symptom_detail.pattern.value,
            'location': symptom_detail.body_location,
            'weight': symptom_detail.weight,
            'onset_order': symptom_detail.onset_order,
        }
    
    def generate_patient_profile(
        self,
        disease_profile: DiseaseProfile,
        risk_patient_probability: float = 0.3
    ) -> Dict:
        """
        Generate patient profile that may or may not be at high risk
        """
        # Probability of high-risk patient
        is_high_risk = random.random() < risk_patient_probability
        
        if is_high_risk and disease_profile.high_risk_age_groups:
            age_group = random.choice(disease_profile.high_risk_age_groups)
        else:
            age_group = random.choice(list(AgeGroup))
        
        # Medical history
        medical_history = []
        if is_high_risk and disease_profile.medical_history_risk_factors:
            if random.random() < 0.5:
                medical_history.append(random.choice(disease_profile.medical_history_risk_factors))
        
        # Add random comorbidities
        common_comorbidities = ['hypertension', 'diabetes', 'asthma', 'obesity', 'smoking']
        if random.random() < 0.3:
            medical_history.append(random.choice(common_comorbidities))
        
        return {
            'age_group': age_group.value,
            'gender': random.choice([g.value for g in Gender if g.value != 'n/a']),
            'medical_history': medical_history,
            'immune_status': random.choice(['normal', 'slightly immunocompromised', 'normal']) 
                            if is_high_risk else 'normal',
            'vaccination_status': {},
        }
    
    def generate_environmental_factors(
        self,
        disease_profile: DiseaseProfile,
        include_probability: float = 0.4
    ) -> List[str]:
        """Generate relevant environmental factors"""
        factors = []
        
        # Add disease-specific environmental factors
        if disease_profile.environmental_factors and random.random() < include_probability:
            factor = random.choice(disease_profile.environmental_factors)
            factors.append(factor.value)
        
        # Add general factors
        general_factors = [
            'crowded living', 'poor sanitation', 'high pollen',
            'poor air quality', 'workplace hazard'
        ]
        if random.random() < 0.3:
            factors.append(random.choice(general_factors))
        
        return factors
    
    def generate_disease_record(
        self,
        disease_name: str,
        disease_profile: DiseaseProfile,
        variation_level: str = 'normal'
    ) -> Dict:
        """
        Generate realistic disease record
        
        Args:
            disease_name: Name of disease
            disease_profile: Disease profile from database
            variation_level: 'strict' (exact match), 'normal' (realistic variation), 'severe' (atypical presentation)
        """
        record = {
            'disease_name': disease_name,
            'category': disease_profile.category.value,
            'severity_level': disease_profile.severity_level.value,
        }
        
        # Generate symptoms
        symptoms_list = []
        
        # Always include most primary symptoms
        num_primary = len(disease_profile.primary_symptoms)
        if variation_level == 'strict':
            primary_to_include = num_primary
        elif variation_level == 'normal':
            primary_to_include = max(int(num_primary * 0.7), 1)  # Include 70% of primary symptoms
        else:  # severe
            primary_to_include = max(int(num_primary * 0.5), 1)  # Include only 50% (atypical)
        
        included_primary = random.sample(
            disease_profile.primary_symptoms,
            min(primary_to_include, num_primary)
        )
        
        for symptom in included_primary:
            symptoms_list.append(self.generate_symptom_detail(symptom))
        
        # Include some secondary symptoms
        num_secondary = len(disease_profile.secondary_symptoms)
        if variation_level == 'strict':
            secondary_to_include = max(int(num_secondary * 0.5), 0)
        elif variation_level == 'normal':
            secondary_to_include = random.randint(0, int(num_secondary * 0.4))
        else:  # severe
            secondary_to_include = random.randint(0, num_secondary)
        
        included_secondary = random.sample(
            disease_profile.secondary_symptoms,
            min(secondary_to_include, len(disease_profile.secondary_symptoms))
        )
        
        for symptom in included_secondary:
            symptoms_list.append(self.generate_symptom_detail(symptom))
        
        record['symptoms'] = symptoms_list
        record['num_symptoms'] = len(symptoms_list)
        
        # Generate patient profile
        record['patient_profile'] = self.generate_patient_profile(disease_profile)
        
        # Generate environmental factors
        record['environmental_factors'] = self.generate_environmental_factors(disease_profile)
        
        # Generate negative symptoms (that should NOT be present)
        negative_symptoms = []
        if disease_profile.negative_symptoms and random.random() < 0.5:
            # Sometimes include absence of negative symptoms for contrast
            num_negative = random.randint(0, min(2, len(disease_profile.negative_symptoms)))
            negative_symptoms = random.sample(disease_profile.negative_symptoms, num_negative)
        record['negative_symptoms'] = negative_symptoms
        
        # Additional clinical info
        record['typical_onset'] = disease_profile.typical_onset
        record['incubation_period'] = f"{disease_profile.incubation_period_min_days}-{disease_profile.incubation_period_max_days}"
        record['recovery_time_days'] = random.randint(
            disease_profile.recovery_time_min_days,
            disease_profile.recovery_time_max_days
        )
        record['diagnostic_tests'] = disease_profile.diagnostic_tests[:2]  # Top 2 tests
        record['treatment_options'] = disease_profile.treatment_options[:2]  # Top 2 treatments
        
        return record
    
    def generate_dataset(
        self,
        records_per_disease: int = 50,
        include_variations: bool = True,
        output_file: str = 'enhanced_medical_dataset.json'
    ) -> List[Dict]:
        """
        Generate complete dataset
        
        Args:
            records_per_disease: Number of records to generate per disease
            include_variations: Whether to include strict/normal/severe variations
            output_file: JSON file to save generated data
            
        Returns:
            List of generated records
        """
        records = []
        
        print(f"Generating {len(self.disease_database)} diseases...")
        print(f"Records per disease: {records_per_disease}")
        print(f"Include variations: {include_variations}\n")
        
        total_records = 0
        
        for disease_name, disease_profile in self.disease_database.items():
            print(f"Generating records for: {disease_name}...", end=" ")
            
            disease_records = 0
            
            if include_variations:
                # Generate mix of strict, normal, and severe presentations
                records_per_variation = records_per_disease // 3
                
                for variation in ['strict', 'normal', 'severe']:
                    for _ in range(records_per_variation):
                        record = self.generate_disease_record(
                            disease_name,
                            disease_profile,
                            variation_level=variation
                        )
                        records.append(record)
                        disease_records += 1
            else:
                # Generate normal presentation only
                for _ in range(records_per_disease):
                    record = self.generate_disease_record(
                        disease_name,
                        disease_profile,
                        variation_level='normal'
                    )
                    records.append(record)
                    disease_records += 1
            
            total_records += disease_records
            print(f"✓ ({disease_records} records)")
        
        print(f"\n{'='*60}")
        print(f"Total records generated: {total_records}")
        print(f"Total unique diseases: {len(self.disease_database)}")
        print(f"{'='*60}\n")
        
        # Save to JSON
        self._save_json_dataset(records, output_file)
        
        # Also save as CSV for ML training
        csv_file = output_file.replace('.json', '.csv')
        self._save_csv_dataset(records, csv_file)
        
        self.generated_records = records
        return records
    
    def _save_json_dataset(self, records: List[Dict], filename: str):
        """Save dataset as JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"✓ JSON dataset saved: {filename}")
    
    def _save_csv_dataset(self, records: List[Dict], filename: str):
        """Save dataset as CSV for ML training"""
        if not records:
            return
        
        # Flatten the complex structure for CSV
        flattened_records = []
        
        for record in records:
            flat_record = {
                'disease_name': record['disease_name'],
                'category': record['category'],
                'severity_level': record['severity_level'],
                'num_symptoms': record['num_symptoms'],
                'symptoms_list': ', '.join([s['name'] for s in record['symptoms']]),
                'symptoms_with_details': json.dumps(record['symptoms']),
                'patient_age_group': record['patient_profile']['age_group'],
                'patient_gender': record['patient_profile']['gender'],
                'patient_medical_history': ', '.join(record['patient_profile']['medical_history']),
                'patient_immune_status': record['patient_profile']['immune_status'],
                'environmental_factors': ', '.join(record['environmental_factors']),
                'negative_symptoms': ', '.join(record['negative_symptoms']),
                'typical_onset': record['typical_onset'],
                'incubation_period': record['incubation_period'],
                'recovery_time_days': record['recovery_time_days'],
                'diagnostic_tests': ', '.join(record['diagnostic_tests']),
                'treatment_options': ', '.join(record['treatment_options']),
            }
            flattened_records.append(flat_record)
        
        # Write CSV
        fieldnames = list(flattened_records[0].keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flattened_records)
        
        print(f"✓ CSV dataset saved: {filename}")
    
    def generate_differential_diagnosis_dataset(
        self,
        disease_pairs: int = 30,
        output_file: str = 'differential_diagnosis_dataset.json'
    ) -> List[Dict]:
        """
        Generate dataset for differential diagnosis (similar symptom diseases)
        to help ML model distinguish between easily confused diseases
        """
        print(f"Generating differential diagnosis dataset...")
        print(f"Disease pairs: {disease_pairs}\n")
        
        records = []
        diseases = list(self.disease_database.keys())
        
        # Create disease pairs with similar symptoms
        generated_pairs = set()
        attempts = 0
        max_attempts = disease_pairs * 5
        
        while len(records) < disease_pairs and attempts < max_attempts:
            attempts += 1
            
            disease1 = random.choice(diseases)
            disease2 = random.choice(diseases)
            
            if disease1 == disease2:
                continue
            
            pair = tuple(sorted([disease1, disease2]))
            if pair in generated_pairs:
                continue
            
            generated_pairs.add(pair)
            
            profile1 = self.disease_database[disease1]
            profile2 = self.disease_database[disease2]
            
            # Generate records for each disease
            record1 = self.generate_disease_record(disease1, profile1)
            record2 = self.generate_disease_record(disease2, profile2)
            
            diff_record = {
                'disease_1': disease1,
                'disease_2': disease2,
                'category_1': profile1.category.value,
                'category_2': profile2.category.value,
                'distinguishing_features_disease_1': [
                    s['name'] for s in record1['symptoms']
                    if s not in record2['symptoms']
                ][:3],
                'distinguishing_features_disease_2': [
                    s['name'] for s in record2['symptoms']
                    if s not in record1['symptoms']
                ][:3],
                'common_symptoms': [
                    s['name'] for s in record1['symptoms']
                    if any(s2['name'] == s['name'] for s2 in record2['symptoms'])
                ],
                'disease_1_data': record1,
                'disease_2_data': record2,
            }
            
            records.append(diff_record)
            print(f"Generated pair: {disease1} vs {disease2}")
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Differential diagnosis dataset saved: {output_file} ({len(records)} pairs)")
        return records
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of generated data"""
        if not self.generated_records:
            return "No records have been generated yet."
        
        report = "\n" + "="*70 + "\n"
        report += "ENHANCED DATASET SUMMARY REPORT\n"
        report += "="*70 + "\n\n"
        
        # Disease distribution
        disease_counts = {}
        for record in self.generated_records:
            disease = record['disease_name']
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
        
        report += f"Total Records: {len(self.generated_records)}\n"
        report += f"Unique Diseases: {len(disease_counts)}\n"
        report += f"Average records per disease: {len(self.generated_records) / len(disease_counts):.1f}\n\n"
        
        # Category distribution
        category_counts = {}
        for record in self.generated_records:
            category = record['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        report += "Disease Category Distribution:\n"
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.generated_records)) * 100
            report += f"  {category:<20} {count:>5} ({percentage:>5.1f}%)\n"
        
        # Symptom statistics
        all_symptoms = set()
        symptom_frequency = {}
        for record in self.generated_records:
            for symptom in record['symptoms']:
                symptom_name = symptom['name']
                all_symptoms.add(symptom_name)
                symptom_frequency[symptom_name] = symptom_frequency.get(symptom_name, 0) + 1
        
        report += f"\nTotal Unique Symptoms: {len(all_symptoms)}\n"
        report += f"Average symptoms per record: {sum(r['num_symptoms'] for r in self.generated_records) / len(self.generated_records):.1f}\n\n"
        
        report += "Top 15 Most Frequent Symptoms:\n"
        for symptom, count in sorted(symptom_frequency.items(), key=lambda x: x[1], reverse=True)[:15]:
            percentage = (count / len(self.generated_records)) * 100
            report += f"  {symptom:<25} {count:>5} ({percentage:>5.1f}%)\n"
        
        # Patient profile distribution
        age_groups = {}
        genders = {}
        for record in self.generated_records:
            profile = record['patient_profile']
            age = profile['age_group']
            gender = profile['gender']
            age_groups[age] = age_groups.get(age, 0) + 1
            genders[gender] = genders.get(gender, 0) + 1
        
        report += "\nPatient Age Group Distribution:\n"
        for age_group, count in sorted(age_groups.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.generated_records)) * 100
            report += f"  {age_group:<30} {count:>5} ({percentage:>5.1f}%)\n"
        
        report += "\nPatient Gender Distribution:\n"
        for gender, count in sorted(genders.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.generated_records)) * 100
            report += f"  {gender:<20} {count:>5} ({percentage:>5.1f}%)\n"
        
        # Environmental factors
        all_env_factors = set()
        for record in self.generated_records:
            all_env_factors.update(record['environmental_factors'])
        
        report += f"\nUnique Environmental Factors: {len(all_env_factors)}\n"
        report += f"Records with environmental factors: {sum(1 for r in self.generated_records if r['environmental_factors'])}\n"
        
        report += "\n" + "="*70 + "\n"
        
        return report


def main():
    """Main function to generate enhanced datasets"""
    
    print("\n" + "="*70)
    print("ENHANCED DISEASE PREDICTION DATASET GENERATOR")
    print("="*70 + "\n")
    
    generator = EnhancedDatasetGenerator(seed=42)
    
    # Generate main dataset
    print("STEP 1: Generating main enhanced dataset with variations...")
    print("-" * 70)
    dataset = generator.generate_dataset(
        records_per_disease=75,  # 25 strict + 25 normal + 25 severe
        include_variations=True,
        output_file='enhanced_medical_dataset_v2.json'
    )
    
    # Generate differential diagnosis dataset
    print("\nSTEP 2: Generating differential diagnosis dataset...")
    print("-" * 70)
    diff_dataset = generator.generate_differential_diagnosis_dataset(
        disease_pairs=50,
        output_file='differential_diagnosis_dataset.json'
    )
    
    # Print summary report
    print("\n" + generator.generate_summary_report())
    
    print("\nDataset generation complete!")
    print("Generated files:")
    print("  ✓ enhanced_medical_dataset_v2.json")
    print("  ✓ enhanced_medical_dataset_v2.csv")
    print("  ✓ differential_diagnosis_dataset.json")
    

if __name__ == "__main__":
    main()

