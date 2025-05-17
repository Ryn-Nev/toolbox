# Author: Ryan Neville Hansen | Stellenbosch University
# Email: 25088521@sun.ac.za
# Created with assistance from Claude AI

# ----- Imports -----------------------------------------------------------------------------------
import zipfile
from pathlib import Path
import os
import sys

# ----- Utility functions -------------------------------------------------------------------------
def extract_zip(zip_path):
    """Extract a single ZIP file to a folder with the same name."""
    try:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            extract_path = Path(zip_path).parent / Path(zip_path).stem
            archive.extractall(path=extract_path)
            print(f"Extracted contents from '{os.path.basename(zip_path)}' to '{extract_path}' directory.")
    except Exception as e:
        print(f"Error extracting {zip_path}: {str(e)}")
        sys.exit(1)

# ----- Main method -------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If a file was provided as argument, extract it
        p = Path(sys.argv[1])

        # Get the user's preference for deleting the original zip files
        print("Do you want to delete the original zip files after extraction? (y/n)")
        delete_original = input("Enter 'y' to delete the original zip files, 'n' to keep them: ").strip().lower()
        if delete_original not in ['y', 'n']:
            print("Invalid input. Please enter 'y' or 'n'.")
            sys.exit(1)

        remove = delete_original == 'y'
        if remove:
            print("Original zip files will be deleted after extraction.")

        # Extract all zip files in the directory and subdirectories
        for f in p.rglob('*.zip'):
            extract_zip(f)
            if remove:
                os.remove(f)
                print(f"Deleted original zip file '{f.name}'.")

    else:
        # Get the current working directory
        current_dir = os.getcwd()

        # Get the file path from the user
        print("Please enter the path to the directory containing the zip files:")
        print("If the directory is in the same location as this script, you can enter 0.")
        filepath = input("Enter the path to the directory containing the zip files: ") 
        if filepath == '0':
            filepath = current_dir

        if not os.path.exists(filepath):
            print(f"The directory '{filepath}' does not exist.")
            sys.exit(1)

        p = Path(filepath)

        # Get the user's preference for deleting the original zip files
        print("Do you want to delete the original zip files after extraction? (y/n)")
        delete_original = input("Enter 'y' to delete the original zip files, 'n' to keep them: ").strip().lower()
        if delete_original not in ['y', 'n']:
            print("Invalid input. Please enter 'y' or 'n'.")
            sys.exit(1)

        remove = delete_original == 'y'
        if remove:
            print("Original zip files will be deleted after extraction.")

        # Extract all zip files in the directory and subdirectories
        for f in p.rglob('*.zip'):
            extract_zip(f)
            if remove:
                os.remove(f)
                print(f"Deleted original zip file '{f.name}'.")