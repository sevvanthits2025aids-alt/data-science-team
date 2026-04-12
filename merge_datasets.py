"""
Merge all disease prediction dataset files into one unified dataset
Handles different CSV formats and ensures no duplicates
"""

import pandas as pd
import os
from pathlib import Path

# Define dataset files to merge
DATASET_FILES = [
    "expanded_medical_dataset.csv",
    "extended_medical_dataset.csv",
    "medical_dataset_expanded.csv",
    "Healthcare.csv"
]

OUTPUT_FILE = "unified_disease_dataset.csv"

def standardize_healthcare_data(df):
    """Convert Healthcare.csv format to standard format"""
    if 'Disease' in df.columns:
        df = df.rename(columns={'Disease': 'Disease Name'})
    
    if 'Symptom_Count' in df.columns:
        df = df.drop('Symptom_Count', axis=1)
    if 'Patient_ID' in df.columns:
        df = df.drop('Patient_ID', axis=1)
    if 'Age' in df.columns:
        df = df.drop('Age', axis=1)
    if 'Gender' in df.columns:
        df = df.drop('Gender', axis=1)
    
    # Add missing columns
    if 'Category' not in df.columns:
        df['Category'] = 'Disease'
    if 'Severity' not in df.columns:
        df['Severity'] = 'Medium'
    if 'Causes' not in df.columns:
        df['Causes'] = 'Unknown'
    
    return df[['Disease Name', 'Category', 'Symptoms', 'Severity', 'Causes']]

def clean_and_validate(df):
    """Clean and validate dataset"""
    # Remove duplicates
    df = df.drop_duplicates(subset=['Disease Name', 'Symptoms'], keep='first')
    
    # Remove rows with missing critical columns
    df = df.dropna(subset=['Disease Name', 'Symptoms'])
    
    # Standardize disease names
    df['Disease Name'] = df['Disease Name'].str.strip().str.title()
    
    # Standardize symptoms (lowercase)
    df['Symptoms'] = df['Symptoms'].str.strip().str.lower()
    
    # Standardize severity
    df['Severity'] = df['Severity'].str.strip().str.title()
    df['Severity'] = df['Severity'].replace({
        'Low': 'Low',
        'Medium': 'Medium',
        'High': 'High',
        'Unknown': 'Medium'
    })
    
    return df

print("="*70)
print("MERGING DISEASE PREDICTION DATASETS")
print("="*70)

all_data = []
total_rows_before = 0

for file in DATASET_FILES:
    filepath = Path(file)
    if filepath.exists():
        print(f"\n✓ Loading {file}...")
        try:
            df = pd.read_csv(filepath)
            print(f"  Rows: {len(df)}")
            
            # Standardize format
            if 'Disease' in df.columns or 'Patient_ID' in df.columns:
                df = standardize_healthcare_data(df)
            
            all_data.append(df)
            total_rows_before += len(df)
            
        except Exception as e:
            print(f"  ✗ Error reading {file}: {e}")
    else:
        print(f"✗ File not found: {file}")

if not all_data:
    print("\nNo valid dataset files found!")
    exit(1)

print(f"\n📊 Combining {len(all_data)} files...")
combined_df = pd.concat(all_data, ignore_index=True)
print(f"Total rows before cleaning: {len(combined_df)}")

print("\n🧹 Cleaning and validating data...")
combined_df = clean_and_validate(combined_df)
print(f"Total rows after cleaning: {len(combined_df)}")
print(f"Duplicate rows removed: {total_rows_before - len(combined_df)}")

# Print statistics
print("\n" + "="*70)
print("DATASET STATISTICS")
print("="*70)
print(f"\nTotal Entries: {len(combined_df)}")
print(f"Unique Diseases: {combined_df['Disease Name'].nunique()}")
print(f"Disease Categories: {combined_df['Category'].nunique()}")

print("\nDisease Distribution:")
print(combined_df['Disease Name'].value_counts().head(10))

print("\nCategory Distribution:")
print(combined_df['Category'].value_counts())

print("\nSeverity Distribution:")
print(combined_df['Severity'].value_counts())

# Save merged dataset
print(f"\n💾 Saving merged dataset to {OUTPUT_FILE}...")
combined_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
print(f"✓ Successfully saved {len(combined_df)} rows to {OUTPUT_FILE}")

# Display sample rows
print("\n" + "="*70)
print("SAMPLE DATA")
print("="*70)
print("\nFirst 5 rows:")
print(combined_df.head().to_string())

print("\n" + "="*70)
print("MERGE COMPLETE!")
print("="*70)
print(f"✓ Output file: {OUTPUT_FILE}")
print(f"✓ Total entries: {len(combined_df):,}")
print(f"✓ Unique diseases: {combined_df['Disease Name'].nunique():,}")
