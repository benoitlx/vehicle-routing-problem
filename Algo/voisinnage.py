import random
import copy

def intra_route_swap(L1):
    """échange d'un client
    avec un autre client dans la même
    route"""
    L = copy.deepcopy(L1)
    i = random.randint(0, len(L)-1)
    j = random.randint(1, len(L[i])-2)
    k = random.randint(1, len(L[i])-2)
    L[i][j], L[i][k] = L[i][k], L[i][j]
    return L

def inter_route_swap(L1):
    """ fonction de voisinage
    qui effectue le déplacement d'échange
    d'un client d’une route avec un client
    d’une autre route"""
    L = copy.deepcopy(L1)
    i, j = random.randint(0, len(L)-1), random.randint(0, len(L)-1)
    k, l = random.randint(1, len(L[i])-2), random.randint(1, len(L[j])-2)
    L[i][k], L[j][l] = L[j][l], L[i][k]
    return L

def intra_route_shift(L1):
    """fonction de voisinage qui effectue
    le déplacement d'un client vers une autre position sur la
    même route"""
    L = copy.deepcopy(L1)
    i = random.randint(0, len(L)-1)
    j = random.randint(1, len(L[i])-2)
    x = L[i].pop(j)
    k = random.randint(1, len(L[i])-2)
    L[i] = L[i][:k] + [x] + L[i][k:]
    return L

def inter_route_shift(L1):
    """ fonction de voisinage qui effectue
    le déplacement d'un client d’une route à une autre"""
    L = copy.deepcopy(L1)
    i, j = random.randint(0, len(L)-1), random.randint(0, len(L)-1)
    k, l = random.randint(1, len(L[i])-2), random.randint(1, len(L[j])-2)
    x = L[i].pop(k)
    if len(L[i]) == 2:
        L.pop(i)
    L[j] = L[j][:l] + [x] + L[j][l:]
    return L

def two_intra_route_swap(L1):
    """fonction de voisinage qui
    consiste en l'échange de clients sur la même route, ainsi
    que la fonction de voisinage d'échange intra-route.
    Cependant, dans la fonction Two Intra-Route Swap,
    deux clients consécutifs sont échangés avec deux autres
    clients consécutifs de la même route"""
    L = copy.deepcopy(L1)
    L_index = [i for i in range(len(L)) if len(L[i]) >= 6]
    i = random.choice(L_index)
    k = random.randint(1, len(L[i])-3)
    L_index_2 = [j for j in range(1, len(L[i]) - 1) if (j != k and j != k+1)]
    l = random.choice(L_index_2)
    L[i][k], L[i][k+1], L[i][l], L[i][l+1] = L[i][l], L[i][l+1], L[i][k], L[i][k+1]
    return L

def two_intra_route_shift(L1):
    """Two Intra-Route Shift: fonction de voisinage
    qui consiste en la relocalisation des clients sur la
    même route, ainsi que la fonction de voisinage
    de shift intra-route. Cependant, dans la fonction
    Two Intra-Route Shift, deux clients consécutifs
    sont retirés de leur position et réinsérés dans
    une autre position de la même route"""
    L = copy.deepcopy(L1)
    L_index = [i for i in range(len(L)) if len(L[i]) >= 5]
    i = random.choice(L_index)
    j = random.randint(1, len(L[i])-3)
    x, y = L[i].pop(j), L[i].pop(j)
    k = random.randint(1, len(L[i])-2)
    L[i] = L[i][:k] + [x, y] + L[i][k:]
    return L  

def elimine_petite_route(L1):
    """ fonction de
    voisinage qui cherche à éliminer la plus petite
    route de la solution"""
    L = copy.deepcopy(L1)
    min, indice_min = len(L[0]), 0
    if len(L) != 1:
        for i in range(1, len(L)):
            if len(L[i]) < min:
                min, indice_min = len(L[i]), i
    X = L.pop(indice_min)
    for x in X[1:min-1]:
        j = random.randint(0, len(L)-1)
        l = random.randint(1, len(L[j])-2)
        L[j] = L[j][:l] + [x] + L[j][l:]
    return L

def elimine_route(L1):
    """Élimine une route aléatoire: la fonction de
    voisinage Élimine la route aléatoire, fonctionne
    de la même manière que la fonction Élimine la
    route la plus petite, mais la route à supprimer est
    choisi au hasard"""
    L = copy.deepcopy(L1)
    i = random.randint(0, len(L)-1)
    X = L.pop(i)
    for x in X[1:len(X)-1]:
        j = random.randint(0, len(L)-1)
        l = random.randint(1, len(L[j])-2)
        L[j] = L[j][:l] + [x] + L[j][l:]
    return L

#L1 = [[0, 1, 2, 3, 4, 5, 6, 7, 0], [0, 1, 2, 3, 0], [0, 1, 2, 3, 4, 5, 0]]
#print(elimine_petite_route(L1))