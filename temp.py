from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from database_manager import conn

# Use a fixed IV (for illustration purposes only; not recommended for real-world use)
FIXED_IV = b'\x00' * 16

def fetch_secret_key():
    connect = conn()
    cursor = connect.cursor()
    try:
        cursor.execute("SELECT `Key` FROM SecretKey;")
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(e)
        return None
    finally:
        connect.close()

def load_key():
    key = fetch_secret_key()
    if key:
        # Ensure the key is 32 bytes
        key = key[:32].encode('utf-8')
        return key
    else:
        return None

def encrypt_pass(passw):
    key = load_key()
    if key:
        cipher = Cipher(algorithms.AES(key), modes.GCM(FIXED_IV), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(passw.encode('utf-8')) + encryptor.finalize()
        # Return both the ciphertext and the tag
        return ciphertext, encryptor.tag
    else:
        return None

def decrypt_pass(ciphertext, tag):
    key = load_key()
    if key:
        cipher = Cipher(algorithms.AES(key), modes.GCM(FIXED_IV, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext.decode('utf-8')
    else:
        return None

# Test
passphrase = "hello"
ciphertext, tag = encrypt_pass(passphrase)
if ciphertext:
    decrypted_passphrase = decrypt_pass(ciphertext, tag)
    print("Decrypted Password:", decrypted_passphrase)
else:
    print("Encryption failed.")
