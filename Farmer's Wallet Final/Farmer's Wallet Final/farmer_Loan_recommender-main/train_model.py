"""
Loan Recommender Model Training Script
Trains and saves the XGBoost model for loan recommendations
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler


def generate_synthetic_dataset(n_samples=1000):
    """Generate synthetic loan dataset based on crop profiles"""
    
    crop_data = {
        "Rice": {
            "LoanName": ["Kisan Credit Card", "Crop Loan", "Irrigation Loan"],
            "Districts": ["Mandya", "Raichur", "Mysuru", "Shivamogga"],
            "LandTypes": ["Irrigated", "Wetland"],
            "IncomeRange": (30000, 40000),
            "LandSizeRange": (1.0, 4.0)
        },
        "Wheat": {
            "LoanName": ["Crop Loan", "PM Kisan Loan"],
            "Districts": ["Vijayapura", "Bagalkot", "Kalaburagi"],
            "LandTypes": ["Irrigated", "Dryland"],
            "IncomeRange": (25000, 35000),
            "LandSizeRange": (1.5, 5.0)
        },
        "Sugarcane": {
            "LoanName": ["Agricultural Term Loan", "Irrigation Loan", "Farm Mechanization Loan"],
            "Districts": ["Belagavi", "Mandya", "Mysuru"],
            "LandTypes": ["Irrigated", "Black cotton soil land"],
            "IncomeRange": (45000, 60000),
            "LandSizeRange": (2.0, 6.0)
        },
        "Cotton": {
            "LoanName": ["Crop Loan", "Kisan Credit Card"],
            "Districts": ["Haveri", "Gadag", "Dharwad", "Ballari"],
            "LandTypes": ["Black cotton soil land", "Dryland"],
            "IncomeRange": (30000, 45000),
            "LandSizeRange": (2.0, 5.0)
        },
        "Pulses": {
            "LoanName": ["PM Kisan Loan", "Organic Farming Loan"],
            "Districts": ["Bidar", "Dharwad"],
            "LandTypes": ["Rainfed", "Dryland"],
            "IncomeRange": (18000, 25000),
            "LandSizeRange": (1.0, 4.0)
        },
        "Millets": {
            "LoanName": ["Organic Farming Loan", "PM Kisan Loan"],
            "Districts": ["Chitradurga", "Ballari", "Tumakuru"],
            "LandTypes": ["Rainfed", "Dryland"],
            "IncomeRange": (15000, 22000),
            "LandSizeRange": (2.0, 6.0)
        }
    }
    
    records = []
    crops = list(crop_data.keys())
    
    for _ in range(n_samples):
        crop = np.random.choice(crops)
        crop_info = crop_data[crop]
        
        record = {
            "CropType": crop,
            "LandType": np.random.choice(crop_info["LandTypes"]),
            "Location": np.random.choice(crop_info["Districts"]),
            "LandSize": np.random.uniform(crop_info["LandSizeRange"][0], 
                                         crop_info["LandSizeRange"][1]),
            "Income": np.random.randint(crop_info["IncomeRange"][0], 
                                       crop_info["IncomeRange"][1]),
            "LoanName": np.random.choice(crop_info["LoanName"])
        }
        records.append(record)
    
    return pd.DataFrame(records)


def balance_dataset(df):
    """Balance the dataset using undersampling and oversampling"""
    
    features_to_balance = ['CropType', 'LandType', 'LoanName', 'Location']
    balanced_df = df.copy()
    
    for feature in features_to_balance:
        print(f"Balancing feature: {feature}")
        
        # Prepare data for sampling
        X = balanced_df.drop(columns=[feature])
        y = balanced_df[feature]
        
        # Undersample majority class
        under = RandomUnderSampler(sampling_strategy='auto', random_state=42)
        X_under, y_under = under.fit_resample(X, y)
        
        # Oversample minority classes
        over = RandomOverSampler(sampling_strategy='auto', random_state=42)
        X_balanced, y_balanced = over.fit_resample(X_under, y_under)
        
        # Merge back
        X_balanced[feature] = y_balanced
        balanced_df = X_balanced
    
    return balanced_df


def train_model(df):
    """Train XGBoost model with label encoders"""
    
    # Create label encoders
    le_land = LabelEncoder()
    le_location = LabelEncoder()
    le_crop = LabelEncoder()
    le_loan = LabelEncoder()
    
    # Encode categorical columns
    df['LandType'] = le_land.fit_transform(df['LandType'])
    df['Location'] = le_location.fit_transform(df['Location'])
    df['CropType'] = le_crop.fit_transform(df['CropType'])
    df['LoanName'] = le_loan.fit_transform(df['LoanName'])
    
    # Prepare features and target
    X = df[['LandType', 'LandSize', 'Location', 'CropType', 'Income']]
    y = df['LoanName']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train XGBoost model
    model = XGBClassifier(eval_metric='mlogloss', random_state=42, verbosity=1)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print("\nModel Performance:")
    print(classification_report(y_test, y_pred))
    
    return model, le_land, le_location, le_crop, le_loan


def save_model_and_encoders(model, encoders, output_dir="."):
    """Save the trained model and label encoders"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(output_dir, "loan_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Model saved to {model_path}")
    
    # Save encoders
    encoders_dict = {
        'LandType': encoders[0],
        'Location': encoders[1],
        'CropType': encoders[2],
        'LoanName': encoders[3]
    }
    
    encoders_path = os.path.join(output_dir, "label_encoders.pkl")
    with open(encoders_path, 'wb') as f:
        pickle.dump(encoders_dict, f)
    print(f"✓ Label encoders saved to {encoders_path}")


def main():
    """Main training pipeline"""
    
    print("="*60)
    print("🌾 LOAN RECOMMENDER MODEL TRAINER")
    print("="*60)
    
    # Generate synthetic dataset
    print("\n1️⃣ Generating synthetic dataset...")
    df = generate_synthetic_dataset(n_samples=2000)
    print(f"   Dataset shape: {df.shape}")
    
    # Balance dataset
    print("\n2️⃣ Balancing dataset...")
    df_balanced = balance_dataset(df)
    print(f"   Balanced dataset shape: {df_balanced.shape}")
    
    # Train model
    print("\n3️⃣ Training XGBoost model...")
    model, le_land, le_location, le_crop, le_loan = train_model(df_balanced)
    
    # Save model and encoders to script directory
    print("\n4️⃣ Saving model and encoders...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_model_and_encoders(model, (le_land, le_location, le_crop, le_loan), output_dir=script_dir)
    
    print("\n" + "="*60)
    print("✅ Training complete!")
    print("="*60)


if __name__ == "__main__":
    main()
