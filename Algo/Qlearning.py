import random
import numpy as np
import gym

# Créer fonction greedy qui détermine le temps d'exploration et le temps d'exploitation
def greedy(current_state,epsilon, q_size):
    p=random()
    
    if p<epsilon : 
        action = random(q_size) #q_size = nombre d'actions
    
    else : 
        action = MaxAction(current_state)

    return action

# Créer la fonction Qlearning
def Qlearning (reward, alpha, epsilon, gamma, nb_state = 8, nb_action = 8) : # Créer une classe 
    Q=np.zeros(nb_state,nb_action)
    nb_episodes = 200
    max_iter_episode = 50

    for i in range(nb_episodes): 
        current_state=0
        for j in range (max_iter_episode):
            action = greedy(current_state, epsilon,nb_action)

            next_step,reward

            Q[current_state,action] = (1-alpha) * Q[current_state,action] + alpha * (reward + gamma * max(Q[nb_state,nb_action]))
    



