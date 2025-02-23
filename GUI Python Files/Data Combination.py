import pandas as pd
import os

# File names
patient_data_file = "Patient_Data.csv"
functional_reach_file = "Functional_Reach_Test_Results.csv"
standing_one_leg_file = "Standing_on_One_Leg_with_Eye_Open_Test_Results.csv"
walking_speed_file = "Walking_Speed_Test_Results.csv"
time_up_go_file = "Time_Up_and_Go_Test_Results.csv"
seated_forward_bend_file = "Seated_Forward_Bend_Test_Results.csv"
combined_data_file = "Combined_Data.csv"

# Read patient data
patient_data = pd.read_csv(patient_data_file)

# Determine next ID to process
if os.path.exists(combined_data_file):
    combined_data = pd.read_csv(combined_data_file)
    processed_ids = set(combined_data["ID"])
else:
    combined_data = pd.DataFrame()
    processed_ids = set()

for index, row in patient_data.iterrows():
    patient_id = row["ID"]
    if patient_id in processed_ids:
        continue  # Skip already processed IDs

    age = row["Age"]
    gender = row["Gender"]

    # Read Functional Reach Test
    func_reach = pd.read_csv(functional_reach_file)
    max_func_reach = func_reach.iloc[index, 2]  # Third column, max of first two rows

    # Read Standing on One Leg Test
    standing_one_leg = pd.read_csv(standing_one_leg_file)
    max_standing_one_leg = standing_one_leg.iloc[index, 2]  # Third column, max of first two rows

    # Read Walking Speed Test
    walking_speed = pd.read_csv(walking_speed_file)
    max_walking_speed = max(walking_speed.iloc[index, 0], walking_speed.iloc[index + 1, 0])

    # Read Time Up and Go Test
    time_up_go = pd.read_csv(time_up_go_file)
    max_time_up_go = max(time_up_go.iloc[index, 0], time_up_go.iloc[index + 1, 0])

    # Read Seated Forward Bend Test
    seated_forward_bend = pd.read_csv(seated_forward_bend_file)
    max_seated_forward_bend = seated_forward_bend.iloc[index, 2]  # Third column, max of first two rows

    # Append data to combined dataframe
    new_row = pd.DataFrame([{
        "ID": patient_id,
        "Age": age,
        "Gender": gender,
        "Functional Reach Test (cm)": max_func_reach,
        "Standing on One Leg with Eye Open (s)": max_standing_one_leg,
        "Walking Speed Test (s)": max_walking_speed,
        "Time Up and Go Test (s)": max_time_up_go,
        "Seated Forward Bench Test (cm)": max_seated_forward_bend
    }])

    # Save row to CSV (append mode)
    new_row.to_csv(combined_data_file, mode='a', header=not os.path.exists(combined_data_file), index=False)
    print(f"Processed ID: {patient_id}")
    break  # Process one row per run
