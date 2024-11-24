import pandas as pd
import random
import pickle
from numpy.random import choice
import itertools

areas = {
    'X0A0A0': 0, 'X0A0B0': 1, 'X0A0C0': 2, 'X0A0E0': 3, 'X0A0G0': 4, 
    'X0A0H0': 5, 'X0A0J0': 6, 'X0A0K0': 7, 'X0A0L0': 8, 'X0A0N0': 9,
    'X0A0R0': 10, 'X0A0S0': 11, 'X0A0V0': 12, 'X0A0W0': 13, 'X0A1H0': 14,
    'X0A2H0': 15, 'X0A3H0': 16, 'X0B0C0': 17, 'X0B0E0': 18, 'X0B1B0': 19,
    'X0B1J0': 20, 'X0B1K0': 21, 'X0B2A0': 22, 'X0C0A0': 23, 'X0C0B0': 24,
    'X0C0C0': 25, 'X0C0E0': 26, 'X0C0G0': 27, 'X0C0H0': 28, 'X0C0J0': 29
}
genders = {'female': 0, 'male': 1}
age_groups = ['U14', '15t19', '20t29', '30t39', '40t49', '50t59', '60plus']


combinations = list(itertools.product(areas.keys(), genders.keys(), age_groups))

gender_percentages = {'female': 0.5, 'male': 0.5}
age_group_percentages = {'U14': 0.328, '15t19': 0.084, '20t29': 0.159, '30t39':0.146, '40t49': 0.109, '50t59':0.098, '60plus':0.076}

total_population = 2300

age_gender_df = pd.DataFrame(combinations, columns=['area', 'gender', 'age'])

age_gender_df["count"] = age_gender_df.apply(
    lambda row: (
        0.03333333 *
        gender_percentages[row["gender"]] *
        age_group_percentages[row["age"]] *
        total_population),
        axis=1
    )

age_gender_df["count"] = age_gender_df["count"].astype(int)

age_gender_df["region"] = 'NU'

ethnicity = ['Inuit', 'European', 'Caucasian', 'Canadian', 'English', 'Irish', 'Scottish', 'French', 'German', 'Other']
combinations_2 = list(itertools.product(areas.keys(), ethnicity))

ethnicity_percentages = {'Inuit': 0.839, 'European': 0.011, 'Caucasian': 0.017, 'Canadian': 0.028, 'English':0.038, 'Irish':0.043, 'Scottish':0.057, 'French':0.024, 'German':0.017, 'Other':0.074}

ethnicity_df = pd.DataFrame(combinations_2, columns=['area', 'ethnicity'])

ethnicity_df["count"] = ethnicity_df.apply(
    lambda row: (
        ethnicity_percentages[row["ethnicity"]] *
        0.033333333333 *
        total_population),
        axis=1
    )

ethnicity_df["count"] = ethnicity_df["count"].astype(int)

ethnicity_df["region"] = 'NU'

population_data = {
    'age_gender': age_gender_df,
    'ethnicity': ethnicity_df
}

# Replace area and gender with integer values
age_gender_df['area'] = age_gender_df['area'].map(areas)
age_gender_df['gender'] = age_gender_df['gender'].map(genders)

# Map age ranges to their middle values
age_mapping = {
    'U14': 7,
    '15t19': 17, 
    '20t29': 25,
    '30t39': 35,
    '40t49': 45,
    '50t59': 55,
    '60plus': 65
}

# Convert age ranges to numeric values using the mapping
age_gender_df['age'] = age_gender_df['age'].map(age_mapping)

# Update the population_data dictionary with encoded dataframe
population_data['age_gender'] = age_gender_df

print(population_data['age_gender'].loc[0])

# Repeat rows based on count value
expanded_df = age_gender_df.loc[age_gender_df.index.repeat(age_gender_df['count'])]

# Reset index after expansion
expanded_df = expanded_df.reset_index(drop=True)

# Create separate dataframes for each attribute
area_df = expanded_df[['area']]
gender_df = expanded_df[['gender']] 
age_df = expanded_df[['age']]

print(area_df.loc[0])
print(gender_df.loc[0])
print(age_df.loc[0])

print(f"Total population after expansion: {len(expanded_df)}") #22740

output_path = '/home/ubuntu/flow/population/Nunavut/area.pickle'
with open(output_path, 'wb') as f:
    pickle.dump(area_df, f)

output_path = '/home/ubuntu/flow/population/Nunavut/gender.pickle'
with open(output_path, 'wb') as f:
    pickle.dump(gender_df, f)

output_path = '/home/ubuntu/flow/population/Nunavut/age.pickle'
with open(output_path, 'wb') as f:
    pickle.dump(age_df, f)