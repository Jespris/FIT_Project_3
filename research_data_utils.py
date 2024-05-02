import json
import os

DATA_FOLDER = 'research_data'


# USE THIS TO SAVE THE DATA TO THE RESEARCH_DATA FOLDER
def save_json_data(data, filepath: str):
    # filepath name should be in style: question_#_data.json
    joined_path = os.path.join(DATA_FOLDER, filepath)
    # Format data to JSON string that looks good
    json_string = json.dumps(data, indent=4)
    # Write JSON string to file
    with open(joined_path, "w") as json_file:
        json_file.write(json_string)
    print(f"JSON file saved to: {joined_path}")


# USE THIS TO LOAD DATA FROM THE RESEARCH_DATA FOLDER
def load_json_data(filepath: str):
    # filepath is json file name in the research_data folder
    print(f"Loading {filepath}...")
    try:
        with open(f"{DATA_FOLDER}/{filepath}", 'r', encoding='utf-8') as file:
            # json.load converts json into python dictionary
            json_data = json.load(file)
        print("Load successful!")
        return json_data
    except Exception as e:
        print(f"File path probably doesn't exist, check spelling... \nError code: {e}")
        return None

