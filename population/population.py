import numpy as np
import pandas as pd
import os

# Path to the population data file. Update with the actual file path.
POPULATION_DATA_PATH = "nunavut_population_data.pkl"

# Path to the household data file. Update with the actual file path.
HOUSEHOLD_DATA_PATH = "nunavut_household_data.pkl"

AGE_GROUP_MAPPING = {
    "adult_list": ["20t29", "30t39", "40t49", "50t64", "65A"],  # Age ranges for adults
    "children_list": ["U14", "14t19"],  # Age range for children
}

print(HOUSEHOLD_DATA_PATH)
print(os.path.abspath(HOUSEHOLD_DATA_PATH))  # This will print the absolute path
print(os.path.exists(HOUSEHOLD_DATA_PATH))

# Load household data
HOUSEHOLD_DATA = pd.read_pickle(HOUSEHOLD_DATA_PATH)

# Load population data
BASE_POPULATION_DATA = pd.read_pickle(POPULATION_DATA_PATH)