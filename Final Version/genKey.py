import math, random

def genKey(n):
	alphabet = list("abcdefghijklmnopqrstuvwxyz")
	out = ""
	for i in range(n):
		out += alphabet[math.floor(random.randint(0, len(alphabet)-1))]
	return out
