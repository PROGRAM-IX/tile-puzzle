import random

"""
    tile_puzzle, an emulated sliding tile board and solver
    Copyright (C) 2012  James Heslin

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

class board():
    def __init__(self, size, grid=None):
        self.size = size
        if not grid == None:
            self.grid = grid
        else:
            self.grid = []
            numbers = range(0, (self.size**2))
            numbers.remove(0) # Take out leading zero
            numbers.append(0) # Drop it back in at the end
            #print numbers
            for i in xrange(0, size):
                self.grid.append(numbers[size*i:size*i+size])
            #print self.grid
            self.blank_pos = (size-1, size-1)
            #print self.grid[self.blank_pos[0]][self.blank_pos[1]]
        
        self.blank_pos = self.findblank_pos(self.grid)
        #print "Found blank_pos:", self.findblank_pos(self.grid)
        #print "Actual blank_pos:", self.blank_pos

    def findblank_pos(self, grid):
        for i in xrange(len(grid[0])):
            for j in xrange(len(grid)):
                if grid[i][j] == 0:
                    return (i, j)
        print "Couldn't find the blank tile."
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
        if not self.size == board.size:
            return False
        for i in xrange(0, self.size):
            for j in xrange(0, self.size):
                if not self.grid[i][j] == board.grid[i][j]:
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
    def tiles_out_of_place(self, goal):
        t = 0
        for i in xrange(self.size):
            for j in xrange(self.size):
                if self.grid[i][j] is not goal.grid[i][j]:
                    t += 1
        return t
        
    def moves_to_state(self, goal):
        m = 0
        tiles = []
        # Check which tiles are out of place compared to the goal state
        for i in xrange(self.size):
            for j in xrange(self.size):
                if not self.grid[i][j] == goal.grid[i][j]:
                    tiles.append((i, j, goal.grid[i][j], 0))
        # Find the Manhattan distance between goal and actual position 
        # of those tiles and add it to m
        i_diff = 0
        j_diff = 0
        for t in tiles:
            for i in xrange(self.size):
                for j in xrange(self.size):
                    if self.grid[i][j] == t[2]:
                        if i > t[0]:
                            i_diff = i - t[0]
                        else:
                            i_diff += t[0] - i
                        if j > t[1]:
                            j_diff += j - t[1]
                        else:
                            j_diff += t[1] - j
                        """# is this a corner tile?
                        if ((i == 0 and j == 0) or 
                                (i == self.size and j == 0) or
                                (i == 0 and j == self.size) or
                                (i == self.size and j == self.size)):
                            m += 1"""
                        #print i_diff, j_diff
                        m += i_diff
                        m += j_diff
                        #print m
        return m
                        

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
        #print bP, "->", self.blank_pos
        #print

    def randomise(self, iterations):
        num = 0
        print "Randomising:", iterations, "iterations"
        while num < iterations:
            direction = random.randint(0, 4)
            if self.is_valid_move(direction):
                self.move_blank(direction)
                num += 1
                #print num

def main():
    # Test the board class
    b = board(3)
    b.show_board()
    b.randomise(50)
    c = board(b.size, b.copy_grid())
    c.show_board()
    print c.is_same_grid(b)
    print c.get_legal_moves()

if __name__ == "__main__":
    main()
