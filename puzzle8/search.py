# Isaac Hollander McCreery
# Nick Towbin-Jones
# Charles Marks

import puzzle8
import math

def numWrongTiles(state):
	numWrongTiles = 0
	for i in range(9):
		if puzzle8.getTile(state, i) != puzzle8.getTile(puzzle8.solution(), i):
			numWrongTiles += 1
	return numWrongTiles

def manhattanDistance(state):
	distance = 0
	for x in range(9):
		tile = puzzle8.getTile(state, x)
		y = xyposition(state, tile)
		distance += math.fabs(puzzle8.xylocation(x)[0] - puzzle8.xylocation(y)[0])
		distance += math.fabs(puzzle8.xylocation(x)[1] - puzzle8.xylocation(y)[1])
	return distance

def xyposition(state, tile):
	for i in range(9):
		if puzzle8.getTile(state, i) == tile:
			return i
