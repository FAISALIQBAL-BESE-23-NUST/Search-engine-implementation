import os
import pandas as pd
from collections import Counter
from nltk.stem import WordNetLemmatizer
import nltk

# Ensure necessary NLTK data files are downloaded
nltk.download("wordnet")
nltk.download("omw-1.4")

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

def lemmatize_word(word):
    """
    Lemmatize a word to its base form using NLTK's WordNetLemmatizer.
    """
    return lemmatizer.lemmatize(word.lower())

def process_chunks_and_save(directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # List all CSV files in the directory
    chunk_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    chunk_files.sort()  # Ensure files are processed in alphabetical order

    # Check if there are any chunk files
    if not chunk_files:
        print("No CSV files found in the directory. Please check the path.")
        return

    # Process each chunk
    for chunk_file in chunk_files:
        print(f"Processing {chunk_file}...")
        file_path = os.path.join(directory, chunk_file)

        try:
            # Load the chunk
            df = pd.read_csv(file_path)
            if df.empty:
                print(f"{chunk_file} is empty. Skipping.")
                continue

            # Combine text from all text-based columns
            text_data = []
            for column in df.columns:
                if df[column].dtype == 'object':  # Check if the column contains strings
                    text_data.extend(df[column].dropna().astype(str).tolist())

            # Build a lexicon
            chunk_lexicon = Counter()
            for text in text_data:
                # Tokenize and lemmatize
                tokens = [lemmatize_word(word) for word in text.split() if word.isalpha()]  # Filter non-alphabetic tokens
                chunk_lexicon.update(tokens)

            # Prepare the lexicon data
            sorted_words = sorted(chunk_lexicon.items(), key=lambda x: x[0])  # Sort words alphabetically
            lexicon_data = {
                "Word ID": list(range(1, len(sorted_words) + 1)),
                "Word": [word for word, _ in sorted_words],
                "Frequency": [freq for _, freq in sorted_words]
            }
            lexicon_df = pd.DataFrame(lexicon_data)

            # Save the lexicon to a CSV file
            output_file = os.path.join(output_directory, f"{os.path.splitext(chunk_file)[0]}_lexicon.csv")
            lexicon_df.to_csv(output_file, index=False)
            print(f"Lexicon for {chunk_file} saved to {output_file}")

        except Exception as e:
            print(f"Error processing {chunk_file}: {e}")

    print("All chunks processed and saved.")

# Directory containing the chunk files
input_directory = "E:/dsapro/DatasetChunks"

# Directory to save the lexicons
output_directory = "E:/dsapro/Lexiconall"

# Run the function
process_chunks_and_save(input_directory, output_directory)
