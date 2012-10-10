import sys
import getopt
from board import *

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

class a_star_node():
    def __init__(self, state, h_val, path=None):
        self.state = state
        self.h_val = h_val
        if path != None:
            self.path = path
        self.path = []

    def get_children(self, depth):
        """Return a collection of the child states available"""

    def get_state(self):
        """Return the current state"""
        return self.state

    def state_in_list(state, c_list):
        """Check if state is in a given list"""

    def show_state(self):
        """Show the state"""

    def equals(self, node):
        """Check if this state matches node's state"""

class tile_puzzle_a_star_node(a_star_node):
    def get_children(self, depth):
        m = self.state.get_legal_moves()
        c = []
        for l in m:
            c.append(tile_puzzle_a_star_node(l, depth))
        return c
    
    def show_state(self):
        self.state.show_board()

    def equals(self, node):
        if self.state.is_same_grid(node.state):
            return True
        else:
            return False


class a_star_solver():
    def state_in_list(self, state, c_list):
        for c in c_list:
            if c.equals(state):
                return c
        return None

    def remove_non_optimal(self, open_list, depth):
        # This always seems to remove too many nodes
        if len(open_list) == 0:
            return
        else:
            for x in open_list:
                if (x.h_val - depth) > (depth * 4):
                    open_list.remove(x)

    def sort_open(self, open_list):
        if len(open_list) == 0:
            return
        else:
            base = open_list[0].h_val
            # get lowest h_val
            for x in open_list:
                if base < x.h_val:
                    base = x.h_val
            for i in open_list:
                if i.h_val > base:
                    open_list.remove(i)
                    open_list.append(i)

    def evaluate(self, board, goal, depth):
        board.h_val = depth
        board.h_val += board.get_state().tiles_out_of_place(
                goal.get_state())
        board.h_val += board.get_state().moves_to_state(
                goal.get_state())

    def a_star(self, start, goal):
        open_list = [start]
        out_of_place = start.get_state().tiles_out_of_place(
                goal.get_state())
        print "Tiles out of place:", out_of_place
        print "Isolated moves from goal state:", (
        start.get_state().moves_to_state(goal.get_state()))
        closed_list = []
        depth = 0
        count = 0
        while len(open_list) > 0:
            #print open_list[0].get_state()
            x = open_list.pop(0)
            if len(x.path) > depth:
                depth = len(x.path)
                print depth
            #print x.get_state()
            #x_state = x.get_state()
            if x.equals(goal):
                # Return path from start to x
                print "Found it after", depth, "moves"
                print "Total children added to open list:", count
                x.show_state()
                return x.path + [x]
            else:
                # get a list of x's children 
                children = x.get_children(depth) 
                for c in children:
                    # if c is already in the list
                    child_open = self.state_in_list(c, open_list)
                    child_closed = self.state_in_list(c, closed_list)
                    # if c is already in open_list
                    if child_open is not None:
                        # if child's path < c's path
                        if len(child_open.path) < len(c.path):
                            # give child c's path
                            child_open.path = c.path 
                    # if child is already in closed_list
                    elif child_closed is not None:
                        # if child's path < c's path
                        if len(child_closed.path) < len(c.path):
                            # take child off closed list
                            closed_list.remove(child_closed)
                            # add child to open list
                            open_list.append(child_closed)
                            #print "Added", child_closed.state.show_board()
                    else:    
                        self.evaluate(c, goal, depth)
                        #print depth
                        #if depth < c.h_val - depth:
                            #print "Added\n", c.state.show_board()
                        open_list.append(c)
                        count += 1
                        p = x.path[:]
                        p.extend(c.path[:])
                        c.path = p
                        c.path.append(x)
                            
                        #print "appended", x, "to", c, "path"
                        #print depth
                        #print c.path
            closed_list.append(x)
            # v Work on this - need to prune somehow
            #self.remove_non_optimal(open_list, depth)
            self.sort_open(open_list)
        print "Did not find solution"
        return None

def main():
    #print sys.argv
    if len(sys.argv) > 1:
        if str.isdigit(sys.argv[1]) and sys.argv[1] > 1:
            size = int(sys.argv[1])
            print "Size:", size
        else:
            print "Usage: python solver.py <board size> <random iterations>"
            size = 2
            print "Size:", size
    else:
        size = 2
        print "Size:", size
    if len(sys.argv) > 2:
        if str.isdigit(sys.argv[2]) and sys.argv[2] >= 0:
            random_iter = int(sys.argv[2])
            print "Random iterations:", random_iter
        else:
            print "Usage: python solver.py <board size> <random iterations>"
            random_iter = 5
            print "Random iterations:", random_iter
    else:
        random_iter = 5
        print "Random iterations:", random_iter
    b = board(size)
    c = board(b.size, b.copy_grid())
    c.randomise(random_iter)
    b_node = tile_puzzle_a_star_node(b, 0)
    c_node = tile_puzzle_a_star_node(c, 0)
    print "start:", b_node
    print "goal:", c_node
    solver = a_star_solver()
    steps = solver.a_star(c_node, b_node)
    for step in steps:
        step.show_state()
    # steps includes the goal as well so -1 is the moves
    print "Did it in", len(steps)-1, "moves."
    

if __name__ == "__main__":
    main()
