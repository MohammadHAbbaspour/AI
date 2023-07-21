from Algorithm import Algorithm
from Constants import NO_OF_CELLS
import time


class A_STAR(Algorithm):
    def __init__(self, grid):
        super().__init__(grid)

    def run_algorithm(self, snake):
        #################################################################################
        # "*** YOUR CODE HERE ***"
        #################################################################################
        src, t = self.get_initstate_and_goalstate(snake)
        if not self.path:
            v = self.grid[src.x][src.y]
            for i in range(NO_OF_CELLS):
                for j in range(NO_OF_CELLS):
                    self.grid[i][j].parent = None
                    self.grid[i][j].f = 0
                    self.grid[i][j].g = 0
                    self.grid[i][j].h = self.manhattan_distance(self.grid[i][j], t)
            self.explored_set = []
            self.frontier = []
            v.g = 0
            self.frontier.append(v)
            start_time = time.time()
            while self.frontier and not v.equal(t) and time.time() - start_time < 0.05:
                v = self.frontier.pop()
                self.explored_set.append(v)
                for u in self.get_neighbors(v):
                    if not (u in self.explored_set) and not self.inside_body(snake, u) \
                        and not self.outside_boundary(u):
                            u.g = v.g + 1
                            u.f = u.g + u.h
                            u.parent = v
                            self.frontier.append(u)
                self.frontier.sort(key=lambda node : node.f, reverse=True)
            node = self.get_path(self.grid[t.x][t.y])
            if node.parent != None:
                return node
        node = None
        neighbors = self.get_neighbors(src)
        for neighbor in neighbors:
            if not self.inside_body(snake, neighbor) and not self.outside_boundary(neighbor):
                node = neighbor
        return self.path.pop() if self.path else node
