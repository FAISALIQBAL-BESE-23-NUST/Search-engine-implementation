import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Define input and output file paths
input_file = "ExtractedCleanedColumns.csv"  # Replace with your input file path
output_file = "Lexicon.csv"  # Replace with your desired output file path

# Initialize lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Function to clean and tokenize text
def clean_and_tokenize(text):
    if pd.isnull(text):
        return []
    # Remove punctuation except dots between words
    text = re.sub(r'(?<!\S)\.(?!\S)', ' ', text)
    text = re.sub(r'["!?,;:\[\]{}()<>]', '', text)
    text = text.lower()  # Convert to lowercase
    tokens = text.split()  # Split into words
    return tokens

# Process the dataset and build the lexicon
def build_lexicon(input_file, output_file):
    try:
        # Read the input CSV
        df = pd.read_csv(input_file)
        total_rows = len(df)

        # Columns to process
        columns_to_process = ['title', 'tags', 'authors', 'text']

        # Dictionary to store unique words and their IDs
        word_dict = {}
        current_id = 1
        processed_rows = 0

        for col in columns_to_process:
            if col in df.columns:
                for text in df[col]:
                    words = clean_and_tokenize(text)
                    for word in words:
                        if word not in stop_words:
                            root_word = lemmatizer.lemmatize(word)

                            # Add root word if not already added
                            if root_word not in word_dict:
                                word_dict[root_word] = current_id
                                current_id += 1

                            # Add the actual word if not already added
                            if word not in word_dict:
                                word_dict[word] = current_id
                                current_id += 1
                    
                    # Track progress
                    processed_rows += 1
                    if processed_rows % 100 == 0:
                        print(f"Processed {processed_rows}/{total_rows} rows...")

        # Convert the dictionary to a DataFrame and sort it
        lexicon_df = pd.DataFrame(word_dict.items(), columns=['Word', 'Word ID'])
        lexicon_df.sort_values(by='Word', inplace=True)

        # Save to CSV
        lexicon_df.to_csv(output_file, index=False)
        print(f"Lexicon successfully saved to '{output_file}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Execute the lexicon building
build_lexicon(input_file, output_file)
