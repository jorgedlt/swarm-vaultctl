#!/usr/bin/env python3
import secrets

# Generate a random 32-byte key for Fernet
key = secrets.token_bytes(32)
print(key.hex())