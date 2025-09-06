import json
import hashlib

file_path = "storage.json"

def get_file_data():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    return data


# very unnecessary considering it's a client-sided project lol but for the flex
def hash_password(password: str) -> str:
    """Return SHA-256 hash of the password as a hex string."""
    return hashlib.sha256(password.encode()).hexdigest()



# Function for Sign-Up
def sign_up(username, password):

    # Limit username and password characters
    if len(username) > 20 or len(username) < 4:
        return "Invalid username length, please ensure it is 4-20 characters long."

    if len(password) > 20 or len(password) < 4:
        return "Invalid password length, please ensure it is 4-20 characters long."

    # Make sure no special characters in username
    if not username.isalnum():
        return "Invalid characters in username, no special characters or emojis (eg [ , . ? :)"

    # Read the file and put it in 'data'
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    # Check if username already exists
    for existing_username in data.keys():
        if existing_username.lower() == username.lower():
            return "Username already exists"

    data[username] = {"password": hash_password(password), "score": 0}


    # If everything was successful, put all the new data in the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


    return "Success!"



# Function for Log-in
def log_in(username, password):

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

            for existing_username in data.keys():
                if existing_username.lower() == username.lower(): # Check if username exists
                    if data[existing_username]["password"] == hash_password(password):
                        return "Success!"
                    else:
                        return "Invalid password"
            return "Username doesn't exist." # if username isn't in the json file just return that it doesn't exist

    except FileNotFoundError: # In case the file doesn't exist
        return "File not found."
    except PermissionError: # In case the file is locked
        return "No permission to open file (run in administrator mode)"
    except json.JSONDecodeError: # In case the file is empty or corrupted.
        return "File is empty or corrupted."
    except Exception:
        return "Unknown error"

def update_data(data: dict):
    try:
        with open(file=file_path, mode='w') as json_file:
            json.dump(data, json_file, indent=4)  # indent=4 for pretty printing
            print("JSON file written successfully!")
    except TypeError:
        print("You wrote an invalid type to the JSON file.")
