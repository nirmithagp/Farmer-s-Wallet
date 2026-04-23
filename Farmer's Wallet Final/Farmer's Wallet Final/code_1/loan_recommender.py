"""
Loan Recommendation Module
Integrates the XGBoost-based loan recommendation system
"""
import sys
import os
import pickle
import pandas as pd
import numpy as np

# Add the loan recommender path
LOAN_RECOMMENDER_PATH = os.path.join(os.path.dirname(__file__), '..', 'farmer_Loan_recommender-main')
sys.path.insert(0, LOAN_RECOMMENDER_PATH)

class LoanRecommender:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.load_model()
    
    def load_model(self):
        """Load the trained XGBoost model and encoders"""
        try:
            # Try to load the model if it exists
            model_path = os.path.join(LOAN_RECOMMENDER_PATH, 'loan_model.pkl')
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
            
            # Load label encoders if they exist
            encoder_path = os.path.join(LOAN_RECOMMENDER_PATH, 'label_encoders.pkl')
            if os.path.exists(encoder_path):
                with open(encoder_path, 'rb') as f:
                    self.label_encoders = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            self.model = None
    
    def get_recommendations(self, crop_type, land_type, location, land_size, income):
        """
        Get loan recommendations based on farmer details
        
        Parameters:
        - crop_type: Type of crop being grown
        - land_type: Type of land (Irrigated, Dryland, etc.)
        - location: District/Location
        - land_size: Size of land in acres
        - income: Annual income
        
        Returns:
        - List of recommended loans with probabilities
        """
        try:
            # Ensure inputs are correct types
            income = float(income)
            land_size = float(land_size)

            if self.model is None:
                # Return default recommendations if model not loaded
                return self._get_default_recommendations(crop_type, land_type, income)
            
            # Prepare input data
            input_data = pd.DataFrame({
                'CropType': [crop_type],
                'LandType': [land_type],
                'Location': [location],
                'LandSize': [land_size],
                'Income': [income]
            })
            
            # Encode categorical variables
            for col in ['CropType', 'LandType', 'Location']:
                if col in self.label_encoders:
                    input_data[col] = self.label_encoders[col].transform(input_data[col])
            
            # Get predictions
            predictions = self.model.predict_proba(input_data)[0]
            loan_names = self.model.classes_
            
            # Get top 3 recommendations
            top_indices = np.argsort(predictions)[-3:][::-1]
            
            recommendations = []
            for idx in top_indices:
                recommendations.append({
                    'loan_name': loan_names[idx],
                    'probability': float(predictions[idx]),
                    'confidence': f"{predictions[idx]*100:.1f}%"
                })
            
            return recommendations
            
        except Exception as e:
            print(f"Error in get_recommendations: {e}")
            return self._get_default_recommendations(crop_type, land_type, float(income) if income else 0)
    
    def _get_default_recommendations(self, crop_type, land_type, income):
        """Provide rule-based recommendations when model is not available"""
        recommendations = []
        
        # Rule-based logic
        if income < 30000:
            recommendations.append({
                'loan_name': 'PM Kisan Loan',
                'probability': 0.85,
                'confidence': '85.0%',
                'description': 'Low-interest loan for small farmers'
            })
            recommendations.append({
                'loan_name': 'Kisan Credit Card',
                'probability': 0.75,
                'confidence': '75.0%',
                'description': 'Flexible credit facility for farmers'
            })
        elif income < 50000:
            recommendations.append({
                'loan_name': 'Crop Loan',
                'probability': 0.80,
                'confidence': '80.0%',
                'description': 'Short-term loan for crop cultivation'
            })
            recommendations.append({
                'loan_name': 'Agricultural Term Loan',
                'probability': 0.70,
                'confidence': '70.0%',
                'description': 'Medium to long-term agricultural loan'
            })
        else:
            recommendations.append({
                'loan_name': 'Farm Mechanization Loan',
                'probability': 0.85,
                'confidence': '85.0%',
                'description': 'Loan for purchasing farm equipment'
            })
            recommendations.append({
                'loan_name': 'NABARD Loan',
                'probability': 0.75,
                'confidence': '75.0%',
                'description': 'Development loan from NABARD'
            })
        
        # Add a third option
        recommendations.append({
            'loan_name': 'Organic Farming Loan',
            'probability': 0.65,
            'confidence': '65.0%',
            'description': 'Special loan for organic farming'
        })
        
        return recommendations[:3]

# Global instance
loan_recommender = LoanRecommender()

def get_loan_recommendations(crop_type, land_type, location, land_size, income):
    """Wrapper function for easy import"""
    return loan_recommender.get_recommendations(crop_type, land_type, location, land_size, income)
