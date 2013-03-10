import othelloBoard

'''You should modify the chooseMove code for the ComputerPlayer
class. You should also modify the heuristic function, which should
return a number indicating the value of that board position (the
bigger the better). We will use your heuristic function when running
the tournament between players.

Feel free to add additional methods or functions.'''

white = 1
black = -1

multipliers = [4, 1, 3, 2, 2, 3, 1, 4]

class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
        
    def chooseMove(self,board):
        while True:
            try:
                move = eval('(' + raw_input(self.name + \
                 ': enter row, column (or type "0,0" if no legal move): ') \
                 + ')')

                if len(move)==2 and type(move[0])==int and \
                   type(move[1])==int and (move[0] in range(1,9) and \
                   move[1] in range(1,9) or move==(0,0)):
                    break

                print 'Illegal entry, try again.'
            except Exception:
                print 'Illegal entry, try again.'

        if move==(0,0):
            return None
        else:
            return move

# bogusHVal = -1
# def heuristic(board):
#     global bogusHVal 
#     bogusHVal += 1
#     #print "bogusHVal returned: " + str(bogusHVal//4)
#     return bogusHVal//4

def heuristic(board):
    '''This very silly heuristic just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''

    # possibilities:
    #   - corner pieces worth much more
    #   - side pieces worth some more
    #
    #   - mod row / column index

    sum = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1,othelloBoard.size-1):
            sum += board.array[i][j]*multipliers[i-1]*multipliers[j-1]
    return sum

def finalHeuristic(board):
    '''This just counts up who wins, and returns
    +/-infty based on who has won'''

    sum = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1,othelloBoard.size-1):
            sum += board.array[i][j]
    if sum > 0:
        return sum*100000
        # return float("inf")

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies):
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies

    def chooseMove(self,board):
        a = float("-inf")
        b = float("inf")
        '''alpha-beta pruning'''
        if self.color == black:
            #print "MIN PLAYER:"
            minMove = None
            for i in range(1,othelloBoard.size-1):
                for j in range(1,othelloBoard.size-1):
                    bcopy = board.makeMove(i,j,self.color)
                    if bcopy:
                        #print 'Min: trying position "' + str(i) + ", " + str(j) + '"'
                        v = self.alphaBeta(bcopy,white,self.plies-1,a,b,False)
                        if v < b:
                            b = v
                            minMove = (i,j)
            return minMove
        else:
            #print "MAX PLAYER:"
            maxMove = None
            for i in range(1,othelloBoard.size-1):
                for j in range(1,othelloBoard.size-1):
                    bcopy = board.makeMove(i,j,self.color)
                    if bcopy:
                        #print 'Max: trying position "' + str(i) + ", " + str(j) + '"'
                        v = self.alphaBeta(bcopy,black,self.plies-1,a,b,False)
                        if v > a:
                            a = v
                            maxMove = (i,j)
            return maxMove

    def alphaBeta(self,board,color,plies,a,b,lastPass):
        #print "a,b: " + str(a) + "," + str(b)
        if (plies == 0):
            return self.heuristic(board)
        if color == black:
            #print "MIN PLAYER:"
            v = float("inf")
            seenLegalMove = False
            for i in range(1,othelloBoard.size-1):
                for j in range(1,othelloBoard.size-1):
                    bcopy = board.makeMove(i,j,color)
                    if bcopy:
                        #print 'Min: trying position "' + str(i) + ", " + str(j) + '"'
                        seenLegalMove = True
                        v = min(v,self.alphaBeta(bcopy,white,plies-1,a,b,False))
                        if v <= a:
                            #print "MIN is PRUNING! Because minV: " + str(v) + " is <= a:" + str(b)
                            return v
                        b = min(b,v)
            if seenLegalMove:
                return v
            else:
                if not lastPass:
                    board.display()
                    return self.alphaBeta(board,white,plies-1,a,b,True)
                else:
                    board.display()
                    return finalHeuristic(board)
        else:
            #print "MAX PLAYER:"
            v = float("-inf")
            seenLegalMove = False
            for i in range(1,othelloBoard.size-1):
                for j in range(1,othelloBoard.size-1):
                    bcopy = board.makeMove(i,j,color)
                    if bcopy:
                        #print 'Max: trying position "' + str(i) + ", " + str(j) + '"'
                        seenLegalMove = True
                        v = max(v,self.alphaBeta(bcopy,black,plies-1,a,b,False))
                        if v >= b:
                            #print "MAX is PRUNING! Because maxV: " + str(v) + " is >= b:" + str(b)
                            return v
                        a = max(a,v)
            if seenLegalMove:
                return v
            else:
                if not lastPass:
                    board.display()
                    return self.alphaBeta(board,black,plies-1,a,b,True)
                else:
                    board.display()
                    return finalHeuristic(board)
