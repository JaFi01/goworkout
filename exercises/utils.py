import base64

#this utils will be used later
def set_password(self, raw_password):
    if raw_password is None:
        self.set_unusable_password()
    else:
        salt = os.urandom(32)
        hashed_password = self._hash_password(raw_password, salt)
        self.password = base64.b64encode(salt + hashed_password).decode('utf-8')
    self.save(update_fields=["password"])
    
def check_password(self, raw_password):
    if not self.has_usable_password() or raw_password is None:
        return False
    decoded = base64.b64decode(self.password.encode('utf-8'))
    salt = decoded[:32]
    stored_hash = decoded[32:]
    computed_hash = self._hash_password(raw_password, salt)
    return stored_hash == computed_hash

@staticmethod
def _hash_password(password, salt):
    import hashlib
    return salt + hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000  # Iteration count
    )
    