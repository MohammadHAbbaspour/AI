from NQueens import NQueens


def hill_climbing(problem : NQueens):
    ''' Returns a state as the solution of the problem '''
    current_state = problem.initial()   # get a random initial state
    while True: # loop until a goal state is found
        neighbors = problem.neighbors(current_state)    # get all possible neighbors
        neighbor = max(neighbors, key=lambda x: problem.value(x))   # get the neighbor with the highest value
        if problem.value(neighbor) <= problem.value(current_state): # if the neighbor has a lower value than the current state, then the current state is a local maximum
            return current_state
        current_state = neighbor    # update the current state

def hill_climbing_random_restart(problem, limit = 10):
    state = problem.initial()   
    cnt = 0 
    while problem.goal_test(state) == False and cnt < limit:    
        state = hill_climbing(problem)  
        cnt += 1
    return state
