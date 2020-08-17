from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

#_DEFAULT_CHARSET_ = 'UTF-8'

# Classe simples para criptografar e descriptografar mensagens usando Fernet como módulo de criptografia simétrica
class MySymmetricCrypto:

	def __init__(self, sk = None):
		self.secretKey = sk

	def encrypt(self, msg, key = None):
		try:
			f = Fernet(self.secretKey if key is None else key)
			encrypted = f.encrypt(msg) # The msg must be type bytes, okay?
			return encrypted
		except InvalidToken as err:
			print('Token inválido ', err)
			raise
		except TypeError as err:
			print('Tipo inválido ', err)
			raise

	def decrypt(self, msg, key = None):
		try:
			f = Fernet(self.secretKey if key is None else key)
			decrypted = f.decrypt(msg)
			return decrypted
		except InvalidToken as err:
			print('Token inválido ', err)
			raise
		except TypeError as err:
			print('Tipo inválido ', err)
			raise


