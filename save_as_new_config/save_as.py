import json
import os

def load_config(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as config_file:
            return json.load(config_file)
    else:
        print(f"File {file_path} does not exist.")
        return None

config_path = "lmao.json" # change this to your config path
current_config = load_config(config_path)

external_config_path = None 

def save_as_new_config(current_config, new_file_name):
    global external_config_path

    if not new_file_name.endswith(".json"): # .json is default if you dont want. Delete this if
        new_file_name += ".json"

    try:
        with open(new_file_name, "w") as config_file:
            json.dump(current_config, config_file, indent=4)

        external_config_path = new_file_name
        print(f"Configuration saved to {new_file_name}. External config path updated.")

    except IOError as e:
        print(f"Failed to save config: {e}")

# Example usage
# new_file_name = input("Enter the new config file name: ").strip()
#save_as_new_config(current_config, new_file_name)
