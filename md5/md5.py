# The functions in this program will calculate the MD5 hash of a provided file.
#
#

#Import the math library to be able to do operations like floor and sin
import math
#Import the os library to be able to get file sizes and such
import os

#Define the bitwise left rotate function that operates on length 32 binary
def leftrotate(b, r):
	rotated = ((b >> r) | (b << (32 - r))) % 2 ** 32
	return rotated

#An array that will be used to inject more complexity to the hash
complexity = []
for i in range(64):
	complexity.insert(i, math.floor(abs(math.sin(i + 1) * (2 ** 32))))
		
#An array that will represent the per-round shift amounts
lshift = [
	7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
	5,  9, 14, 20, 5, 9, 14,  20, 5,  9, 14, 20, 5,  9, 14, 20,
	4, 11, 16, 23, 4, 11,16,  23, 4, 11, 16, 23, 4, 11, 16, 23,
	6, 10, 15, 21, 6, 10,15,  21, 6, 10, 15, 21, 6, 10, 15, 21,
]

#See below for explanation for this term
xorterm = 2 ** 32 - 1

#The four functions that will be used during the hashing
#Note on '~': Using this for the 'not' operation will treat the result as if it
# were being represented using two's complement. Thus, XOR'ing it with all ones
# of the proper length is better for this purpose.
def F(X, Y, Z):
	return ((X & Y) | ((X ^ xorterm) & Z))
def G(X, Y, Z):
	return ((X & Z) | (Y & (Z ^ xorterm)))
def H(X, Y, Z):
	return (X ^ Y ^ Z)
def I(X, Y, Z):
	return (Y ^ (X | (Z ^ xorterm)))

#A function that will take a given file, copy it bytewise into an array, and pad
# it properly
#Note: Python can only read from a file one byte at a time, so the padding
# figures out the suffix that will need to be appended, then appends it all
# as one rather than a piece at a time.
def loadfile(filename):
	filesizebytes = os.path.getsize(filename)
	bytesneeded = int((512 / 8) - filesizebytes % (512 / 8))
	if bytesneeded == 0:
		bytesneeded = 64 
	#The first byte will start with a 1, and since the file size must be
	# in bytes, we know that the remaining values of that byte will be 
	# zeros
	firstbyte = 0b10000000
	bytestofilesize = bytesneeded - 1 - 8
	zerobyte = 0
	#The last 64 bits (8 bytes) represent the file length in little-endian
	# binary, so here's the sequence of bytes that properly does that
	filesizenum = (filesizebytes * 8) % (2 ** 64)
	byteone = int(filesizenum / 256 ** 7) % 256
	bytetwo = int(filesizenum / 256 ** 6) % 256
	bytethree = int(filesizenum / 256 ** 5) % 256
	bytefour = int(filesizenum / 256 ** 4) % 256
	bytefive = int(filesizenum / 256 ** 3) % 256
	bytesix = int(filesizenum / 256 ** 2) % 256
	byteseven = int(filesizenum / 256) % 256
	byteeight = int(filesizenum) % 256 
	rawfile = open(filename)
	bytelist = rawfile.read()
	bytelist += chr(firstbyte)
	for i in range(bytestofilesize):
		#Debugging
		#print("Have printed " + str(i) + "blanks")
		#print("Length:" + str(len(bytelist)))
		bytelist += chr(zerobyte)
	bytelist += chr(byteone)
	bytelist += chr(bytetwo)
	bytelist += chr(bytethree)
	bytelist += chr(bytefour)
	bytelist += chr(bytefive)
	bytelist += chr(bytesix)
	bytelist += chr(byteseven)
	bytelist += chr(byteeight)
	finalbytelist = []
	for character in bytelist:
		finalbytelist.append(ord(character))

	#Debugging
	#print("Bytes needed: " + str(bytesneeded))
	#print("Bytes to file size: " + str(bytestofilesize))
	
	rawfile.close()
	
	return finalbytelist

