import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

def main():
    print("--- Starting Mobile Price Analysis Pipeline ---")

    # 1. Define Paths (Dynamic Path Handling)
    # This helps find the data folder whether you run from root or src
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    input_file = os.path.join(data_dir, 'Mobile Price Dataset.xlsx')
    output_file = os.path.join(data_dir, 'Cleaned_Mobile_Price_Dataset.csv')

    # 2. Load Data
    if not os.path.exists(input_file):
        print(f"Error: Dataset not found at {input_file}")
        return

    data = pd.read_excel(input_file)
    print("✅ Data Loaded Successfully.")

    # 3. Data Cleaning
    print("🧹 Cleaning Data...")
    
    # Fill Categorical Missing Values (Mode)
    categorical_cols = ['blue', 'dual_sim', 'four_g', 'wifi', 'price_range']
    for col in categorical_cols:
        if col in data.columns:
            data[col].fillna(data[col].mode()[0], inplace=True)

    # Fill Numerical Missing Values (Median)
    num_cols = ['battery_power', 'clock_speed', 'int_memory', 'mobile_wt', 
                'n_cores', 'pc', 'px_height', 'px_width', 'ram', 'sc_h', 'sc_w']
    for col in num_cols:
        if col in data.columns:
            data[col].fillna(data[col].median(), inplace=True)
            data[col].replace(0, data[col].median(), inplace=True)

    # Remove Duplicates
    initial_rows = len(data)
    data.drop_duplicates(inplace=True)
    print(f"   - Removed {initial_rows - len(data)} duplicate rows.")

    # 4. Outlier Treatment (IQR)
    print("🔧 Handling Outliers...")
    for col in ['n_cores', 'px_height']:
        if col in data.columns:
            q1 = data[col].quantile(0.25)
            q3 = data[col].quantile(0.75)
            iqr = q3 - q1
            upper = q3 + 1.5 * iqr
            data[col] = np.where(data[col] > upper, upper, data[col])

    # 5. Save Data
    data.to_csv(output_file, index=False)
    print(f"✅ Cleaned data saved to: {output_file}")
    print("--- Pipeline Finished Successfully ---")

if __name__ == "__main__":
    main()