import random

class board():
    def __init__(self, size, grid=None):
        self.size = size
        if grid != None:
            self.grid = grid
        else:
            self.grid = []
            numbers = range(0, (self.size**2))
            numbers.remove(0) # Take out leading zero
            numbers.append(0) # Drop it back in at the end
            #print numbers
            for i in xrange(0, size):
                self.grid.append(numbers[size*i:size*i+size])
            print self.grid
            self.blankPos = (size-1, size-1)
            print self.grid[self.blankPos[0]][self.blankPos[1]]
        
        self.blankPos = self.findBlankPos(self.grid)
        #print "Found blankPos:", self.findBlankPos(self.grid)
        #print "Actual blankPos:", self.blankPos

    #def __init__(self, grid, size):
        #self.grid = grid
        #self.size = size
    def findBlankPos(self, grid):
        for i in xrange(len(grid[0])):
            for j in xrange(len(grid)):
                if grid[i][j] == 0:
                    return (i, j)
        print "Well done, genius. Couldn't find the blank tile."
        return (0, 0)

    def copyGrid(self):
        l = []
        for i in list(self.grid):
            e = (list(i))
            l.append(e)
        #print l
        return l

    def getLegalMoves(self):
        moves = []
        for i in range(0, 4):
            if self.isValidMove(i):
                b = board(self.size, self.copyGrid())
                b.moveBlank(i)
                moves.append(b)
        #print moves
        return moves

    def isSameGrid(self, board):
        if self.size != board.size:
            return False
        for i in xrange(0, self.size):
            for j in xrange(0, self.size):
                if self.grid[i][j] != board.grid[i][j]:
                    return False
        return True

    def getBlankPos(self):
        return self.blankPos

    def showBoard(self):
        for i in self.grid:
            line = "|"
            for j in i:
                if j < 10:
                    line += " " 
                line += str(j)
                line += "|"
            print line
        print ""

    def isValidMove(self, direction): 
        if direction == 3: # up
            if self.blankPos[0] < 1:
                return False
            else:
                #print ("Can move up from", str(self.blankPos[0]), 
                    #str(self.blankPos[1]))
                return True
        elif direction == 2: # right
            if self.blankPos[1] > self.size-2:
                return False
            else:
                #print ("Can move right from", str(self.blankPos[0]), 
                    #str(self.blankPos[1]))
                return True
        elif direction == 1: # down
            if self.blankPos[0] > self.size-2:
                return False
            else:
                #print ("Can move down from", str(self.blankPos[0]),
                    #str(self.blankPos[1]))
                return True
        elif direction == 0: # left
            if self.blankPos[1] < 1:
                return False
            else:
                #print ("Can move left from", str(self.blankPos[0]), 
                    #str(self.blankPos[1]))
                return True


    def moveBlank(self, direction): # 3: up 2: right 1: down 0: left
        #if self.isValidMove(direction):
        bP = self.blankPos
        #print bP
        if direction == 0: # left
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]][bP[1]-1])
            self.grid[bP[0]][bP[1]-1] = 0
            self.blankPos = (bP[0], bP[1]-1)

        elif direction == 1: # down
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]+1][bP[1]])
            self.grid[bP[0]+1][bP[1]] = 0
            self.blankPos = (bP[0]+1, bP[1]) 
            
        elif direction == 2: # right
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]][bP[1]+1])
            self.grid[bP[0]][bP[1]+1] = 0
            self.blankPos = (bP[0], bP[1]+1)
            
        elif direction == 3: # up
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]-1][bP[1]])
            self.grid[bP[0]-1][bP[1]] = 0
            self.blankPos = (bP[0]-1, bP[1])
        #self.showBoard()
        print bP, "->", self.blankPos
        print

    def randomise(self, iterations):
        num = 0
        while num < iterations:
            direction = random.randint(0, 4)
            if self.isValidMove(direction):
                self.moveBlank(direction)
                num += 1
                #print num

    #def solve(self, bP):

def main():
    b = board(3)
    b.showBoard()
    #b.randomise(50)
    c = board(b.size, b.copyGrid())
    c.showBoard()
    print c.isSameGrid(b)
    print c.getLegalMoves()

if __name__ == "__main__":
    main()
