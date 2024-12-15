import pandas as pd
import os
from collections import defaultdict

def create_barrels(inverted_index_csv, output_dir, barrel_size=1000):
    """
    Create barrels (partitioned inverted index) from an inverted index CSV.
    
    :param inverted_index_csv: Path to the inverted index CSV file.
    :param output_dir: Directory to save the barrel files.
    :param barrel_size: Number of terms per barrel.
    """
    try:
        # Load the inverted index
        print("Loading inverted index CSV...")
        inverted_index = pd.read_csv(inverted_index_csv)

        # Ensure columns are correctly named
        if not {'Term', 'Doc_Indices'}.issubset(inverted_index.columns):
            raise ValueError("CSV file must contain columns {'Term', 'Doc_Indices'}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Initialize barrels
        barrel_id = 0
        current_barrel = defaultdict(list)

        # Iterate through the inverted index
        for i, row in inverted_index.iterrows():
            term = row['Term']
            doc_indices = row['Doc_Indices']

            # Ensure doc_indices are parsed correctly
            if isinstance(doc_indices, str):
                doc_indices_list = list(map(int, doc_indices.split(',')))
            else:
                doc_indices_list = []

            # Add term and its indices to the current barrel
            current_barrel[term] = doc_indices_list

            # If the barrel reaches the size limit, save it and start a new one
            if len(current_barrel) >= barrel_size:
                save_barrel(current_barrel, output_dir, barrel_id)
                barrel_id += 1
                current_barrel.clear()

        # Save any remaining terms in the last barrel
        if current_barrel:
            save_barrel(current_barrel, output_dir, barrel_id)

        print(f"Barrels created successfully in '{output_dir}'")

    except Exception as e:
        print(f"Error while creating barrels: {e}")

def save_barrel(barrel, output_dir, barrel_id):
    """
    Save a single barrel to a CSV file.
    
    :param barrel: The barrel (dictionary of terms and their document lists).
    :param output_dir: Directory to save the barrel file.
    :param barrel_id: ID of the barrel for naming.
    """
    barrel_df = pd.DataFrame({
        "Term": list(barrel.keys()),
        "Doc_Indices": [",".join(map(str, indices)) for indices in barrel.values()]
    })
    barrel_file = os.path.join(output_dir, f"barrel_{barrel_id}.csv")
    barrel_df.to_csv(barrel_file, index=False)
    print(f"Saved barrel {barrel_id} to '{barrel_file}'")

def main():
    # File paths
    inverted_index_csv = "backward_index.csv"  # Replace with your inverted index file
    output_dir = "barrels"  # Directory to save the barrels

    # Barrel size (number of terms per barrel)
    barrel_size = 1000

    # Create barrels
    create_barrels(inverted_index_csv, output_dir, barrel_size)

if __name__ == "__main__":
    main()
