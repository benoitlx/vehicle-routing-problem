from voisinnage.py import *
from Qlearning.py import *


def choose_an_action(state, type_function):
    next_state = 0
    if type_function == 1:
        next_state = greedy(state)
    else:
        if type_function == 2:
            next_state = randomAction()
    return next_state