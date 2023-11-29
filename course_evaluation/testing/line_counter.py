# line_counter.py: Reads a .json file created by CIS_json_test.py
import os

def count_filled_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return sum(1 for line in lines if line.strip())

def count_filled_lines_in_folder(folder_path):
    total_filled_lines = 0

    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Iterate through each file and count filled lines
    for file in files:
        file_path = os.path.join(folder_path, file)
        filled_lines = count_filled_lines(file_path)
        total_filled_lines += filled_lines
        print(f"File: {file}, Filled Lines: {filled_lines}")

    print(f"Total Filled Lines in all files: {total_filled_lines}")

# Replace 'your_folder_path' with the path to the folder containing your .txt files
folder_path = 'complete_dictionaries'
count_filled_lines_in_folder(folder_path)
