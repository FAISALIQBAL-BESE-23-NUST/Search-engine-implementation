import pandas as pd

# Read the CSV file
input_file = 'extracted_cleaned_columns.csv'  # Replace with your CSV file path
output_file = 'author_file.csv'  # Path for the output file

# Load the CSV into a pandas DataFrame
df = pd.read_csv(input_file)

# Split the 'authors' column by spaces and create a new list for the processed authors
split_authors = []

# Variable to track the last word added
last_added_word = None

for _, row in df.iterrows():
    authors = row['authors'].split()
    for i, author in enumerate(authors):
        # Avoid repetition of the same word at the end of the previous row
        if i > 0 and author == last_added_word:
            continue
        # If it's the first word, keep it in the current row
        split_authors.append({'authors': author})
        last_added_word = author  # Update the last added word

# Create a new DataFrame from the processed authors list
split_df = pd.DataFrame(split_authors)

# Optionally, you can add other columns from the original df if needed
# split_df['other_column'] = df['other_column'].repeat(len(split_authors)//len(df))

# Write the result to a new CSV
split_df.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")
