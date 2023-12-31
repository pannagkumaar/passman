from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import hashlib
import base64
from database_manager import conn, store_master_hash, store_secret_key,fetch_master_hash, fetch_secret_key
FIXED_IV = b'\x00' * 16

# Creating a .env file if not present
def DoesHashExist():
    connect = conn()
    cursor = connect.cursor()

    try:
        # Check if the Master table has any rows
        cursor.execute("SELECT COUNT(*) FROM Master;")
        result = cursor.fetchone()

        if result and result[0] > 0:
            return True
    except Exception as e:
        print(e)

    return False


def generate_hash():
    if DoesHashExist() == False:
        print("To use PasswordManager first set your Master Password\n")
        masterPass = input("Set Master Password: ")
        print("\nPlease do not forget this password, as otherwise your passwords cannot be recovered")
        print("-" * 40)
        sha256_MasterPass = hashlib.sha256(masterPass.encode()).hexdigest()
        store_master_hash(sha256_MasterPass)


def check_hash():
    hash_from_db = fetch_master_hash()
    MasterPasswordInputNow = input("Enter the Master Password: ")
    MasterPasswordInputNowHashed = hashlib.sha256(MasterPasswordInputNow.encode()).hexdigest()
    return MasterPasswordInputNowHashed == hash_from_db, MasterPasswordInputNow

def DoesKeyExist():
    return fetch_secret_key() is not None

def generate_salt():
    return os.urandom(16) 


def generateKey():
    if not DoesKeyExist():
        master_password =fetch_master_hash()
        salt = generate_salt()

        # Using PBKDF2 to derive the key from the master password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=64,  # Length of the derived key
            salt=salt,
            iterations=100000,  # Adjust the number of iterations based on your security requirements
            backend=default_backend()
        )
        key = kdf.derive(master_password.encode())
        
        # Store the binary key directly, without converting to a string
        key_str = base64.urlsafe_b64encode(key).decode('utf-8')
        store_secret_key(key_str.encode('utf-8'))
        



def load_key():
    key = fetch_secret_key()
    if key:
        # Ensure the key is 32 bytes
        key = key[:32].encode('utf-8')
        return key
    else:
        return None

def encryptPass(passw):
    key = load_key()
    if key:
        cipher = Cipher(algorithms.AES(key), modes.GCM(FIXED_IV), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(passw.encode('utf-8')) + encryptor.finalize()
        # Return both the ciphertext and the tag
        return ciphertext, encryptor.tag
    else:
        return None

def decryptPass(ciphertext, tag):
    key = load_key()
    if key:
        cipher = Cipher(algorithms.AES(key), modes.GCM(FIXED_IV, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode('utf-8')
    else:
        return None