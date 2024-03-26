import numpy as np
import random as rd
import matplotlib.pyplot as plt

class Client:
    def __init__(self, id, demand, x, y):
        self.id = id
        self.demand = demand
        self.x = x
        self.y = y

    def distance_to(self, other_client):
        return np.sqrt((self.x - other_client.x)**2 + (self.y - other_client.y)**2)

class Vehicle:
    def __init__(self, capacity):
        self.capacity = capacity
        self.route = []

    def add_client(self, client):
        self.route.append(client)

    def total_distance(self):
        total = 0
        for i in range(len(self.route) - 1):
            total += self.route[i].distance_to(self.route[i+1])
        return total

class Solution:
    def __init__(self, clients, vehicles):
        self.clients = clients
        self.vehicles = vehicles

    def evaluate(self):
        total_distance = 0
        for vehicle in self.vehicles:
            total_distance += vehicle.total_distance()
        return total_distance

class Algorithme:
    def __init__(self, clients, capacity, nb_vehicles):
        self.clients = clients
        self.capacity = capacity
        self.nb_vehicles = nb_vehicles

    def initial_solution(self):
        vehicles = []
        clients_copy = self.clients.copy()
        rd.shuffle(clients_copy)
        for i in range(self.nb_vehicles):
            vehicle = Vehicle(self.capacity)
            vehicle.add_client(self.clients[0])  # Ajouter le dépôt au début de chaque itinéraire
            vehicles.append(vehicle)
        i = 1
        for client in clients_copy:
            vehicles[i % self.nb_vehicles].add_client(client)
            i += 1
        return Solution(self.clients, vehicles)

    def run(self, max_iterations):
        best_solution = self.initial_solution()
        current_solution = best_solution
        for i in range(max_iterations):
            # Implémentez votre logique d'algorithme ici
            pass
        return best_solution

# Exemple d'utilisation des classes
nb_client = 21
demandes_clients = np.random.randint(1, 20, size=nb_client)
coordonnees_clients = np.random.rand(nb_client, 2)

clients = [Client(i, demandes_clients[i], coordonnees_clients[i][0], coordonnees_clients[i][1]) for i in range(nb_client)]

