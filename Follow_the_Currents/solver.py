import os
import zlib
from Crypto.Util.number import *
def keystream():
	#key = b'g\x15'
	index = 0
	print(key)
	while 1:
		index+=1
		if index >= len(key):
			key += zlib.crc32(key).to_bytes(4,'big')
			print(key)
		yield key[index]

def kstream(key):
	index = 0
	while True:
		index+=1
		if index >= len(key):
			key += zlib.crc32(key).to_bytes(4,'big')
		yield key[index]


f = open("enc","rb")
enc = f.read()
for i in range(256):
	print(i)
	for j in range(256):
		#keyをbrute forceしている
		k = kstream(long_to_bytes(i*256+j))
		flag = ""
		for x in enc:
			flag += chr(x^next(k))
		if "actf" in flag: print(flag)
