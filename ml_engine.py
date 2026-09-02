import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def calculate_collectability(amount, error_code, historical_success_rate):
    """
    Trains a quick Random Forest model on dummy historical patterns
    and returns a probability score (0-100%) for a given invoice.
    """
    # 1. Generate structured dummy training features
    np.random.seed(42)
    n_samples = 500
    
    # Feature 1: Invoice Amount (numeric)
    X_amount = np.random.uniform(50, 5000, n_samples)
    
    # Feature 2: Error Code mapped to numeric weight
    # 0: Insufficient Funds, 1: Card Expired, 2: Bank Decline
    X_error = np.random.choice([0, 1, 2], size=n_samples, p=[0.5, 0.3, 0.2])
    
    # Feature 3: Past success rate (0.0 to 1.0)
    X_history = np.random.uniform(0, 1, n_samples)
    
    X_train = pd.DataFrame({
        'amount': X_amount,
        'error_code': X_error,
        'history': X_history
    })
    
    # Target Variable: 1 = Recovered, 0 = Lost
    # Formulate a simple rule for the dummy target so the model actually learns a clear pattern
    y_train = np.where((X_history > 0.4) & (X_error != 2) & (X_amount < 3000), 1, 0)
    
    # 2. Train the Machine Learning Model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    
    # 3. Process the runtime single input
    error_mapping = {"Insufficient Funds": 0, "Card Expired": 1, "Bank Decline": 2}
    error_numeric = error_mapping.get(error_code, 0)
    
    input_data = pd.DataFrame([{
        'amount': float(amount.replace('$', '').replace(',', '')),
        'error_code': error_numeric,
        'history': float(historical_success_rate)
    }])
    
    # Predict the probability of recovery (class 1)
    probability = model.predict_proba(input_data)[0][1]
    
    return int(probability * 100)
