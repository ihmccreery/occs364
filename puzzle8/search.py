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
	manhattanDistance = 0
	for i in range(9):
		tile = puzzle8.getTile(state, i)
		j = xyposition(puzzle8.solution(), tile)
		manhattanDistance += math.fabs(puzzle8.xylocation(i)[0] - puzzle8.xylocation(j)[0])
		manhattanDistance += math.fabs(puzzle8.xylocation(i)[1] - puzzle8.xylocation(j)[1])
	return manhattanDistance

def xyposition(state, tile):
	for i in range(9):
		if puzzle8.getTile(state, i) == tile:
			return i
