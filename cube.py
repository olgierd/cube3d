#!/usr/bin/python
import time

# de github.com/olgierd 2018, CC-BY-NC-SA

# prints block/cube state, bottom layer on the left, view from top
def print3dblock(block):
	print(block[:3]+' '+block[9:12]+' '+block[18:21])
	print(block[3:6]+' '+block[12:15]+' '+block[21:24])
	print(block[6:9]+' '+block[15:18]+' '+block[24:27])
	print()

# block format - first 9 chars = bottom layer and so on
blocks = [
	'111010000100000000000000000',
	'220022000020000000000000000',
	'030333000030000000000000000',
	'400440000400000000000000000',
	'555000000050000000000000000',
	'666600000000000000000000000'
]

# moves a block in 3d spaceusing 27-char format block description
def moveblock(block, dir, distance):
	if distance == 0:
		return block
	if len(block) != 27:
		return "ERR"

	if dir == "up" and block[-9:] == '0'*9:
		bl = '0'*9+block[0:18]
		return moveblock(bl, dir, distance-1)

	if dir == "down" and block[:9] == '0'*9:
		bl = block[9:]+'0'*9
		return moveblock(bl, dir, distance-1)

	if dir == "left" and block[::3] == '0'*9:
		bl = block[1:] + '0'
		return moveblock(bl, dir, distance-1)

	if dir == "right" and block[2::3] == '0'*9:
		bl = '0'+block[:-1]
		return moveblock(bl, dir, distance-1)

	if dir == "back" and block[0:3]+block[9:12]+block[18:21] == '0'*9:
		bl = block[3:]+'000'
		return moveblock(bl, dir, distance-1)

	if dir == "front" and block[6:9]+block[15:18]+block[24:27] == '0'*9:
		bl = '000'+block[:24]
		return moveblock(bl, dir, distance-1)

	return "ERR"

# easier to use
def movexy(block, x, y, z):
	if x > 0:
		block = moveblock(block, 'right', x)
	if x < 0:
		block = moveblock(block, 'left', -x)
	if y > 0:
		block = moveblock(block, 'up', y)
	if y < 0:
		block = moveblock(block, 'down', -y)
	if z > 0:
		block = moveblock(block, 'back', z)
	if z < 0:
		block = moveblock(block, 'front', -z)
	return block

# tries to move a block -2/+2 pixels in X, Y and Z
def getAllMoves(block):
	outbl = []
	for x in range(-2, 3):
			for y in range(-2, 3):
					for z in range(-2, 3):
						obl = movexy(block, x, y, z)
						if len(obl) == 27:
							outbl.append(obl)

	return outbl

# generates a sequence for block rotation
def genseq(p):
	q = []
	for x in [0,1,2][::p[3]]:
		for y in [0,1,2][::p[4]]:
			for z in [0,1,2][::p[5]]:
				c = (x) * p[0] + (y) * p[1] + (z) * p[2]
				q.append(c)
	return q

# generates a new block using rotation sequence
def genBlockRot(sblock, seq):
	brot = ''
	for x in range(27):
		brot = brot + sblock[seq[x]]
	
	return brot

def getAllRotations(block):
	# magic values for getseq() function to perform all possible 90° rotations of a block (24 of them)
	rotationParams = [[9,3,1,1,1,1], [9,3,1,1,-1,-1], [9,3,1,-1,1,-1], [9,3,1,-1,-1,1], 
					[9,1,3,-1,1,1], [9,1,3,1,-1,1], [9,1,3,1,1,-1], [9,1,3,-1,-1,-1],
					[3,1,9,1,1,1], [3,1,9,1,-1,-1], [3,1,9,-1,1,-1], [3,1,9,-1,-1,1], 
					[3,9,1,1,1,-1], [3,9,1,1,-1,1], [3,9,1,-1,1,1], [3,9,1,-1,-1,-1],
					[1,3,9,1,1,-1], [1,3,9,1,-1,1], [1,3,9,-1,1,1], [1,3,9,-1,-1,-1], 
					[1,9,3,1,1,1], [1,9,3,1,-1,-1], [1,9,3,-1,1,-1], [1,9,3,-1,-1,1]]

	# generate translation sequences
	secs = []
	for x in rotationParams:
		secs.append(genseq(x))
	
	# generate all possible rotations of a block
	blox = []
	for x in secs:
		blox.append(genBlockRot(block, x))
	return blox
			
# combine 2 blocks using 27-char format
def combine(a, b):
	outs = ''
	for x in range(len(a)):
		if a[x] == '0' and b[x] == '0':
			outs = outs + '0'
		if a[x] != '0' and b[x] == '0':
			outs = outs + a[x]
		if a[x] == '0' and b[x] != '0':
			outs = outs + b[x]
	return outs

startTime = time.time()

allblocks = {}


#for each block..
for bl in range(len(blocks)):
	allblocks[bl] = []
	# generate all possible moves..
	moves = getAllMoves(blocks[bl])
	for x in moves:
		# for all moves, generate all possible rotations
		rotations = getAllRotations(x)
		for z in rotations:
			allblocks[bl].append(z)

# allblocks now contain all possible states of blocks in 3x3x3 cube
for x in allblocks:
	print(len(allblocks[x]))

for x in range(len(allblocks)):
	print("Block", x, "-", len(allblocks[x]),"states")
print()

outbl = {}

#fill in the initial states
for x in range(6):
	outbl[x] = []

for x in allblocks[0]:
	outbl[0].append(x)

for x in range(len(allblocks)-1):
	print("Computing stage",x, "and block",x+1)
	print("Cube states in current pool:", len(outbl[x]),"; States of current block:",len(allblocks[x+1]))
	print(len(outbl[x])*len(allblocks[x+1]), "possible combinations")

	for b1 in outbl[x]:
		for b2 in allblocks[x+1]:
			for q in range(27):		# checks if two blocks intersect
				if b1[q] != '0' and b2[q] != '0':
					break
				if q==26:		# if two blocks do not collide..
					outbl[x+1].append(combine(b1,b2))

	outbl[x+1] = set(outbl[x+1])

endTime = time.time()

print()
print(len(outbl[5]), "solutions found:")
print()

for x in outbl[5]:
	print3dblock(x)

print("Processing time: %.2fs" % (endTime-startTime))


