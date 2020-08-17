import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


# Gerar uma nova chave de criptografia
def newKey(palavra_chave):
	password = palavra_chave.encode() # convert to type bytes
	salt = os.urandom(32) # b'secret_key'
	kdf = PBKDF2HMAC(
	    algorithm=hashes.SHA256(),
	    length=32,
	    salt=salt,
	    iterations=16384,
	    backend=default_backend()
	)
	key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
	return key


# Try it:
# python3 -c 'import util.GenerateKey; print(util.GenerateKey.newKey("yes! its my password"))'
