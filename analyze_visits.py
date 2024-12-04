import pandas as pd
import random

# Use this function to calculate the cost with different insurances
def calculate_cost(row):
        base_cost = 1000
        # The better the insurance, the less money people pay
        insurance_modifiers = {
            "Basic": 1.0,
            "Premium": 0.7,
            "Platimum": 0.5,
            "Deluxe_Premium": 0.3,
            "Ultimate": 0.1
        }
        modifier = insurance_modifiers.get(row['insurance_type'], 1.0)
        # Add some variation between users using the same insurance
        variation = random.uniform(-50, 50)
        return round(base_cost * modifier + variation, 2)

def main():
    my_pd = pd.read_csv("ms_data.csv")
    # Structure the data
    # Read data in CSV format
    # Tell panda what datatype panda should treat each column
    # Sort the data by ID and Date
    myData = pd.read_csv("ms_data.csv")
    myData['visit_date'] = pd.to_datetime(myData['visit_date'])
    myData['patient_id'] = myData['patient_id'].astype(str)
    myData['age'] = pd.to_numeric(myData['age'])  
    myData['education_level'] = myData['education_level'].astype('category')  
    myData['walking_speed'] = pd.to_numeric(myData['walking_speed'])
    myData = myData.sort_values(by=['patient_id', 'visit_date'])

    # Read insurance types from insurance.lst file
    with open("insurance.lst", "r") as ins:
        insurance_types = [line.strip() for line in ins if line.strip()]

    # Assign insurances randomly to the patients(Ensure patient with the same ID will have the same insurance type)
    unique_patient_ID = myData['patient_id'].unique()
    patient_insurance = {patient_id: random.choice(insurance_types) for patient_id in unique_patient_ID}
    myData['insurance_type'] = myData['patient_id'].map(patient_insurance)

    myData['visit_cost'] = myData.apply(calculate_cost, axis=1)

    # Print or save the updated data
    myData.to_csv("ms_data.csv", index=False)

    # Mean speed by education 
    mean_speed_by_education = myData.groupby('education_level', observed=False)['walking_speed'].mean()
    print("The mean speed by education is:")
    print(mean_speed_by_education.reset_index())
    
    # Mean costs by different insurances
    mean_cost_by_insurance = myData.groupby('insurance_type')['visit_cost'].mean()
    print("\nThe mean costs by differnet insurances:")
    print(mean_cost_by_insurance.reset_index())
    
    # Calculate the correlation to find the relationship between age and walking speed
    correlation = myData[['age', 'walking_speed']].corr().iloc[0, 1]

    # Print the results
    print("\nAge Effects on Walking Speed:")
    print(f"correlation is {correlation: .2f}")
    if correlation < 0:
        print(f"Age increases, walking speed decreases.")
    elif correlation > 0:
        print(f"Age increases, walking speed increase.")
    else:
        print("There is no relationship between age and walking speed.")

if __name__ == "__main__":
    main()