#The function that actually does the hashing
def hash(bytelist):
	
	#Initialize the variables for the hashing
	A_0 = 0x67452301
	B_0 = 0xEFCDAB89
	C_0 = 0x98BADCFE
	D_0 = 0x10325476


	#Iterate through all 64 byte chunks
	for i in range(1, 1 + int(len(bytelist) / 64)):
		
		#For debugging
		print("A_0: " + hex(A_0))
	
		#Initialize the ABCD values
		A = A_0
		B = B_0
		C = C_0
		D = D_0

		#Go through each chunk in increments of 32 bits (4 bytes)
		for j in range(16):
			value = bytelist[4 * j * i] * 256 ** 3 + \
			        bytelist[4 * j * i + 1] * 256 ** 2 + \
			        bytelist[4 * j * i + 2] * 256 + \
					bytelist[4 * j * i + 3]
			print("Value for " + str(j) + ":" + str(value))
			print("A: " + hex(A) + "\n" + "B: " + hex(B) + "\n" + "C: " + hex(C) + "\n" + "D: " + hex(D))
			holdb = B
			B = (leftrotate((F(B,C,D) + A + value + \
				complexity[j]) % 2 ** 32, \
				lshift[j]) + B) % 2 ** 32
			holdd = D
			D = C
			C = holdb
			print("B: " + hex(B))
			A = holdd
		#Go through each chunk again, but with a twist
		for j in range(16, 32):
			value = bytelist[((5 * j * i + 1) % 16) * 4] * 256 ** 3 + \
			        bytelist[((5 * j * i + 1) % 16) * 4 + 1] * \
								  256 ** 2 + \
			        bytelist[((5 * j * i + 1) % 16) * 4 + 2] * 256 + \
					bytelist[((5 * j * i + 1) % 16) * 4 + 3]
			print("Value for " + str(j) + ":" + str(value))
			holdb = B
			B = (leftrotate((G(B,C,D) + A + value + \
						complexity[j]) % 2 ** 32, \
						lshift[j]) + B) % 2 ** 32
			holdd = D
			D = C
			C = holdb
			A = holdd
		#Again, but in a different manner
		for j in range(32, 48):
			value = bytelist[((3 * j * i + 5) % 16) * 4] * 256 ** 3 + \
			        bytelist[((3 * j * i + 5) % 16) * 4 + 1] * \
								  256 ** 2 + \
			        bytelist[((3 * j * i + 5) % 16) * 4 + 2] * 256 + \
					bytelist[((3 * j * i + 5) % 16) * 4 + 3]
			print("Value for " + str(j) + ":" + str(value))
			holdb = B
			B = (leftrotate((H(B,C,D) + A + value + \
						complexity[j]) % 2 ** 32, \
						lshift[j]) + B) % 2 ** 32
			holdd = D
			D = C
			C = holdb
			A = holdd
		#One last time!
		for j in range(48, 64):
			value = bytelist[((7 * j * i) % 16) * 4] * 256 ** 3 + \
			        bytelist[((7 * j * i) % 16) * 4 + 1] * \
								  256 ** 2 + \
			        bytelist[((7 * j * i) % 16) * 4 + 2] * 256 + \
					bytelist[((7 * j * i) % 16) * 4 + 3]
			print("Value for " + str(j) + ":" + str(value))
			print("Value of B: " + str(B))
			holdb = B
			B = (leftrotate((I(B,C,D) + A + value + \
						complexity[j]) % 2 ** 32, \
						lshift[j]) + B) % 2 ** 32
			holdd = D
			D = C
			C = holdb
			A = holdd
		
		#For debugging
		print("A: " + hex(A))

		#Append our hash to the total
		A_0 = (A_0 + A) % 2 ** 32
		B_0 = (B_0 + B) % 2 ** 32
		C_0 = (C_0 + C) % 2 ** 32
		D_0 = (D_0 + D) % 2 ** 32

		print("A_0: " + hex(A_0))
	return ((A_0 << 96) + (B_0 << 64) + (C_0 << 32) + D_0)

def main():
	filename = input("Which file would you like to hash? ")
	print("File size in bits: " + str(os.path.getsize(filename) * 8))
	bytelist = loadfile(filename)
	hashtext = hash(bytelist)
	print(hex(hashtext))

#main()

#For Debugging
def stepone(A,B,C,D, Value, Complexity, LShift):
	holdb = B
	holdd = D
	newB = (leftrotate((A + F(B, C, D) + Complexity + Value) % 2 ** 32, LShift) + B) % 2 ** 32
	newD = C
	newC = holdb
	newA = holdd
	print("newA: " + hex(newA))
	print("newB: " + hex(newB))
	print("newC: " + hex(newC))
	print("newD: " + hex(newD))
