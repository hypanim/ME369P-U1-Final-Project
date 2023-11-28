# json_reader.py: Reads a .json file created by CIS_json_test.py
import json
def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data
if __name__ == "__main__":
    file_path = 'instructor_data.json'
    instructor_data = read_json(file_path)
    print(json.dumps(instructor_data, indent=2))