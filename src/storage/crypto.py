from cryptography.fernet import Fernet
from storage import storage

def write_key():
    key = Fernet.generate_key()
    with open(storage.DATA_DIR + "key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    return open(storage.DATA_DIR + "key.key", "rb").read()