import string
import secrets

def generate_password(length=12, include_lowercase=True, include_uppercase=True, include_digits=True, include_special=True):
   
    # Define character sets based on user preferences
    character_sets = []
    if include_lowercase:
        character_sets.append(string.ascii_lowercase)
    if include_uppercase:
        character_sets.append(string.ascii_uppercase)
    if include_digits:
        character_sets.append(string.digits)
    if include_special:
        character_sets.append(string.punctuation)

    # Ensure at least one character set is selected
    if not character_sets:
        raise ValueError("At least one character set must be selected.")

    # Calculate the minimum password length based on selected character sets
    

    # Ensure the length of the password meets the minimum requirement
    length = max(length, 12)

    # Generate a secure random password
    password = ''.join(secrets.choice(secrets.choice(character_sets)) for _ in range(length))

    return password

if __name__ == "__main__":
    # Example usage:
    password = generate_password(length=16, include_lowercase=True, include_uppercase=True, include_digits=True, include_special=True)
    print("Generated Password:", password)
