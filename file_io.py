import os
import json

# Loads and returns a dictionary, created by a JSON file
# filepath is the path to the JSON file
def load_json_file(filepath):
    with open(filepath, "r") as f:
        mod_set = json.loads(f.read())
    print("File read successfully")
    return mod_set

# Creates a JSON file from the dictionary provided at the given filepath
# Can also be used to update a JSON file by overwriting it
def write_json_file(filepath, mod_set):
    with open(filepath, "w") as f:
        f.write(json.dumps(mod_set))
    print("File created successfully")

# Lists all the JSON files in the saves directory
def list_saves():
    print()
    print("List of all module sets")
    print("----------")
    for file in os.listdir("saves/"):
        if file.endswith(".json"):
            print(file[:-5])

# Generates the filepath to the json file with this name
def get_filepath(name):
    return os.path.join("saves/", name + ".json")
