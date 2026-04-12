"""
Comprehensive Dataset Merger for Disease Prediction Project
Merges all disease and vaccine datasets into unified files
"""

import pandas as pd
import os
import glob
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class DatasetMerger:
    """Advanced dataset merger for disease prediction project"""

    def __init__(self, project_dir="C:\\Users\\Sevvanthi\\Desktop\\DISEASE PREDICTION"):
        self.project_dir = Path(project_dir)
        self.disease_files = []
        self.vaccine_files = []
        self.merged_disease_df = None
        self.merged_vaccine_df = None

    def find_csv_files(self):
        """Find all CSV files and categorize them"""
        print("🔍 Scanning for CSV files...")

        # Find all CSV files
        csv_files = list(self.project_dir.glob("*.csv"))
        print(f"Found {len(csv_files)} CSV files total")

        # Categorize files
        disease_keywords = ['disease', 'symptom', 'medical', 'healthcare', 'prediction']
        vaccine_keywords = ['vaccine']

        for csv_file in csv_files:
            filename = csv_file.name.lower()

            # Skip certain files
            if any(skip in filename for skip in ['history', 'users', 'merged']):
                continue

            # Check if vaccine file
            if any(keyword in filename for keyword in vaccine_keywords):
                self.vaccine_files.append(csv_file)
                print(f"  📋 Vaccine file: {csv_file.name}")
            # Check if disease file
            elif any(keyword in filename for keyword in disease_keywords):
                self.disease_files.append(csv_file)
                print(f"  🏥 Disease file: {csv_file.name}")
            else:
                # Default to disease if unclear
                self.disease_files.append(csv_file)
                print(f"  ❓ Unclear file (treating as disease): {csv_file.name}")

        print(f"\n📊 Summary:")
        print(f"  Disease files: {len(self.disease_files)}")
        print(f"  Vaccine files: {len(self.vaccine_files)}")

    def load_and_merge_disease_files(self):
        """Load and merge all disease-related CSV files"""
        print("\n🏥 Merging disease datasets...")

        if not self.disease_files:
            print("No disease files found!")
            return

        dfs = []
        total_rows = 0

        for file_path in self.disease_files:
            try:
                print(f"  Loading: {file_path.name}")
                df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)

                # Handle duplicate columns by renaming them
                cols = df.columns.tolist()
                seen = set()
                new_cols = []
                for col in cols:
                    col_lower = col.lower().replace(' ', '_').replace('-', '_')
                    if col_lower in seen:
                        # Rename duplicate
                        counter = 1
                        while f"{col_lower}_{counter}" in seen:
                            counter += 1
                        new_col = f"{col_lower}_{counter}"
                    else:
                        new_col = col_lower
                    seen.add(new_col)
                    new_cols.append(new_col)

                df.columns = new_cols

                print(f"    Columns: {list(df.columns)}")
                print(f"    Rows: {len(df)}")

                dfs.append(df)
                total_rows += len(df)

            except Exception as e:
                print(f"    ❌ Error loading {file_path.name}: {e}")
                continue

        if not dfs:
            print("No valid disease dataframes loaded!")
            return

        print(f"\n🔄 Combining {len(dfs)} disease dataframes...")

        # Merge all dataframes with better error handling
        try:
            self.merged_disease_df = pd.concat(dfs, ignore_index=True, sort=False)
        except Exception as e:
            print(f"❌ Error during concat: {e}")
            print("Trying alternative merge approach...")

            # Alternative: merge one by one
            self.merged_disease_df = dfs[0]
            for df in dfs[1:]:
                try:
                    self.merged_disease_df = pd.concat([self.merged_disease_df, df], ignore_index=True, sort=False)
                except Exception as e2:
                    print(f"❌ Skipping problematic dataframe: {e2}")
                    continue

        print(f"  Before cleaning: {len(self.merged_disease_df)} rows")

        # Clean and standardize
        self._clean_disease_dataset()

        print(f"  After cleaning: {len(self.merged_disease_df)} rows")
        print(f"  Final columns: {list(self.merged_disease_df.columns)}")

    def _clean_disease_dataset(self):
        """Clean and standardize the merged disease dataset"""
        if self.merged_disease_df is None:
            return

        # Fill missing values
        self.merged_disease_df = self.merged_disease_df.fillna('none')

        # Standardize disease names
        if 'disease' in self.merged_disease_df.columns:
            self.merged_disease_df['disease'] = self.merged_disease_df['disease'].str.strip().str.title()
        elif 'disease_name' in self.merged_disease_df.columns:
            self.merged_disease_df['disease'] = self.merged_disease_df['disease_name'].str.strip().str.title()
            self.merged_disease_df = self.merged_disease_df.drop('disease_name', axis=1)

        # Standardize symptom columns
        symptom_cols = [col for col in self.merged_disease_df.columns if 'symptom' in col.lower()]
        if symptom_cols:
            # Combine all symptom columns into one
            self.merged_disease_df['symptoms'] = self.merged_disease_df[symptom_cols].apply(
                lambda row: ', '.join([str(val) for val in row if str(val) != 'none' and str(val).lower() != 'nan']),
                axis=1
            )
            # Remove individual symptom columns
            self.merged_disease_df = self.merged_disease_df.drop(symptom_cols, axis=1)

        # Remove duplicates
        initial_count = len(self.merged_disease_df)
        self.merged_disease_df = self.merged_disease_df.drop_duplicates()
        duplicates_removed = initial_count - len(self.merged_disease_df)

        print(f"  Duplicates removed: {duplicates_removed}")

        # Ensure required columns exist
        required_cols = ['disease', 'symptoms']
        for col in required_cols:
            if col not in self.merged_disease_df.columns:
                self.merged_disease_df[col] = 'none'

        # Reorder columns
        cols = ['disease', 'symptoms'] + [col for col in self.merged_disease_df.columns if col not in ['disease', 'symptoms']]
        self.merged_disease_df = self.merged_disease_df[cols]

    def load_and_merge_vaccine_files(self):
        """Load and merge all vaccine-related CSV files"""
        print("\n💉 Merging vaccine datasets...")

        if not self.vaccine_files:
            print("No vaccine files found!")
            return

        dfs = []
        total_rows = 0

        for file_path in self.vaccine_files:
            try:
                print(f"  Loading: {file_path.name}")
                df = pd.read_csv(file_path, encoding='utf-8', low_memory=False)

                # Clean column names
                df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')

                print(f"    Columns: {list(df.columns)}")
                print(f"    Rows: {len(df)}")

                dfs.append(df)
                total_rows += len(df)

            except Exception as e:
                print(f"    ❌ Error loading {file_path.name}: {e}")
                continue

        if not dfs:
            print("No valid vaccine dataframes loaded!")
            return

        print(f"\n🔄 Combining {len(dfs)} vaccine dataframes...")

        # Merge all dataframes
        self.merged_vaccine_df = pd.concat(dfs, ignore_index=True, sort=False)

        print(f"  Before cleaning: {len(self.merged_vaccine_df)} rows")

        # Clean and standardize
        self._clean_vaccine_dataset()

        print(f"  After cleaning: {len(self.merged_vaccine_df)} rows")
        print(f"  Final columns: {list(self.merged_vaccine_df.columns)}")

    def _clean_vaccine_dataset(self):
        """Clean and standardize the merged vaccine dataset"""
        if self.merged_vaccine_df is None:
            return

        # Fill missing values
        self.merged_vaccine_df = self.merged_vaccine_df.fillna('none')

        # Standardize disease names
        if 'disease' in self.merged_vaccine_df.columns:
            self.merged_vaccine_df['disease'] = self.merged_vaccine_df['disease'].str.strip().str.title()
        elif 'disease_name' in self.merged_vaccine_df.columns:
            self.merged_vaccine_df['disease'] = self.merged_vaccine_df['disease_name'].str.strip().str.title()
            self.merged_vaccine_df = self.merged_vaccine_df.drop('disease_name', axis=1)

        # Standardize vaccine availability
        if 'vaccine_availability' in self.merged_vaccine_df.columns:
            self.merged_vaccine_df['vaccine_available'] = self.merged_vaccine_df['vaccine_availability'].str.lower().map({
                'yes': 'Yes', 'no': 'No', 'limited': 'Limited', 'available': 'Yes', 'not available': 'No'
            }).fillna('No')
            self.merged_vaccine_df = self.merged_vaccine_df.drop('vaccine_availability', axis=1)

        # Remove duplicates
        initial_count = len(self.merged_vaccine_df)
        self.merged_vaccine_df = self.merged_vaccine_df.drop_duplicates()
        duplicates_removed = initial_count - len(self.merged_vaccine_df)

        print(f"  Duplicates removed: {duplicates_removed}")

        # Ensure required columns exist
        required_cols = ['disease', 'vaccine_available']
        for col in required_cols:
            if col not in self.merged_vaccine_df.columns:
                self.merged_vaccine_df[col] = 'none'

        # Reorder columns
        cols = ['disease', 'vaccine_available'] + [col for col in self.merged_vaccine_df.columns if col not in ['disease', 'vaccine_available']]
        self.merged_vaccine_df = self.merged_vaccine_df[cols]

    def save_merged_datasets(self):
        """Save the merged datasets to CSV files"""
        print("\n💾 Saving merged datasets...")

        # Save disease dataset
        if self.merged_disease_df is not None and not self.merged_disease_df.empty:
            disease_output = self.project_dir / "merged_disease_dataset.csv"
            self.merged_disease_df.to_csv(disease_output, index=False, encoding='utf-8')
            print(f"✅ Disease dataset saved: {disease_output}")
            print(f"   Rows: {len(self.merged_disease_df)}")
        else:
            print("❌ No disease dataset to save")

        # Save vaccine dataset
        if self.merged_vaccine_df is not None and not self.merged_vaccine_df.empty:
            vaccine_output = self.project_dir / "merged_vaccine_dataset.csv"
            self.merged_vaccine_df.to_csv(vaccine_output, index=False, encoding='utf-8')
            print(f"✅ Vaccine dataset saved: {vaccine_output}")
            print(f"   Rows: {len(self.merged_vaccine_df)}")
        else:
            print("❌ No vaccine dataset to save")

    def print_summary(self):
        """Print comprehensive summary of the merge operation"""
        print("\n" + "="*60)
        print("📊 MERGE SUMMARY")
        print("="*60)

        print(f"📁 Project Directory: {self.project_dir}")
        print(f"🔍 Total CSV files found: {len(self.disease_files) + len(self.vaccine_files)}")
        print(f"🏥 Disease files processed: {len(self.disease_files)}")
        print(f"💉 Vaccine files processed: {len(self.vaccine_files)}")

        if self.merged_disease_df is not None:
            print(f"\n🏥 DISEASE DATASET:")
            print(f"   Final rows: {len(self.merged_disease_df)}")
            print(f"   Columns: {list(self.merged_disease_df.columns)}")
            print(f"   Unique diseases: {self.merged_disease_df['disease'].nunique() if 'disease' in self.merged_disease_df.columns else 'N/A'}")

        if self.merged_vaccine_df is not None:
            print(f"\n💉 VACCINE DATASET:")
            print(f"   Final rows: {len(self.merged_vaccine_df)}")
            print(f"   Columns: {list(self.merged_vaccine_df.columns)}")
            print(f"   Unique diseases: {self.merged_vaccine_df['disease'].nunique() if 'disease' in self.merged_vaccine_df.columns else 'N/A'}")

        print("\n✅ Merge operation completed successfully!")

    def run_merge(self):
        """Run the complete merge operation"""
        print("🚀 Starting Dataset Merger...")
        print("="*60)

        self.find_csv_files()
        self.load_and_merge_disease_files()
        self.load_and_merge_vaccine_files()
        self.save_merged_datasets()
        self.print_summary()


# Main execution
if __name__ == "__main__":
    merger = DatasetMerger()
    merger.run_merge()