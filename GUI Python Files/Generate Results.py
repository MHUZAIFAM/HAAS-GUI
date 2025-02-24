import pandas as pd
import joblib
import time
import sklearn
from openpyxl import Workbook


# Load the test dataset
file_path = "Combined_Data.csv"  # Replace with your dataset path

data = pd.read_csv(file_path)

# Extract relevant columns for all 6 tests + Age & Gender
test_data = {
    "SFB": data[["Seated Forward Bench Test (cm)", "Age", "Gender"]],
    "FRT": data[["Functional Reach Test (cm)", "Age", "Gender"]],
    "TUG": data[["Time Up and Go Test (s)", "Age", "Gender"]],
    "WS": data[["Walking Speed Test (s)", "Age", "Gender"]],
   # "GS": data[["Grip Strength (kg)", "Age", "Gender"]],
    "SOOLWEO": data[["Standing on One Leg with Eye Open (s)", "Age", "Gender"]]
}

# Encode Gender column (convert 'Male' -> 0, 'Female' -> 1)
for test in test_data:
    test_data[test].loc[:, "Gender"] = test_data[test]["Gender"].map({"Male": 0, "Female": 1})
print("error")
# Load saved scalers and label encoders
scalers = {
    "SFB": joblib.load("Scaler_SFB.pkl"),
    "FRT": joblib.load("Scaler_FRT.pkl"),
    "TUG": joblib.load("Scaler_TUG.pkl"),
    "WS": joblib.load("Scaler_WS.pkl"),
   # "GS": joblib.load("Scaler_GS.pkl"),
    "SOOLWEO": joblib.load("Scaler_SOOLWEO.pkl"),
}
print ("scalers loaded")

label_encoders = {
    "SFB": joblib.load("Label_Encoder_SFB.pkl"),
    "FRT": joblib.load("Label_Encoder_FRT.pkl"),
    "TUG": joblib.load("Label_Encoder_TUG.pkl"),
    "WS": joblib.load("Label_Encoder_WS.pkl"),
   # "GS": joblib.load("Label_Encoder_GS.pkl"),
    "SOOLWEO": joblib.load("Label_Encoder_SOOLWEO.pkl"),
}
print ("scalers loaded")
# Load best models for all tests
models = {
    "SFB": joblib.load('Random_Forest_SFB.pkl'),
    "FRT": joblib.load('K-Nearest_Neighbors_FRT.pkl'),
    "TUG": joblib.load('K-Nearest_Neighbors_TUG.pkl'),
    "WS": joblib.load('Random_Forest_WS.pkl'),
    #"GS": joblib.load('XGBoost_GS.pkl'),
    "SOOLWEO": joblib.load('Random_Forest_SOOLWEO.pkl'),
}
print ("scalers loaded")
# Align columns with the scaler expectations
for test in test_data:
    test_data[test] = test_data[test].reindex(columns=scalers[test].feature_names_in_, fill_value=0)

# Standardize the test data
test_data_scaled = {test: scalers[test].transform(test_data[test]) for test in test_data}

# Initialize a DataFrame for storing predictions
predictions_df = data.copy()

# Initialize computational costs dictionary
computational_costs = {}

# Predict for each test and store results
for test_name, model in models.items():
    start_time = time.time()
    batch_predictions = model.predict(test_data_scaled[test_name])  # Predict
    end_time = time.time()

    # Convert numerical predictions to original labels
    predictions_df[f"{test_name} Prediction"] = label_encoders[test_name].inverse_transform(batch_predictions)

    # Measure computational cost
    computational_costs[test_name] = {
        "Time per example (average)": (end_time - start_time) / len(test_data[test_name]),
        "Total time (whole dataset)": end_time - start_time
    }

# Save combined predictions
output_file_path = "data.csv"
predictions_df.to_csv(output_file_path, index=False)

print(f"\nPredictions saved to: {output_file_path}")
