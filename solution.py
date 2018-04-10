#!/usr/bin/env python3


def getKeystream():
	file_plaintext = open("in/bis.txt","rb")
	plaintext = file_plaintext.read(512)
	file_plaintext.close()

	file_ciphertext = open("in/bis.txt.enc","rb")
	ciphertext = file_ciphertext.read(512)
	file_ciphertext.close()

	keystream = bytes([ plainbyte^cypherbyte for (plainbyte,cypherbyte) in zip(plaintext,ciphertext) ])

	return keystream


keystream = getKeystream()

file_python = open("in/super_cipher.py.enc","rb")
pythontext = file_python.read(512)
file_python.close()

pythonplain = [ pythonbyte^keybyte for (pythonbyte,keybyte) in zip(pythontext,keystream) ]
print(''.join(chr(a) for a in pythonplain))
