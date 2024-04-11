import numpy as np

class QLearningAgent:
    def __init__(self, num_states=8, num_actions=8, alpha=0.1, gamma=0.9, epsilon=0.8): #epsilon 0.8 ?
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha  # Taux d'apprentissage
        self.gamma = gamma  # Facteur d'actualisation
        self.epsilon = epsilon  # Taux d'exploration
        self.q_table = np.zeros((num_states, num_actions))  # Initialisation de la table Q
        self.previous_state = 0

    def e_greedy(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            # Exploration : choisissez une action aléatoire
            action = np.random.randint(0, self.num_actions)
        else:
            # Exploitation : choisissez l'action avec la plus grande valeur Q
            action = np.argmax(self.q_table[state])
        return action

    def update_q_table(self, state, action, reward, next_state):
        # Mise à jour de la table Q en utilisant l'équation de mise à jour du Q-learning
        self.q_table[state, action] += self.alpha * (reward + self.gamma * np.max(self.q_table[next_state]) - self.q_table[state, action])
        #self.previous_state = action
    
    def reward(self,cost_after, cost_before):
        return cost_before - cost_after
