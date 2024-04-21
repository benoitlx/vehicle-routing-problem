import random
import numpy as np
from voisinnage import *


# Créer fonction greedy qui détermine le temps d'exploration et le temps d'exploitation
def greedy(current_state,epsilon, Q):
    p=random()
    
    if p<epsilon : 
        action = random(len(Q[0])) #nombre d'actions = nbr de colonnes de Q
    
    else : 
        action = np.argmax(Q[current_state])

    return action

#Procédure pour choisir la prochaine action à affectuer : 
def choose_an_action(state, type_function, epsilon, Q):
    next_state = 0
    if type_function == 1:
        next_state = greedy(state, epsilon, Q)
    else:
        if type_function == 2:
            next_state = randomAction()
    return next_state

def randomAction(L) : 
    a = intra_route_swap(L)
    b = inter_route_swap(L)
    c = intra_route_shift(L)
    d = inter_route_shift(L)
    e = two_intra_route_swap(L)
    f = two_intra_route_shift(L)
    g = elimine_petite_route(L)
    h = elimine_route(L)

    return random.choice([a,b,c,d,e,f,g,h])

class Qlearning:
    NBR_OF_ACTION = 8

    solution = []
    fitness_evolution = []
    fitness = 0

    epsilon = 0

    def __init__(self, graph=None, max_iteration=50, epsilon=0.8, alpha=0.1, gamma=0.9):
        if graph is None:
            database = Database()
            graph = database.Graph

        # TODO: Replace the defaults values taken from the lectures by more efficient values
        self.MAX_ITERATION = max_iteration

        self.Graph = graph

        self.Q = np.zeros((self.NBR_OF_ACTION, self.NBR_OF_ACTION))

        self.initial_epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    """
    Fonction principale, applique l'apprentissage à notre problème
    
    Returns
    -------
    solution: list - the best solution to the problem
    -------
    """

    def main(self, initial_solution=None):
        if initial_solution is None:
            ga = GeneticAlgorithm(graph=self.Graph)
            ga.main()
            initial_solution = ga.solution

        self.Q = np.zeros((self.NBR_OF_ACTION, self.NBR_OF_ACTION))
        self.epsilon = self.initial_epsilon

        self.fitness_evolution = []
        no_improvement = 0

        best_solution = initial_solution
        current_solution = initial_solution

        best_fitness = compute_fitness(best_solution, self.Graph)

        iteration = 0
        progress_bar = tqdm(desc='Q-Learning', total=self.MAX_ITERATION, colour='green')

        while iteration < self.MAX_ITERATION and self.is_fitness_evolving():
            iteration += 1

            visited_states = []

            next_state = rd.randint(0, self.NBR_OF_ACTION - 1)
            new_solution = perform_action(next_state, current_solution)

            visited_states.append(next_state)

            if is_solution_valid(new_solution, self.Graph):
                current_solution = new_solution

            current_solution_fitness = compute_fitness(current_solution, self.Graph)

            if current_solution_fitness < best_fitness:
                best_solution = current_solution
                best_fitness = current_solution_fitness
            else:
                is_not_stuck = True

                while is_not_stuck:
                    current_state = next_state

                    if no_improvement == 0:
                        next_state = self.epsilon_greedy(next_state)
                    else:
                        next_state = rd.randint(0, self.NBR_OF_ACTION - 1)

                    current_solution = perform_action(next_state, current_solution)
                    current_solution_fitness = compute_fitness(current_solution, self.Graph)

                    if next_state not in visited_states:
                        visited_states.append(next_state)

                    if current_solution_fitness < best_fitness and is_solution_valid(current_solution, self.Graph):
                        best_solution = current_solution
                        best_fitness = current_solution_fitness

                        no_improvement = 0
                        reward = (10 ** 8) / best_fitness

                        self.Q = self.compute_qtable(current_state, next_state, reward)
                    else:
                        no_improvement += 1

                        if no_improvement > self.MAX_ITERATION and len(visited_states) == self.NBR_OF_ACTION:
                            is_not_stuck = False

                self.epsilon = self.compute_epsilon(iteration)

            self.fitness_evolution.append(best_fitness)
            progress_bar.update(1)

        self.solution = best_solution
        self.fitness = best_fitness

        plot_solution(self.solution, self.Graph, title='Q-Learning solution')

    """
    Select an action to perform that maximize the reward
     
    Parameters
    ----------
    current_state: int - the index of the current action performed
    ----------
    
    Returns
    -------
    next_state: int - the index of the next action to perform
    -------
    """

    def select_best_action(self, current_state):
        reward_max = 0
        next_state = 0

        for index_state in range(len(self.Q)):
            if self.Q[current_state][index_state] > reward_max:
                reward_max = self.Q[current_state][index_state]
                next_state = index_state

        return next_state

    """
    Select the next action to perform, which can either be randomly selected or chosen to maximize reward
    
    Parameters
    ----------
    current_state: int - the current action performed
    ----------
    
    Returns
    -------
    next_state: int - the next action to perform
    -------
    """

    def epsilon_greedy(self, current_state):
        random_proba = rd.random()

        if random_proba < self.epsilon:
            next_state = rd.randint(0, self.NBR_OF_ACTION - 1)
        else:
            next_state = self.select_best_action(current_state)

        return next_state

    """
    Update the Q value
    
    Parameters
    ----------
    state
    next_state
    reward
    ----------
    """

    def compute_qtable(self, state, next_state, reward):
        qtable = deepcopy(self.Q)

        qtable_max = max(self.Q[next_state - 1])
        increase = self.alpha * (reward + self.gamma * qtable_max - self.Q[state - 1][next_state - 1])
        qtable[state - 1][next_state - 1] += np.around(increase, decimals=2)

        return qtable

    def compute_epsilon(self, nbr_of_iteration):
        decay_rate = 1 / (1 + np.sqrt(nbr_of_iteration))
        return self.epsilon * decay_rate

    def is_fitness_evolving(self):
        if len(self.fitness_evolution) < 5:
            return True

        last_fitness = self.fitness_evolution[-1]

        index = len(self.fitness_evolution) - 2

        while index >= 0:
            fitness = self.fitness_evolution[index]

            if fitness != last_fitness:
                return True

            index -= 1

        return False


