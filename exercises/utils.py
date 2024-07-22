import hashlib
import os
import base64

def generate_salt():
    return os.urandom(32)

def hash_password(password, salt=None):
    if salt is None:
        salt = generate_salt()
    
    salted_password = salt + password.encode('utf-8')
    hashed = hashlib.sha256(salted_password).digest()
    return base64.b64encode(salt + hashed).decode('utf-8')

def check_password(stored_password, provided_password):
    decoded = base64.b64decode(stored_password.encode('utf-8'))
    salt = decoded[:32]
    stored_hash = decoded[32:]
    
    salted_password = salt + provided_password.encode('utf-8')
    computed_hash = hashlib.sha256(salted_password).digest()
    
    return computed_hash == stored_hash