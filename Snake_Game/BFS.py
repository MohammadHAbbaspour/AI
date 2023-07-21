from collections import deque
from Snake import Snake
from Utility import Node
from Algorithm import Algorithm
from Constants import NO_OF_CELLS

FIRST = True

class BFS(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake : Snake):
        #################################################################################
        # "*** YOUR CODE HERE ***"
        src, t = self.get_initstate_and_goalstate(snake)
        if not self.path:
            s = self.grid[src.x][src.y]
            for i in range(NO_OF_CELLS):
                for j in range(NO_OF_CELLS):
                    self.grid[i][j].parent = None
            self.frontier = []
            self.explored_set = []
            self.frontier.append(s)
            while self.frontier:
                s = self.frontier.pop(0)
                neighbors = self.get_neighbors(s)
                for neighbor in neighbors:
                    if not (neighbor in self.explored_set) and not self.inside_body(snake, neighbor) \
                    and not self.outside_boundary(neighbor):
                        self.frontier.append(neighbor)
                        self.explored_set.append(neighbor)
                        neighbor.parent = s
            node = self.get_path(self.grid[t.x][t.y])
            if node.parent != None:
                return node
        node = None
        for neighbor in self.get_neighbors(src):
            if not self.inside_body(snake, neighbor) and not self.outside_boundary(neighbor):
                node = neighbor
                break
        return self.path.pop() if self.path else node
        #################################################################################
