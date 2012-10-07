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
            self.blank_pos = (size-1, size-1)
            print self.grid[self.blank_pos[0]][self.blank_pos[1]]
        
        self.blank_pos = self.findblank_pos(self.grid)
        #print "Found blank_pos:", self.findblank_pos(self.grid)
        #print "Actual blank_pos:", self.blank_pos

    #def __init__(self, grid, size):
        #self.grid = grid
        #self.size = size
    def findblank_pos(self, grid):
        for i in xrange(len(grid[0])):
            for j in xrange(len(grid)):
                if grid[i][j] == 0:
                    return (i, j)
        print "Well done, genius. Couldn't find the blank tile."
        return (0, 0)

    def copy_grid(self):
        l = []
        for i in list(self.grid):
            e = (list(i))
            l.append(e)
        #print l
        return l

    def get_legal_moves(self):
        moves = []
        for i in range(0, 4):
            if self.is_valid_move(i):
                b = board(self.size, self.copy_grid())
                b.move_blank(i)
                moves.append(b)
        #print moves
        return moves

    def is_same_grid(self, board):
        if self.size != board.size:
            return False
        for i in xrange(0, self.size):
            for j in xrange(0, self.size):
                if self.grid[i][j] != board.grid[i][j]:
                    return False
        return True

    def get_blank_pos(self):
        return self.blank_pos

    def show_board(self):
        for i in self.grid:
            line = "|"
            for j in i:
                if j < 10:
                    line += " " 
                line += str(j)
                line += "|"
            print line
        print ""

    def is_valid_move(self, direction): 
        if direction == 3: # up
            if self.blank_pos[0] < 1:
                return False
            else:
                #print ("Can move up from", str(self.blank_pos[0]), 
                    #str(self.blank_pos[1]))
                return True
        elif direction == 2: # right
            if self.blank_pos[1] > self.size-2:
                return False
            else:
                #print ("Can move right from", str(self.blank_pos[0]), 
                    #str(self.blank_pos[1]))
                return True
        elif direction == 1: # down
            if self.blank_pos[0] > self.size-2:
                return False
            else:
                #print ("Can move down from", str(self.blank_pos[0]),
                    #str(self.blank_pos[1]))
                return True
        elif direction == 0: # left
            if self.blank_pos[1] < 1:
                return False
            else:
                #print ("Can move left from", str(self.blank_pos[0]), 
                    #str(self.blank_pos[1]))
                return True


    def move_blank(self, direction): # 3: up 2: right 1: down 0: left
        #if self.is_valid_move(direction):
        bP = self.blank_pos
        #print bP
        if direction == 0: # left
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]][bP[1]-1])
            self.grid[bP[0]][bP[1]-1] = 0
            self.blank_pos = (bP[0], bP[1]-1)

        elif direction == 1: # down
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]+1][bP[1]])
            self.grid[bP[0]+1][bP[1]] = 0
            self.blank_pos = (bP[0]+1, bP[1]) 
            
        elif direction == 2: # right
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]][bP[1]+1])
            self.grid[bP[0]][bP[1]+1] = 0
            self.blank_pos = (bP[0], bP[1]+1)
            
        elif direction == 3: # up
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]-1][bP[1]])
            self.grid[bP[0]-1][bP[1]] = 0
            self.blank_pos = (bP[0]-1, bP[1])
        #self.show_board()
        print bP, "->", self.blank_pos
        print

    def randomise(self, iterations):
        num = 0
        while num < iterations:
            direction = random.randint(0, 4)
            if self.is_valid_move(direction):
                self.move_blank(direction)
                num += 1
                #print num

    #def solve(self, bP):

def main():
    b = board(3)
    b.show_board()
    #b.randomise(50)
    c = board(b.size, b.copy_grid())
    c.show_board()
    print c.is_same_grid(b)
    print c.get_legal_moves()

if __name__ == "__main__":
    main()
