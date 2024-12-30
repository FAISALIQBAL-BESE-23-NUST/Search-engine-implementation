import pandas as pd

# Paths to the input and output CSV files
input_file = 'updated_with_authors.csv'  # Replace with your CSV file path
output_root_lexicon = 'root_lexicon.csv'  # Output CSV for root_word lexicon
output_derived_lexicon = 'derived_lexicon.csv'  # Output CSV for derived_words lexicon

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(input_file)

# Function to create lexicon from a column
def create_lexicon(column_data):
    words = set()
    for entry in column_data:
        # Ensure the entry is treated as a string before splitting
        entry = str(entry)  # Convert entry to string
        words.update(entry.split())  # Split and add each word to the set
    
    # Create a dictionary that maps words to unique IDs
    word_to_id = {word: idx + 1 for idx, word in enumerate(sorted(words))}
    
    return word_to_id

# Create lexicons for both 'root_word' and 'derived_words' columns
root_lexicon = create_lexicon(df['root_word'])
derived_lexicon = create_lexicon(df['derived_words'])

# Convert lexicons into DataFrames for easy export to CSV
root_lexicon_df = pd.DataFrame(list(root_lexicon.items()), columns=['word', 'id'])
derived_lexicon_df = pd.DataFrame(list(derived_lexicon.items()), columns=['word', 'id'])

# Sort lexicons alphabetically by the word column
root_lexicon_df = root_lexicon_df.sort_values(by='word', ascending=True)
derived_lexicon_df = derived_lexicon_df.sort_values(by='word', ascending=True)

# Save the lexicons to separate CSV files
root_lexicon_df.to_csv(output_root_lexicon, index=False)
derived_lexicon_df.to_csv(output_derived_lexicon, index=False)

print(f"Root lexicon saved to {output_root_lexicon}")
print(f"Derived lexicon saved to {output_derived_lexicon}")
