from encryption import generateKey, encryptPass, decryptPass
import base64
from database_manager import (
    store_password,
    find_password,
    find_using_email,
)
import subprocess
from colorama import Fore, Style


def menu():
    # Creating required files
    generateKey()

    

    # Aesthetics
    print("-" * 40)
    print("-" * 40)
    print("1. Create New Password")
    print("2. Find a Password for a Service")
    print("3. Find All Passwords for an Email")
    print("Q. Quit")
    print("_" * 40)
    return input(": ")


def store():
    email = input("Email: ")
    username = input("Username: ")
    password = input("Password: ")
    url = input("URL: ")
    service = input("Service: ")
    if len(username) < 1:
        username = ""
    encryptedPass,tag = encryptPass(password)
    hex_string1 = ''.join(format(byte, '02x') for byte in encryptedPass)
    hex_string2 = ''.join(format(byte, '02x') for byte in tag)
    

    store_password(hex_string1, email, username, url, service,hex_string2)
    print("_" * 40)
    print(
        "Password Encrypted and Stored",
    )
    print("_" * 40)


def find():
    service = input("Service: ")
    encrypted_pass_hex, tag_hex = find_password(service)

    if encrypted_pass_hex == "" or tag_hex == "":
        print("No Password Found")
    else:
        # Convert hex strings to byte strings
        encrypted_pass = bytes.fromhex(encrypted_pass_hex)
        tag = bytes.fromhex(tag_hex)

        # Decrypt the password
        passw = decryptPass(encrypted_pass, tag)

        # Assuming decryptPass returns the original password as a string
        subprocess.run("clip", universal_newlines=True, input=passw)
        print("_" * 40)
        print("Password has been copied to clipboard")
        print("_" * 40)

def find_email():
    data = ["Encrypted Password", "Email", "Username", "Url", "Service","Tag"]
    email = input("Email: ")
    results = find_using_email(email)
    print(results)
    print("-" * 40)
    if results:
        for row in results:
            for i in range(0, len(row)):
                print("{}: {}".format(data[i], row[i]))
            print("-" * 40)
    else:
        print("No Passwords Found")


def aesthetics():
   
    print(Fore.CYAN + "#" * 40)
   
    print("#" * 40)
    print("To reset the password press 9 ")
    print()