class EnvGrid(object):
    """
        docstring forEnvGrid.
    """
    def __init__(self):
        super(EnvGrid, self).__init__()

        # Je définis ma grille & les récompenses
        self.grid = [
            [0, 0, 1],
            [0, -1, 0],
            [0, 0, 0]
        ]
        # Je définis la position initiale
        self.y = 2
        self.x = 0

        # Je définis les actions possibles

        self.actions = [
            [-1, 0], # Up
            [1, 0], #Down
            [0, -1], # Left
            [0, 1] # Right
        ]

    # Je définis une fonction qui reset l'environnement aux valeurs de base

    def reset(self):
        """
            Reset world
        """
        self.y = 2
        self.x = 0
        return (self.y*3+self.x+1)

    
    # Je définis une fonction pour se dépalcer dans l'environnement
    def step(self, action):
        """
            Action: 0, 1, 2, 3
        """
        self.y = max(0, min(self.y + self.actions[action][0],2))
        self.x = max(0, min(self.x + self.actions[action][1],2))
        return (self.y*3+self.x+1) , self.grid[self.y][self.x]

    
    # Je définis une fonction pour afficher l'environnement actuel
    def show(self):
        """
            Show the grid
        """
        print("---------------------")
        y = 0
        for line in self.grid:
            x = 0
            for pt in line:
                print("%s\t" % (pt if y != self.y or x != self.x else "X"), end="")
                x += 1
            y += 1
            print("")

    # Je définis une fonction pour vérifier si j'ai terminé dans l'environnement 
    # i.e. la voiture a trouvé la maison dans la grille

    def is_finished(self):
        return self.grid[self.y][self.x] == 1


if __name__ == '__main__':
    env = EnvGrid()
    st = env.reset()

    Q = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    for _ in range(100):
        # Reset the game
        #Je récupère l'état actuel
        st = env.reset()
    
        while not env.is_finished():
            #env.show()
            #demande quelles actions je vais effectuer 
            #at = int(input("$>"))
            
            
            #je choisis une action


            at = greedy(st, Q, 0.8)

            #je me déplace dans l'environnement en utilisant l'action que j'ai utilisée
            #retourne 2 valeurs : stp1 : le nouvel etat dans le quel je me retrouve & r: la récompense
            
            stp1, r = env.step(at)
            #print("s", stp1)
            #print("r", r)

            # Update Q function
            # chercher atp1, epsilon = 0 pour etre sur que  je fais de l'exploitation pour trouver l'epérance max à t+1
            atp1 = greedy(stp1, Q, 0.0)
            # learning rate=0.1 , gamma=0.9 (à quel point je donne de l'importance aux récompenses futures)
            Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])
            # le prochain état sera l'état à t+1 et on recommence
            st = stp1
    for s in range(1, 10):
        print(s, Q[s])


