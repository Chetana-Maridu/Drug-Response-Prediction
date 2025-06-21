# train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Generate synthetic data
n = 1000
np.random.seed(0)

# Features
drug_id = np.random.choice([0, 1, 2, 3, 4], size=n)
dosage = np.random.randint(1, 101, size=n)
age = np.random.randint(18, 80, size=n)
bmi = np.round(np.random.normal(25, 5, size=n), 2)
condition_indicator = np.random.choice([0, 1], size=n)

# Target
response_efficiency = (
    20 * drug_id +
    0.3 * dosage +
    0.1 * age -
    0.5 * bmi +
    5 * condition_indicator +
    np.random.normal(0, 10, size=n)
)
response_efficiency = np.clip(response_efficiency, 0, 100)

# DataFrame
data = pd.DataFrame({
    'drug_id': drug_id,
    'dosage': dosage,
    'age': age,
    'bmi': bmi,
    'condition_indicator': condition_indicator,
    'response_efficiency': response_efficiency
})

# Save dataset
data.to_csv('synthetic_drug_response_data.csv', index=False)

# Split data
X = data[['drug_id', 'dosage', 'age', 'bmi', 'condition_indicator']]
y = data['response_efficiency']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluate and save model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Model trained with Mean Squared Error: {mse}")
joblib.dump(model, 'drug_response_model.pkl')
print("Model saved as 'drug_response_model.pkl'")