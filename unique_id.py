import random
import os

# File to store IDs
FILE_NAME = "unique_ids.txt"

def generate_random_id():
    """Generate a random 4-digit ID."""
    return f"{random.randint(1000, 9999)}"

def load_existing_ids():
    """Load existing IDs from the file."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return set(file.read().splitlines())
    return set()

def save_id(new_id):
    """Save a new ID to the file."""
    with open(FILE_NAME, "a") as file:
        file.write(new_id + "\n")

def generate_unique_id():
    """Generate a unique 4-digit ID."""
    existing_ids = load_existing_ids()
    while True:
        new_id = generate_random_id()
        if new_id not in existing_ids:
            save_id(new_id)
            return new_id

if __name__ == "__main__":
    unique_id = generate_unique_id()
    print(f"Generated unique ID: {unique_id}")
