import numpy as np
import pandas as pd
import pickle
from dotenv import load_dotenv
import os
import warnings

# Load environment variables
load_dotenv()

# Suppress the specific sklearn warning
warnings.filterwarnings('ignore', message='X does not have valid feature names')

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load models and preprocessor
try:
    Jmodel = pickle.load(open(os.path.join(SCRIPT_DIR, 'jmodel.pkl'), 'rb'))
    Wmodel = pickle.load(open(os.path.join(SCRIPT_DIR, 'wmodel.pkl'), 'rb'))
    Cmodel = pickle.load(open(os.path.join(SCRIPT_DIR, 'cmodel.pkl'), 'rb'))
    Smodel = pickle.load(open(os.path.join(SCRIPT_DIR, 'smodel.pkl'), 'rb'))
    Bmodel = pickle.load(open(os.path.join(SCRIPT_DIR, 'bmodel.pkl'), 'rb'))
    preprocessor = pickle.load(open(os.path.join(SCRIPT_DIR, 'preprocessor.pkl'), 'rb'))
    print("✓ All models and preprocessor loaded successfully!")
except FileNotFoundError as e:
    print(f"Error loading model files: {e}")
    print("Please ensure all .pkl files are in the same directory as this script.")
    exit(1)

# Commodity details (model, MSP range)
commodity_info = {
    "jowar":     {"model": Jmodel, "min_msp": 1550, "max_msp": 2970},
    "wheat":     {"model": Wmodel, "min_msp": 1350, "max_msp": 2125},
    "cotton":    {"model": Cmodel, "min_msp": 3600, "max_msp": 6080},
    "sugarcane": {"model": Smodel, "min_msp": 2250, "max_msp": 2775},
    "bajara":    {"model": Bmodel, "min_msp": 1175, "max_msp": 2350}
}

def display_welcome():
    print("="*60)
    print("🌾 CROP PRICE PREDICTION SYSTEM 🌾")
    print("="*60)
    print("Available commodities:")
    for i, commodity in enumerate(commodity_info.keys(), 1):
        print(f"{i}. {commodity.capitalize()}")
    print("="*60)

def get_user_input():
    """Get input from user with validation"""
    
    # Get commodity
    while True:
        commodity = input("\nEnter commodity name: ").lower().strip()
        if commodity in commodity_info:
            break
        else:
            print(f" Invalid commodity! Please choose from: {', '.join(commodity_info.keys())}")
    
    # Get month
    while True:
        try:
            month = int(input("Enter month (1-12): "))
            if 1 <= month <= 12:
                break
            else:
                print(" Month must be between 1 and 12!")
        except ValueError:
            print(" Please enter a valid number for month!")
    
    # Get year
    while True:
        try:
            year = int(input("Enter year (e.g., 2024): "))
            if year > 0:
                break
            else:
                print(" Please enter a valid year!")
        except ValueError:
            print(" Please enter a valid number for year!")
    
    # Get rainfall
    while True:
        try:
            rainfall = float(input("Enter rainfall (mm): "))
            if rainfall >= 0:
                break
            else:
                print(" Rainfall cannot be negative!")
        except ValueError:
            print(" Please enter a valid number for rainfall!")
    
    return commodity, month, year, rainfall

def predict_price(commodity, month, year, rainfall):
    """Make price prediction"""
    
    # Create DataFrame with proper feature names (these must match the training data)
    feature_names = ['Month', 'Year', 'Rainfall']  # Capitalized as per training data
    
    # Create DataFrame instead of numpy array
    features_df = pd.DataFrame([[month, year, rainfall]], columns=feature_names)
    
    # Transform using preprocessor
    transformed = preprocessor.transform(features_df)

    model = commodity_info[commodity]["model"]
    min_msp = commodity_info[commodity]["min_msp"]
    max_msp = commodity_info[commodity]["max_msp"]

    # Predict
    prediction = model.predict(transformed).reshape(1, -1)
    predicted_index = round(prediction[0][0], 3)

    min_price = round((predicted_index * min_msp) / 100, 2)
    max_price = round((predicted_index * max_msp) / 100, 2)
    avg_price = round((min_price + max_price) / 2, 2)

    return predicted_index, min_price, max_price, avg_price

def display_results(commodity, month, year, rainfall, predicted_index, min_price, max_price, avg_price):
    """Display prediction results"""
    
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    
    print("\n" + "="*60)
    print(" PREDICTION RESULTS")
    print("="*60)
    print(f"Commodity: {commodity.capitalize()}")
    print(f"Month: {month_names[month]} ({month})")
    print(f"Year: {year}")
    print(f"Rainfall: {rainfall} mm")
    print("-"*40)
    print(f"Predicted Index: {predicted_index}")
    print(f"Price Range: ₹{min_price} - ₹{max_price}")
    print(f"Average Price: ₹{avg_price}")
    print("="*60)

def main():
    """Main application loop"""
    
    display_welcome()
    
    while True:
        try:
            # Get user input
            commodity, month, year, rainfall = get_user_input()
            
            # Make prediction
            predicted_index, min_price, max_price, avg_price = predict_price(
                commodity, month, year, rainfall
            )
            
            # Display results
            display_results(
                commodity, month, year, rainfall,
                predicted_index, min_price, max_price, avg_price
            )
            
            # Ask if user wants to continue
            while True:
                choice = input("\nDo you want to make another prediction? (y/n): ").lower().strip()
                if choice in ['y', 'yes']:
                    print("\n" + "-"*60)
                    break
                elif choice in ['n', 'no']:
                    print("\nThank you for using the Crop Price Prediction System! 🌾")
                    return
                else:
                    print(" Please enter 'y' for yes or 'n' for no.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n An error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()