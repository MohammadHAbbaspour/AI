from random import randrange


class NQueens:
    def __init__(self, N):
        self.N = N

    def initial(self):
        ''' Returns a random initial state '''
        return tuple(randrange(self.N) for i in range(self.N))

    def goal_test(self, state):
        ''' Returns True if the given state is a goal state '''
        if self.value(state) == (self.N)*(self.N-1):
            return True
        return False

    def value(self, state):
        ''' Returns the value of a state. The higher the value, the closest to a goal state '''
        value = 0
        for i in range(self.N):
            # check if there is a queen in the same column
            for k in range(i+1, self.N):
                if state[i] != state[k]:
                    value += 1
            # check if there is a queen in the same diagonal
            for k in range(i+1, self.N):
                if abs(state[i]-state[k]) != abs(i-k):  # if the distance between two queens is not equal to the distance between two columns, then they are not in the same diagonal
                    value += 1
        return value

    def neighbors(self, state):
        ''' Returns all possible neighbors (next states) of a state '''
        states = [] # list of all possible neighbors
        for i in range(self.N):
            k = 1
            state_ls = list(state)  # convert tuple to list
            while state[i] + k < self.N:
                state_ls[i] = state[i] + k  # move queen to the right
                states.append(tuple(state_ls))
                k += 1 
            k = 1
            while state[i] - k >= 0:
                state_ls[i] = state[i] - k  # move queen to the left
                states.append(tuple(state_ls))
                k += 1
            k = 1
            # state_ls[i] = state[i]  # move queen to the original position
            # while i + k < self.N:
            #     if state[i] + k < self.N:
            #         state_ls[i + k] = state[i] + k  # move queen to the bottom_right diagonal
            #         states.append(tuple(state_ls))
            #     if state[i] - k >= 0:
            #         state_ls[i + k] = state[i] - k
            #         states.append(tuple(state_ls))  # move queen to the bottom_left diagonal
            #     state_ls[i + k] = state[i + k]  # move queen to the original position
            #     k += 1
            # k = 1
            # while i - k >= 0:
            #     if state[i] + k < self.N:
            #         state_ls[i - k] = state[i] + k  # move queen to the top_right diagonal
            #         states.append(tuple(state_ls))
            #     if state[i] - k >= 0:
            #         state_ls[i - k] = state[i] - k  # move queen to the top_left diagonal
            #         states.append(tuple(state_ls))
            #     state_ls[i - k] = state[i - k]  # move queen to the original position
            #     k += 1
        return states
