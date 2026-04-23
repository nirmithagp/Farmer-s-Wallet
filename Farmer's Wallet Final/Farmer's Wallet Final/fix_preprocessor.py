#!/usr/bin/env python3
"""
Fix script to properly load, verify, and save preprocessors for all crops.
This ensures all scalers are fitted and ready for use in crop_price.py
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# Try to import joblib, fall back to pickle if not available
try:
    import joblib
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False

# Get paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JUPYTER_DIR = os.path.join(SCRIPT_DIR, 'code_1', 'jupyter_files')
CODE_DIR = os.path.join(SCRIPT_DIR, 'code_1')

# Crop information: (joblib_file, pkl_file, csv_file)
CROPS = {
    'jowar': ('jowar.joblib', 'jmodel.pkl', 'Jowar.csv'),
    'wheat': ('Wheat.joblib', 'wmodel.pkl', 'Wheat.csv'),
    'cotton': ('Cotton.joblib', 'cmodel.pkl', 'Cotton.csv'),
    'sugarcane': ('sugarcane.joblib', 'smodel.pkl', 'Sugarcane.csv'),
    'bajra': ('Bajra.joblib', 'bmodel.pkl', 'Bajra.csv'),
}

def verify_and_fix_preprocessors():
    """Verify and fix all preprocessor files."""
    
    print("=" * 60)
    print("FIXING CROP PRICE PREPROCESSORS")
    print("=" * 60)
    
    # First, check if we have individual crop preprocessors
    preprocessor_mapping = {
        'jowar': 'jowar_preprocessor.pkl',  # Check if it exists
        'wheat': 'Wpreprocessor.pkl',
        'cotton': 'cpreprocessor.pkl',
        'sugarcane': 'spreprocessor.pkl',
        'bajra': 'bpreprocessor.pkl',
    }
    
    all_preprocessors = {}
    
    for crop, preproc_file in preprocessor_mapping.items():
        preproc_path = os.path.join(JUPYTER_DIR, preproc_file)
        
        if os.path.exists(preproc_path):
            try:
                # Try to load with pickle
                with open(preproc_path, 'rb') as f:
                    preprocessor = pickle.load(f)
                all_preprocessors[crop] = preprocessor
                print(f"✓ Loaded {crop}: {preproc_file}")
                
                # Verify it's fitted
                if hasattr(preprocessor, 'named_steps'):
                    scaler = preprocessor.named_steps.get('std_scaler')
                    if scaler and hasattr(scaler, 'scale_'):
                        print(f"  ✓ Pipeline has fitted scaler")
                    else:
                        print(f"  ⚠ Pipeline scaler not fitted - will rebuild")
                else:
                    print(f"  ⚠ Not a pipeline - will rebuild")
            except Exception as e:
                print(f"✗ Error loading {crop} preprocessor: {e}")
        else:
            print(f"✗ Not found: {preproc_file}")
    
    # If all preprocessors are loaded and fitted, use the first one
    if all_preprocessors:
        # Verify the first preprocessor works
        first_preprocessor = list(all_preprocessors.values())[0]
        
        # Test transform
        try:
            test_data = pd.DataFrame([[3, 2024, 100]], columns=['Month', 'Year', 'Rainfall'])
            result = first_preprocessor.transform(test_data)
            print(f"\n✓ Test transform successful: {result.shape}")
            
            # Save as the unified preprocessor
            unified_path = os.path.join(CODE_DIR, 'preprocessor.pkl')
            joblib.dump(first_preprocessor, unified_path)
            print(f"✓ Saved unified preprocessor to: {unified_path}")
            return True
            
        except Exception as e:
            print(f"✗ Test transform failed: {e}")
    
    # If we reach here, rebuild preprocessors from scratch
    print("\n" + "=" * 60)
    print("REBUILDING PREPROCESSORS FROM TRAINING DATA")
    print("=" * 60)
    
    for crop, (joblib_file, pkl_file, csv_file) in CROPS.items():
        csv_path = os.path.join(JUPYTER_DIR, csv_file)
        
        if not os.path.exists(csv_path):
            print(f"✗ CSV not found: {csv_file}")
            continue
        
        try:
            # Load data
            df = pd.read_csv(csv_path)
            print(f"\n✓ Loaded {csv_file}: {df.shape}")
            
            # Separate features and labels (assuming 'WPI' is the target)
            if 'WPI' in df.columns:
                df_labels = df['WPI'].copy()
                df_features = df.drop('WPI', axis=1)
            else:
                print(f"  ⚠ No 'WPI' column found, using all columns")
                df_features = df
            
            # Create and fit pipeline with model
            pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('std_scaler', StandardScaler()),
                ('model', RandomForestRegressor(random_state=42, n_estimators=100))
            ])
            
            # Fit on the data
            pipeline.fit(df_features, df_labels)
            print(f"  ✓ Fitted pipeline (including model) for {crop}")
            
            # Test prediction
            test_data = df_features.iloc[:1]
            result = pipeline.predict(test_data)
            print(f"  ✓ Test prediction successful: {result}")
            
            # Save it
            pkl_path = os.path.join(CODE_DIR, pkl_file)
            
            # Use pickle for better compatibility
            with open(pkl_path, 'wb') as f:
                pickle.dump(pipeline, f)
            print(f"  ✓ Saved to: {pkl_file}")
            
        except Exception as e:
            print(f"✗ Error processing {crop}: {e}")
    
    # Load one and save as unified preprocessor
    unified_preproc = None
    for crop, (_, pkl_file, _) in CROPS.items():
        pkl_path = os.path.join(CODE_DIR, pkl_file)
        try:
            # Try to load with pickle
            with open(pkl_path, 'rb') as f:
                test_preproc = pickle.load(f)
            if hasattr(test_preproc, 'transform'):
                unified_preproc = test_preproc
                print(f"\n✓ Using {crop} as unified preprocessor")
                break
        except:
            pass
    
    if unified_preproc:
        unified_path = os.path.join(CODE_DIR, 'preprocessor.pkl')
        with open(unified_path, 'wb') as f:
            pickle.dump(unified_preproc, f)
        print(f"✓ Saved unified preprocessor to: {unified_path}")
        return True
    else:
        print("\n✗ Failed to create unified preprocessor")
        return False

if __name__ == '__main__':
    success = verify_and_fix_preprocessors()
    print("\n" + "=" * 60)
    if success:
        print("✓ PREPROCESSOR FIX COMPLETE")
        print("You can now run: python code_1/app_new.py")
    else:
        print("✗ PREPROCESSOR FIX FAILED")
        print("Please check your training data and notebooks")
    print("=" * 60)
