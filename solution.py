#!/usr/bin/env python3

#prints first 512B of super_cipher.py.enc decoded
def printPythonFileContent():
	file_plaintext = open("in/bis.txt","rb")
	plaintext = file_plaintext.read(512)
	file_plaintext.close()

	file_ciphertext = open("in/bis.txt.enc","rb")
	ciphertext = file_ciphertext.read(512)
	file_ciphertext.close()

	keystream = [ plainbyte^cypherbyte for (plainbyte,cypherbyte) in zip(plaintext,ciphertext) ]

	file_python = open("in/super_cipher.py.enc","rb")
	pythontext = file_python.read(512)
	file_python.close()

	pythonplain = [ pythonbyte^keybyte for (pythonbyte,keybyte) in zip(pythontext,keystream) ]
	print("".join(chr(p) for p in pythonplain))

#gets 32B long keystream
def getKeystream():
	file_plaintext = open("in/bis.txt","rb")
	plaintext = file_plaintext.read(32)
	file_plaintext.close()

	file_ciphertext = open("in/bis.txt.enc","rb")
	ciphertext = file_ciphertext.read(32)
	file_ciphertext.close()

	keystream = [ plainbyte^cypherbyte for (plainbyte,cypherbyte) in zip(plaintext,ciphertext) ]

	return keystream


# ===== CONTENTS OF DECODED FILE super_cipher.py.enc ============================
SUB = [0, 1, 1, 0, 1, 0, 1, 0]
N_B = 32
N = 8 * N_B

# Next keystream
def step(x):
	x = (x & 1) << N+1 | x << 1 | x >> N-1
	y = 0
	for i in range(N):
		y |= SUB[(x >> i) & 7] << i
	return y


def enc(key):
	keystr = int.from_bytes(key.encode(),'little')
	for i in range(N//2):
		keystr = step(keystr)

	return keystr
# ================================================================================

# printPythonFileContent()


sub_inv = {
	1: {
		1: { 0:3, 1:2},
		2: { 0:5, 1:4},
		4: { 0:0, 1:1},
		6: { 0:5, 1:4}
	},
	0: {
		0: { 0:0, 1:1},
		3: { 0:7, 1:6},
		5: { 0:3, 1:2},
		7: { 0:7, 1:6}
	}
}

#for testing purposes
# y_after_step = enc("KRY_0123456789")

#get my keystream
keystream = getKeystream()

#keystream is y after all iterations in "enc" function (integer)
y_after_step = int.from_bytes(keystream,'little')

#do as many iterations as "enc" does
for i in range(N//2):
	#perform variables initialization
	msb_prev = y_after_step>>(255) & 1 #get MSb
	possibles = list(sub_inv[msb_prev].keys()) #get possible indexes of SUB array for the MSb
	paths = [ #we get 4 possible paths; accumulate them all
		[possibles[0]],
		[possibles[1]],
		[possibles[2]],
		[possibles[3]]
	]


	for j in range(1,256):
		msb_curr = y_after_step>>(255-j) & 1 #get MSb

		newPossibles = []
		for possible in possibles:
			#get possible indexes, which take us from msb_prev to msb_curr
			newPossibles.append(sub_inv[msb_prev][possible][msb_curr])

		#we are storing 4 possible paths; accumulate them all
		paths[0].append(newPossibles[0])
		paths[1].append(newPossibles[1])
		paths[2].append(newPossibles[2])
		paths[3].append(newPossibles[3])

		#re-init for next step
		msb_prev = msb_curr
		possibles = newPossibles


	#foreach path - store all 3 bits from the first elem, only LSb from others
	x_orig = None
	for path in paths:
		x_potencial = path[0] #first elem - store all 3 bits
		for elem in path[1:]:
			x_potencial = x_potencial<<1 | (elem & 1) #from others - only LSb

		#now we have x' = {LSb(x).x.MSb(x)}, extract x
		#that means shift x' right and clear MSb(x')
		x_potencial = (x_potencial>>1) & ~(1<<N)

		#choose right x by sending it into step() function and checking its result
		if(step(x_potencial)==y_after_step):
			x_orig = x_potencial

	#re-init y for next cycle
	y_after_step = x_orig

#we know key has length 29 -> convert int to bytes and then to string
key = x_orig.to_bytes(29,byteorder='little').decode()

#print out the key
print(key)