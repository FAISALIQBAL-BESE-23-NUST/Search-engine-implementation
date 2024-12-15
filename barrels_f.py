import pandas as pd
import os

def create_forward_index_barrels(forward_index_csv, output_dir, barrel_size=1000):
    """
    Create barrels for the forward index.
    
    :param forward_index_csv: Path to the forward index CSV file.
    :param output_dir: Directory to save the barrel files.
    :param barrel_size: Number of documents per barrel.
    """
    try:
        # Load the forward index
        print("Loading forward index CSV...")
        forward_index = pd.read_csv(forward_index_csv)

        # Ensure the CSV contains necessary columns
        if not {'Doc_ID', 'Terms'}.issubset(forward_index.columns):
            raise ValueError("CSV file must contain columns {'Doc_ID', 'Terms'}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Partition the forward index into barrels
        for i in range(0, len(forward_index), barrel_size):
            barrel = forward_index.iloc[i:i+barrel_size]
            barrel_file = os.path.join(output_dir, f"forward_barrel_{i // barrel_size}.csv")
            barrel.to_csv(barrel_file, index=False)
            print(f"Saved forward index barrel to '{barrel_file}'")

    except Exception as e:
        print(f"Error while creating forward index barrels: {e}")

def main():
    # File paths
    forward_index_csv = "forward_index.csv"  # Path to the forward index file
    output_dir = "forward_barrels"          # Directory to save barrels

    # Barrel size (number of documents per barrel)
    barrel_size = 1000

    # Create forward index barrels
    create_forward_index_barrels(forward_index_csv, output_dir, barrel_size)

if __name__ == "__main__":
    main()
