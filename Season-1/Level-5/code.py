# Welcome to Secure Code Game Season-1/Level-5!

# This is the last level of our first season, good luck!

import binascii
import secrets
import hashlib
import os
import bcrypt

class Random_generator:

    # generates a random token
    def generate_token(self, length=8, alphabet=(
    '0123456789'
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )):
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    # generates salt
    def generate_salt(self, rounds=12):
        salt = bcrypt.gensalt(rounds=rounds)
        return salt

class SHA256_hasher:

    # produces the password hash using bcrypt
    def password_hash(self, password, salt=None):
        if salt is None:
            salt = bcrypt.gensalt()
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = bcrypt.hashpw(password, salt)
        return password_hash.decode('ascii')

    # verifies that the hashed password reverses to the plain text version on verification
    def password_verification(self, password, password_hash):
        password = binascii.hexlify(hashlib.sha256(password.encode()).digest())
        password_hash = password_hash.encode('ascii')
        return bcrypt.checkpw(password, password_hash)

# Deprecated MD5_hasher for security reasons
class MD5_hasher:

    # same as above but using a different algorithm to hash which is MD5
    def password_hash(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def password_verification(self, password, password_hash):
        password = self.password_hash(password)
        return secrets.compare_digest(password, password_hash)

# a collection of sensitive secrets necessary for the software to operate
PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
PUBLIC_KEY = os.environ.get('PUBLIC_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_urlsafe(32))  # Default to a secure random key if not set
PASSWORD_HASHER = 'SHA256_hasher'

# Ensure SECRET_KEY is securely managed and not hardcoded.
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set!")


# Contribute new levels to the game in 3 simple steps!
# Read our Contribution Guideline at github.com/skills/secure-code-game/blob/main/CONTRIBUTING.md