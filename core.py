## enrypt and decrypt
from cryptography.fernet import Fernet
import json
import os

# Generate a key (or load if exists)
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

# Encrypt & Decrypt functions
def encrypt_password(password, key):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password.encode()).decode()
######
PASSWORDS_FILE = "passwords.json"

def save_passwords(passwords):
    with open(PASSWORDS_FILE, "w") as f:
        json.dump(passwords, f)

def load_passwords():
    if not os.path.exists(PASSWORDS_FILE):
        return {}
    with open(PASSWORDS_FILE, "r") as f:
        return json.load(f)

#####
MASTER_PASSWORD_FILE = "master.key"


def set_master_password(password):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode()).decode()
    with open(MASTER_PASSWORD_FILE, "w") as f:
        json.dump({"key": key.decode(), "password": encrypted_password}, f)


def check_master_password(input_password):
    if not os.path.exists(MASTER_PASSWORD_FILE):
        return True  # First-time setup

    with open(MASTER_PASSWORD_FILE, "r") as f:
        data = json.load(f)
        key = data["key"].encode()
        stored_password = data["password"]

    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(stored_password.encode()).decode()
    return input_password == decrypted_password
###########

