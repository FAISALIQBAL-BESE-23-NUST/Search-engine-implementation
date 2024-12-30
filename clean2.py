import os
import pandas as pd
import ast
import re

# Define cleaning functions
def clean_title(title):
    """Clean the title by removing extra whitespace and special characters."""
    return re.sub(r'[^a-zA-Z0-9\s]', '', title).strip().lower() if isinstance(title, str) else ""

def clean_authors(authors):
    """Clean the authors by converting to a standardized format."""
    if isinstance(authors, str):
        try:
            author_list = ast.literal_eval(authors)  # Convert string to list
            return ", ".join(author.strip().title() for author in author_list)
        except Exception:
            return authors.strip().title()  # Fallback for malformed data
    return ""

def clean_tags(tags):
    """Clean the tags by converting to lowercase and joining into a string."""
    if isinstance(tags, str):
        try:
            tag_list = ast.literal_eval(tags)  # Convert string to list
            return ", ".join(tag.strip().lower() for tag in tag_list)
        except Exception:
            return tags.strip().lower()  # Fallback for malformed data
    return ""

# Process each chunk
def process_chunks(input_folder, output_folder):
    """Read dataset chunks, clean specified columns, and save modified chunks."""
    os.makedirs(output_folder, exist_ok=True)

    for chunk_file in os.listdir(input_folder):
        if not chunk_file.endswith(".csv"):
            continue

        print(f"Processing chunk: {chunk_file}")
        chunk_path = os.path.join(input_folder, chunk_file)

        # Load the chunk
        df = pd.read_csv(chunk_path)

        # Clean columns and add new ones
        df['clean_title'] = df['title'].apply(clean_title)
        df['clean_authors'] = df['authors'].apply(clean_authors)
        df['clean_tags'] = df['tags'].apply(clean_tags)

        # Save the modified chunk
        output_path = os.path.join(output_folder, chunk_file)
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned chunk to: {output_path}")

# Example Usage
if __name__ == "__main__":
    input_folder = "DatasetChunks"  # Folder containing the original chunks
    output_folder = "cleaned_chunks"  # Folder to save the cleaned chunks

    process_chunks(input_folder, output_folder)
