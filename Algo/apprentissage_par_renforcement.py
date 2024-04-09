from voisinnage import *
from Qlearning import *

def randomAction(state):
    f = random.choice(intra_route_swap, inter_route_swap, intra_route_shift, inter_route_shift, two_intra_route_swap, two_intra_route_shift, elimine_petite_route, elimine_route)
    return f

def choose_an_action(state, type_function, epsilon, q_size):
    next_state = 0
    if type_function == 1:
        next_state = greedy(state, epsilon, q_size)
    else:
        if type_function == 2:
            next_state = randomAction(state)
    return next_state

