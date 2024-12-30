import pandas as pd

# Input file large dataset
input_file = "E:/dsapro/Dataset.csv"  
output_file = "Dataset50Krows.csv" 

# Read the first 50,000 rows of the CSV
try:
    df = pd.read_csv(input_file, nrows=50000)
    # Save the data to a new CSV file without any changes
    df.to_csv(output_file, index=False)
    print(f"Successfully saved the first 50,000 rows to '{output_file}'.")
except Exception as e:
    print(f"An error occurred: {e}")
