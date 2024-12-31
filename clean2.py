import pandas as pd
import string

# Function to remove punctuation from words
def remove_punctuation_from_words(df, column_name='word'):
    # Create a translation table for removing punctuation
    translator = str.maketrans('', '', string.punctuation)
    
    # Remove punctuation from each word in the specified column
    df[column_name] = df[column_name].apply(lambda x: x.translate(translator) if isinstance(x, str) else x)
    
    return df

# Read the CSV file
file_path = 'derived_lexicon.csv'  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Clean the words in the 'word' column by removing punctuation
df_cleaned = remove_punctuation_from_words(df)

# Save the cleaned data back to a new CSV file
output_file_path = 'cleaned_output_file.csv'  # Output file path
df_cleaned.to_csv(output_file_path, index=False)

print(f"Cleaned data has been saved to {output_file_path}")
