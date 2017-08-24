#!/usr/local/bin/python3.6

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
import base64
import json
import hashlib

#
# decrypt data
#
def __decode(key,data):
	pass

#
# encrypt data
#
def __encode(key,data):
	pass

#
# return sha256 of data
#
def sha256(data):
	if type(data) == str:
		data = data.encode()
	h = SHA256.new()
	h.update(data)
	return h.hexdigest()

class Storage:
	#
	# set path to keyholder data file
	#
	def __init__(self,path):
		self.path = path

	#
	# loads and decrypth data
	#
	def load(self,password):
		cp = AESCipher(password)
		try:
			st = open(self.path).read()
		except Exception as e:
			if str(e) == "[Errno 2] No such file or directory: '%s'"%(str(self.path)):
				st = '{}'
				open(self.path,'w')
			else:
				raise RuntimeError(e)
		if len(st) > 0:
			return json.loads(cp.decrypt(st))
		else:
			return {}

	#
	# encrypt and dump data to file
	#
	def dump(self,password,data):
		cp = AESCipher(password)
		st = cp.encrypt(json.dumps(data)).decode('utf-8')
		open(self.path,'w').write(st)


#
# taken from stackoverflow
#
class AESCipher(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()
        #self.key = sha256(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

if __name__ == '__main__':
	pass