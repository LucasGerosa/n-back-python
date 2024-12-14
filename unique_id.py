import random
import os

# File to store unique 4-digit numbers
FILE_NAME = "unique_numbers.txt"

def generate_random_id():
    """Generate a random ID with a random lowercase letter and a unique 4-digit number."""
    random_letter = chr(random.randint(97, 122))  # Random lowercase letter (ASCII a-z)
    random_number = f"{random.randint(1000, 9999)}"  # Random 4-digit number
    return random_letter + random_number

def generate_unique_number():
    """Generate a unique 4-digit number."""
    existing_numbers = load_existing_numbers()
    while True:
        new_number = f"{random.randint(1000, 9999)}"
        if new_number not in existing_numbers:
            save_number(new_number)
            return new_number

def load_existing_numbers():
    """Load existing 4-digit numbers from the file."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return set(file.read().splitlines())
    return set()

def save_number(new_number):
    """Save a new unique 4-digit number to the file."""
    with open(FILE_NAME, "a") as file:
        file.write(new_number + "\n")

def generate_unique_id():
    """Generate a unique ID with a random letter and a unique 4-digit number."""
    random_letter = chr(random.randint(97, 122))  # Random lowercase letter
    unique_number = generate_unique_number()      # Unique 4-digit number
    return random_letter + unique_number

if __name__ == "__main__":
    for _ in range(100):
        unique_id = generate_unique_id()
        print(f"Generated unique ID: {unique_id}")
