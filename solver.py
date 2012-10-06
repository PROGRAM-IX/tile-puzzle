from board import *

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

    def equals(self, node):
        """Check if this state matches node's state"""
        if self.state.isSameGrid(node.state):
            return True
        else:
            return False

class tile_puzzle_a_star_node(a_star_node):
    def get_children(self, depth):
        m = self.state.getLegalMoves()
        c = []
        for l in m:
            c.append(tile_puzzle_a_star_node(l, depth))
        return c
    
    def equals(self, node):
        if self.state.isSameGrid(node.state):
            return True
        else:
            return False


class a_star_solver():
    def state_in_list(self, state, c_list):
        for c in c_list:
            if c.equals(state):
                return c
        return None
    
    def sort_open(self, open_list):
        if len(open_list) == 0:
            return
        else:
            base = open_list[0].hVal
            # get lowest hVal
            for x in open_list:
                if base < x.hVal:
                    base = x.hVal
            for i in open_list:
                if i.hVal > base:
                    open_list.remove(i)
                    open_list.append(i)

    def evaluate(self, board, goal, depth):
        board.hVal = depth
        g = goal.get_state()
        for i in xrange(board.state.size):
            for j in xrange(board.state.size):
                if board.state.grid[i][j] != g.grid[i][j]:
                    board.hVal += 1

    def a_star(self, start, goal):
        open_list = [start]
        closed_list = []
        depth = 0
        while len(open_list) > 0:
            depth += 1
            #print open_list[0].get_state()
            x = open_list.pop(0)
            #print x.get_state()
            x_state = x.get_state()
            if x_state.isSameGrid(goal.get_state()):
                # Return path from start to x
                print "FOUND IT"
                x_state.showBoard()
                return x.path
            else:
                # get a list of x's children 
                children = x.get_children(depth) 
                for c in children:
                    # if c is already in the list
                    child_open = self.state_in_list(c, open_list)
                    child_closed = self.state_in_list(c, closed_list)
                    # if c is already in open_list
                    if child_open is not None:
                        # if c's path < child's path
                        if len(child_open.path) < len(c.path):
                            # give child c's path
                            child_open.path = c.path 
                    elif child_closed is not None:
                        if len(child_closed.path) < len(c.path):
                            closed_list.remove(child)
                            open_list.append(child)
                            child_closed.path = c.path + c 
                            print "Added", child_closed.state.showBoard()
                    else:    
                        self.evaluate(c, goal, depth)
                        open_list.append(c)
                        print "Added\n", c.state.showBoard()
            closed_list.append(x)
            self.sort_open(open_list)
        return ["Derp", "Derp", "Derp"]

def main():
    b = board(3)
    c = board(b.size, b.copyGrid())
    c.randomise(50)
    b_node = tile_puzzle_a_star_node(b, 0)
    c_node = tile_puzzle_a_star_node(c, 0)
    solver = a_star_solver()
    print solver.a_star(c_node, b_node)

if __name__ == "__main__":
    main()
