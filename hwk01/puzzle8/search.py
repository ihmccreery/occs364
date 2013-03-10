# Isaac Hollander McCreery
# Nick Towbin-Jones
# Charles Marks

import puzzle8
import math
import Queue

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

def itdeep(state):
	depth = 0
	found = False
	while found == False:
		found = depthLimitedDFS(state, depth)
		#found = recdepthLimitedDFS(state, depth)
		depth += 1
	return found

# recursive implimentation of a depth-limited DFS
def depthLimitedDFS(initial_state, depth):
	fringe = Queue.LifoQueue()
	fringe.put((initial_state, []))
	while not fringe.empty():
		state, path = fringe.get()
		if state == puzzle8.solution():
			return path
		if len(path) == depth:
			continue
		zero_position = xyposition(state, 0)
		for neighbor in puzzle8.neighbors(zero_position):
			next_state = puzzle8.moveBlank(state, neighbor)
			fringe.put((next_state, path+[[zero_position, neighbor]]))
	return False

# recursive implimentation of a depth-limited DFS
def recdepthLimitedDFS(state, height):
	# if found, return
	if state == puzzle8.solution():
		return []
	# if we're at the bottom, return
	if height == 0:
		return False
	# find 0 and iterate over neighbors
	zero_position = xyposition(state, 0)
	for neighbor in puzzle8.neighbors(zero_position):
		next_result = depthLimitedDFS(puzzle8.moveBlank(state, neighbor), height-1)
		# if next_result is a list, we've found a solution
		if isinstance(next_result, list):
			return [[zero_position, neighbor]] + next_result
	# we're out of things to do
	return False

def astar(initial_state, heuristic):
	fringe = Queue.PriorityQueue()
	fringe.put((0+heuristic(initial_state), initial_state, []))
	while True:
		h, state, path = fringe.get()
		if state == puzzle8.solution():
			return path
		zero_position = xyposition(state, 0)
		for neighbor in puzzle8.neighbors(zero_position):
			next_state = puzzle8.moveBlank(state, neighbor)
			# note: we add neighbor/10. to make sure that neighbors are taken out in the appropriate order
			fringe.put((len(path)+1+heuristic(next_state)+neighbor/10., next_state, path+[[zero_position, neighbor]]))

def xyposition(state, tile):
	for i in range(9):
		if puzzle8.getTile(state, i) == tile:
			return i
