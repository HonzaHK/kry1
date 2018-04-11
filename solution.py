#!/usr/bin/env python3


def getKeystream():
	file_plaintext = open("in/bis.txt","rb")
	plaintext = file_plaintext.read(32)
	file_plaintext.close()

	file_ciphertext = open("in/bis.txt.enc","rb")
	ciphertext = file_ciphertext.read(32)
	file_ciphertext.close()

	keystream = [ plainbyte^cypherbyte for (plainbyte,cypherbyte) in zip(plaintext,ciphertext) ]

	return keystream


keystream = getKeystream()
# keystream256 = keystream[:32]

file_python = open("in/super_cipher.py.enc","rb")
pythontext = file_python.read(512)
file_python.close()

pythonplain = [ pythonbyte^keybyte for (pythonbyte,keybyte) in zip(pythontext,keystream) ]
# print("".join(chr(p) for p in pythonplain))

def printBits(x):
	print("{:08b}".format(x))

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


# a = int.from_bytes(''.join(str(x) for x in keystream).encode(),'little')
# a=int.from_bytes(plaintext,'little')
# b=int.from_bytes(ciphertext,'little')
c=int.from_bytes(keystream,'little')
keystr = int.from_bytes("KRY{0123456789}".encode(),'little')
for i in range(N//2):
	keystr = step(keystr)

print(keystr)
print("---------------------------")

subb = {
	1:{
		1:{0:3,1:2},
		2:{0:5,1:4},
		4:{0:0,1:1},
		6:{0:5,1:4}
	},
	0:{
		0:{0:0,1:1},
		3:{0:7,1:6},
		5:{0:3,1:2},
		7:{0:7,1:6}
	}
}


y_after_step = c

for i in range(N//2):
	msb_prev = 1 & y_after_step>>(255)
	possibles = list(subb[msb_prev].keys())
	paths = [[possibles[0]],[possibles[1]],[possibles[2]],[possibles[3]]]

	for j in range(1,256):
		msb_curr = 1 & y_after_step>>(255-j)

		newPossibles = []
		for possible in possibles:
			newPossibles.append(subb[msb_prev][possible][msb_curr])

		paths[0].append(newPossibles[0])
		paths[1].append(newPossibles[1])
		paths[2].append(newPossibles[2])
		paths[3].append(newPossibles[3])
		msb_prev = msb_curr
		possibles = newPossibles


	#pro kazodu path - prvni prvek beru cely, z kazdeho dalsiho pouze posledni bit
	#jakmile poskladam potencialni vstup, poslu jej do funkce step, abych zjistil, ktery z nich je spravny
	x_orig = None
	for path in paths:
		x_potencial = path[0] & 3#prvni prvek beru cely (3 bity)
		for elem in path[1:len(path)-1]:
			x_potencial = x_potencial<<1 | (elem & 1) #z kazdeho dalsiho vezmu lsb a prilepim ho zprava


		if(step(x_potencial)==y_after_step):
			x_orig = x_potencial


	# x_orig = (x_orig>>1) & ~(1>>N)
	# x_orig = (x_orig>>1) | (x_orig & (0<<N+1)) | (x_orig & (0<<N))
	# print("step ",i)
	y_after_step = x_orig

res = x_orig.to_bytes(29,byteorder='little').decode()
# print("{:b}".format(x_orig))
print(res)