algorithm = Algorithme(clients, capacity=100, nb_vehicles=3)
best_solution = algorithm.run(max_iterations=1000)
print("Meilleure solution trouvée:", best_solution.evaluate())
"""import numpy as np
import random as rd
import matplotlib.pyplot as plt
#donnée du problème choisi de manière aléatroire : à terme les changer par les données du data-set
nb_client = 20 #nombre de client
demandes_clients = np.random.randint(1, 20, size=nb_client) #demande des clients i.e les points à visiter : ici aléatoire
#print(demandes_clients)
coordonnees_clients = np.random.rand(nb_client, 2)  # Coordonnées géographique des clients (x, y) : ici aléatoire
coordonnees_depot = [0.5,0.5]
x,y= [coordonnees_depot[0]],[coordonnees_depot[1]]
for k in range(nb_client):
    x.append(coordonnees_clients[k][0])
    y.append(coordonnees_clients[k][1])
plt.scatter(x,y)
plt.scatter([coordonnees_depot[0]],[coordonnees_depot[1]], c = "red", s = 100)

distance_entre_clients = np.zeros([nb_client+1,nb_client+1])
for i in range(nb_client):
    for j in range(i,nb_client):
        if i==0 and j!=0:
            d = np.sqrt((coordonnees_depot[0]-coordonnees_clients[j][0])**2+(coordonnees_depot[1]-coordonnees_clients[j][1])**2)
            distance_entre_clients[0,j],distance_entre_clients[j,0] = d,d

        d = np.sqrt((coordonnees_clients[i][0]-coordonnees_clients[j][0])**2+(coordonnees_clients[i][1]-coordonnees_clients[j][1])**2)
        distance_entre_clients[i+1,j+1],distance_entre_clients[j+1,i+1] = d,d

def eval_sol(solution):
    distance = 0
    n = len(solution)
    for k in range(n-1):
        distance = distance + distance_entre_clients[solution[k]][solution[k + 1]] #incrémentation de la distance parcourut
    return distance   

def trace_sol(solution, color = "lightblue"):
    tx,ty = [],[]
    for c in solution:
        tx.append(x[c])
        ty.append(y[c])
    plt.plot(tx,ty,c = color)

def ensemble_mouvement(solution, Tabou):
    E = []
    n = len(solution) - 1
    val = eval_sol(solution)
    indices = np.arange(1, n)
    np.random.shuffle(indices)
    for i in range(1, n):
        for j in range(i + 1, n):
            if [i, j, val] not in Tabou and [j, i, val] not in Tabou:
                E.append([i, j, val])
    return E

def diversification(solution, nb_aleatoire):
    n = len(solution) - 1
    for _ in range(nb_aleatoire):
        i, j = rd.sample(range(1, n), 2)  # Sélection aléatoire de deux indices distincts
        solution[i], solution[j] = solution[j], solution[i]  # Permutation aléatoire de deux clients
    return solution

def applique_mouvement(solution, mouvmement):
    nouvelle_solution = solution.copy()
    i = mouvmement[0]
    j = mouvmement[1]
    nouvelle_solution[i], nouvelle_solution[j] = nouvelle_solution[j], nouvelle_solution[i] #permute les 2 elements
    return nouvelle_solution

def best_mouvement(solution,E):
    s = applique_mouvement(solution.copy(),E[0])
    best = E[0]
    min = eval_sol(s)
    for mv in E:
        s = applique_mouvement(solution,mv)
        if eval_sol(s)<min:
            best = mv
            min = eval_sol(s)
    return best

def pop_worst_mouvemnt(Tabou,epsi = 3):
    if not Tabou:
        return
    val = Tabou[0][2]
    i = len(Tabou) - 1  # Commencer par la fin de la liste
    while i >= 0:
        if Tabou[i][0] - epsi > val:
            Tabou.pop(i)
        i -= 1

def stagnation_detectee(Tabou, seuil_stagnation):
    # Vérifier si la meilleure solution n'a pas été mise à jour depuis un certain nombre d'itérations
    if len(Tabou) < 2:
        return False  # Pas de stagnation si la liste Tabou est trop courte
    derniere_meilleure_solution = Tabou[0][2]  # Évaluation de la dernière meilleure solution
    nb_iter = 0
    for mouvement in reversed(Tabou[1:]):  # Parcourir les mouvements dans l'ordre inverse
        if mouvement[2] == derniere_meilleure_solution:
            nb_iter += 1
        else:
            break
    return nb_iter >= seuil_stagnation

def gestion_tabou(Tabou, taille_max, nb_iter, seuil_stagnation,epsi):
    if len(Tabou) > taille_max:
        pop_worst_mouvemnt(Tabou,epsi)
    if nb_iter % seuil_stagnation == 0:
        # Vérifier si l'algorithme stagne en observant l'évolution des valeurs dans la liste Tabou
        if stagnation_detectee(Tabou,seuil_stagnation):
            # Si une stagnation est détectée, faire de la place dans la liste Tabou
            pop_worst_mouvemnt(Tabou,epsi)

s = [0] + list(np.random.permutation(range(1, nb_client + 1))) + [0]
s_etoile = s.copy()
nbiter = 0
T = []
meil_iter = 0
inf = 0
nb_max = 1000
L_d = []


while eval_sol(s) > inf and (nbiter - meil_iter < nb_max):
    nbiter += 1
    E = ensemble_mouvement(s, T)

    # Ajout d'une phase d'exploration aléatoire
    if nbiter % 30 == 0:
        s = diversification(s, 4)  # Explorer 4 mouvements aléatoires toutes les 30 operations

    best_mv = best_mouvement(s, E)
    s = applique_mouvement(s, best_mv)
    val = eval_sol(s)

    T.append(best_mv)
    gestion_tabou(T,1000,nbiter,3,2)


    L_d.append(val)
    if eval_sol(s) < eval_sol(s_etoile):
        s_etoile = s.copy()
        meil_iter = nbiter


print("La solution finale est :", s_etoile, "évaluée à :", eval_sol(s_etoile))
trace_sol(s_etoile)
plt.figure()
plt.plot(L_d)
plt.show()





#version précédente
import numpy as np
import random as rd
import matplotlib.pyplot as plt



#donnée du problème choisi de manière aléatroire : à terme les changer par les données du data-set

nb_client = 30 #nombre de client
demandes_clients = np.random.randint(1, 20, size=nb_client) #demande des clients i.e les points à visiter : ici aléatoire
coordonnees_clients = np.random.rand(nb_client, 2)  # Coordonnées géographique des clients (x, y) : ici aléatoire
coordonnees_depot = [0.5,0.5]
x,y= [coordonnees_depot[0]],[coordonnees_depot[1]]
for k in range(nb_client):
    x.append(coordonnees_clients[k][0])
    y.append(coordonnees_clients[k][1])
plt.scatter(x,y)
plt.scatter([coordonnees_depot[0]],[coordonnees_depot[1]], c = "red", s = 100)

distance_entre_clients = np.zeros([nb_client+1,nb_client+1])
for i in range(nb_client):
    for j in range(i,nb_client):
        if i==0 and j!=0:
            d = np.sqrt((coordonnees_depot[0]-coordonnees_clients[j][0])**2+(coordonnees_depot[1]-coordonnees_clients[j][1])**2)
            distance_entre_clients[0,j],distance_entre_clients[j,0] = d,d

        d = np.sqrt((coordonnees_clients[i][0]-coordonnees_clients[j][0])**2+(coordonnees_clients[i][1]-coordonnees_clients[j][1])**2)
        distance_entre_clients[i+1,j+1],distance_entre_clients[j+1,i+1] = d,d






#definition des fonctions
        
def eval_sol(solution):
    distance = 0
    n = len(solution)
    for k in range(n-1):
        distance = distance + distance_entre_clients[solution[k]][solution[k + 1]] #incrémentation de la distance parcourut
    return distance   

def trace_sol(solution, color = "lightblue"):
    tx,ty = [],[]
    for c in solution:
        tx.append(x[c])
        ty.append(y[c])
    plt.plot(tx,ty,c = color)

def ensemble_mouvement(solution, Tabou): #on considère un mouvement élémentaire comme la perumation de SEULEMENT 2 elements (2 parmis n mouvment possible)
    E = []
    n = len(solution)-1
    val = eval_sol(solution)
    for i in range(1,n):
        for j in range(i+1,n):
            if [i,j,val] not in Tabou and [j,i,val] not in Tabou: #on considère uniquement les mouvements qui ne sont pas dans la liste Tabou
                E.append([i,j,val])
    return E

def applique_mouvement(solution, mouvmement):
    nouvelle_solution = solution.copy()
    i = mouvmement[0]
    j = mouvmement[1]
    nouvelle_solution[i], nouvelle_solution[j] = nouvelle_solution[j], nouvelle_solution[i] #permute les 2 elements
    return nouvelle_solution

def rand_mouvement(E):
   return rd.choice(E)


def best_mouvement(solution,E):
    s = applique_mouvement(solution.copy(),E[0])
    best = E[0]
    min = eval_sol(s)
    for mv in E:
        s = applique_mouvement(solution,mv)
        if eval_sol(s)<min:
            best = mv
            min = eval_sol(s)
    return best

def pop_worst_mouvemnt(Tabou): #fait office de fonction d'aspiration
    if len(Tabou) == 0:
        pass
    n= len(Tabou)
    epsi = 3 #"tolerance" de la fonction d'apiration
    val = Tabou[0][2] #evaluation de la solution si le mouvement  avait été apliqué
 
    for k in range(n):
        if Tabou[k][0]-epsi>val:
            val = Tabou[k][2] #disuctable
            Tabou.pop(k)
            n = len(Tabou)



def option(solution,E):
    val = eval_sol(solution)
    epsi = 0.2
    omega = []
    for mv in E:
        s = solution.copy()
        if eval_sol(applique_mouvement(s,mv))+epsi>val:
            omega.append(mv)
    return omega


s = [0] +list(np.random.permutation(range(1, nb_client+1))) + [0]

s_etoile = s.copy()
nbiter = 0 #compteur d'iteration
T = [] #liste tabou 
meil_iter = 0 # (itération ayant conduit à la meilleure solution current_solution trouvée jusque-là)
inf = 0 #constante a definir (borne inferieur)
nb_max = 600 #idem (limite d'operation)

L_d = []
best_s = []

while eval_sol(s)> inf and (nbiter - meil_iter< nb_max):

    nbiter = nbiter +1
    E = ensemble_mouvement(s, T)

    best_mv = best_mouvement(s,E)
    #print(best_mv)
    s = applique_mouvement(s,best_mv)
    val = eval_sol(s)

    T.append(best_mv)

    if len(E)<0.5*nb_client: #pseudo fonction d'aspiration : si il y a moin de 500 mouvement disponible on libère des mouvment de la liste tabou
        T = pop_worst_mouvemnt(T)
    L_d.append(val)

    if eval_sol(s)< eval_sol(s_etoile):
        s_etoile = s.copy()
        meil_iter = nbiter
        best_s.append(s_etoile)

print("la solution final est:",s_etoile, "evaluée à :", eval_sol(s_etoile))
trace_sol(s_etoile)
plt.figure()
plt.plot(L_d)
plt.show()
"""

