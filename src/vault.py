import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib

class Vault:
    def __init__(self, master_key, storage_file):
        self.master_key = master_key
        self.storage_file = storage_file
        self.data = self._load_data()

    def _derive_key(self, master_key):
        salt = b'static_salt'  # In production, use a random salt stored securely
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_key.encode()))

    def _encrypt(self, data):
        f = Fernet(self._derive_key(self.master_key))
        return f.encrypt(data.encode()).decode()

    def _decrypt(self, token):
        f = Fernet(self._derive_key(self.master_key))
        return f.decrypt(token.encode()).decode()

    def _load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                encrypted_data = f.read()
                if encrypted_data:
                    decrypted = self._decrypt(encrypted_data)
                    return json.loads(decrypted)
        return {}

    def _save_data(self):
        encrypted_data = self._encrypt(json.dumps(self.data))
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        with open(self.storage_file, 'w') as f:
            f.write(encrypted_data)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self._save_data()

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save_data()
            return True
        return False

    def list_keys(self):
        return list(self.data.keys())

    def rotate_key(self, new_key):
        # Decrypt with old key, encrypt with new
        plain_data = json.dumps(self.data)
        self.master_key = new_key
        self._save_data()

    def status(self):
        return {
            "keys_count": len(self.data),
            "storage_file": self.storage_file
        }