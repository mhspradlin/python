# The functions in this program will calculate the MD5 hash of a provided file.
#
#

#Import the math library to be able to do operations like floor and sin
import math
#Import the os library to be able to get file sizes and such
import os

#Define the bitwise left rotate function that operates on length 32 binary
def leftrotate(b, r):
	return ((b << r) | (b >> (32 - r)))

#Define the initial constants for the hash calculation
A_0 = 0x67452301
B_0 = 0xEFCDAB89
C_0 = 0x98BADCFE
D_0 = 0x10325476

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

#The four functions that will be used during the hashing
def F(X, Y, Z):
	return ((X & Y) | ((~X) & Z))
def G(X, Y, Z):
	return ((X & Z) | (Y & (~Z)))
def H(X, Y, Z):
	return (X ^ Y ^ Z)
def I(X, Y, Z):
	return (Y ^ (X | (~ Z)))

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

	return finalbytelist

#The function that actually does the hashing
def hash(bytelist):
	print("This is a hash!")

def main():
	filename = input("Which file would you like to hash? ")
	print("File size in bits: " + str(os.path.getsize(filename) * 8))
	bytelist = loadfile(filename)
	hash = hash(bytelist)
	print(hash)

main()
