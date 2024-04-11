
import numpy as np
import random as rd
import matplotlib.pyplot as plt
from utils import *


"""
fonctionne uniquement avec des solutions de la forme : [0, 26, 42, 90, 4, 91, 46, 0, 75, 67, 99, 7, 58, 15, 24, 18, 28, 88, 16, 0, 64, 50, 54, 0]
(une unique liste)

/!\ attention !!!
si vous avez une solution : [[0, 26, 42, 21, 69, 65, 84, 6, 0], [0, 39, 25, 58, 15, 24, 18, 28, 88, 16, 0]]
(liste de liste) il fautdra appliquer la fonction past_sol pour adopter le formalisme, la fonction cut_sol permet de revenir à une liste de litse

/!\ attention 2
les fonctions mouvement renvoie un tuple : la solution voisine et un mouvement


Pour le moment le choix de la fonction est uniforme,
jeux de test à la fin
"""


m = 20

def cut_sol(solution):
    """"permet de decouper une solution en plusieur route"""
    S = []
    n = len(solution)
    a= 0
    for k in range(1,n):
        if solution[k]==0:
            S.append(solution[a:k] + [0])
            a = k
    return S

def past_sol(solution):
    """permet de former à partire de route une solution"""
    s = []
    S = solution[1]
    for r in S:
        s = s +r
    return s

def applique_mouvement(solution, mouvmement):
    """"applique une permutation dans une route"""
    nouvelle_solution = solution.copy()
    i = mouvmement[0]
    j = mouvmement[1]
    nouvelle_solution[i], nouvelle_solution[j] = nouvelle_solution[j], nouvelle_solution[i] 
    return nouvelle_solution

class mouvement:
    def __init__(self):
        pass

    def find_zero(self,s):
        """"permet de localiser les 0 (retour au depot) dans une solution:
        utile pour identifer les differentes routes d'une solution"""
        I_0 = []
        for k in range(1,len(s)-1):
            if s[k]==0:
                I_0.append(k)
        return I_0
    
    def Intra_Route_Swap(self,s,Indice_0): 
        """
        1. Intra-Route Swap: échange d'un client avec un autre client dans la même route (les clients 4 et 6 de la route 2 sont échangés)
        Principe : on recherche une route de plus de 3 clients, en séléctione deux clients parmis celle ci et on les permutes
        """
        n = len(s)
        I = Indice_0.copy()
        n_s = s.copy()
        I = [0] + I + [n-1] #on considère tout les 0 y compris le 1er et le dernier
        c = 0
        if len(I)<3:
            return (s,[])

        i = rd.randint(0,len(I)-2)
        a,b = I[i],I[i+1]
        while abs(a-b)<3 and c<m: #recherche aléatoire d'indice compatible (m itération de recherche max)
            i = rd.randint(0,len(I)-2)
            a,b = I[i],I[i+1]
            c = c+1
 
        if abs(b-a)<3: 
            return (n_s, []) #cas ou aucun indice compatible n'est trouvé après les 10 iteration
        
        c,d = rd.randint(a+1,b-1),rd.randint(a+1,b-1) #selection de 2 clients
        n_s = applique_mouvement(n_s,[c,d])#permutation
        return (n_s,[1,c,d])
        
    def Inter_Route_Swap(self,s,Indice_0):
        """"
        2. Inter-Route Swap: fonction de voisinage qui effectue le déplacement d'échange d'un client d’une route avec un client d’une autre route.
        Principe : selection d'un pivot compatible (plus de deux client) puis selection de deux client l'un intervenant avant le pivot l'autre après,
        pas nécessairement dans le route du pivot choisit 
        +interdiction de modifier la taille de la route
        """
        #print("Inter_Route_Swap")
        n = len(s)
        if not Indice_0:
            return (s, [])
        n_s = s.copy()
        c =0
        pivot = rd.choice(Indice_0)
        while (pivot<2 or abs(n-pivot)<2) and c<m: #recherche d'un pivot compatible (m iteration max)
            pivot = rd.choice(Indice_0) #choix d'un pivot aléatoire
            c = c+1
        if pivot<2 or (n-pivot)<3:
            return (n_s,[])
        a = rd.randint(1,pivot-1)
        b = rd.randint(pivot+1,n-2)
        c =0
        while (s[a]==0 or s[b]==0) and c<m: #choix de deux clients dans une route précedante et suivante
            a = rd.randint(1,pivot-1)
            b = rd.randint(pivot+1,len(s)-1)
            c =c+1
  
        n_s = applique_mouvement(n_s,[a,b]) #permutation des deux clients
        return (n_s,[2,a,b])
    
    def Intra_Route_Shift(self,s, Indice_0):
        """
        3. Intra-Route Shift: fonction de voisinage qui effectue le déplacement d'un client vers une autre position sur la même route.
        """
        #print("Intra_Route_Shift")
        if not Indice_0:
            a,b = 0,len(s)
        else: #choix d'une route (segment de la solution)
            I = [0] + Indice_0.copy() +[len(s)]
            i = rd.randint(0,len(I)-2)
            a,b = I[i],I[i+1]
        if abs(a-b)<4:
            return (s,[])
        gauche = s[:a+1] #segement gauche la solution
        droite = s[b:] #segment droit de la solution
        route = s[a+1:b] #route choisit
        i_client = rd.randint(1, len(route) - 2) #choix d'un client dans cette route
        client = route.pop(i_client) #supresion du client dans cette route
        i_insert = rd.randint(0, len(route)-1) #insertion a une nouvelle position
        new_route = route[:i_insert] + [client] + route[i_insert:] 
        n_s = gauche + new_route + droite #concaténation des 3 segment pour reformer la solution
        return (n_s,[3,-i_client,-i_insert])

    
    def Inter_Route_Shift(self,s,Indice_0):
        """
        4. Inter-Route Shift: fonction de voisinage qui effectue le déplacement d'un client d’une route à une autre.
        Principe : on choisi un retour au depot qui sert de pivot, on choisi un client qui est visiter avant et un après, puis on les échanges

        """
        #print("Inter_Route_Shift")
        n_s = s.copy()
        n = len(s)
        if not Indice_0:
            return (n_s,[])

        c= rd.randint(0,len(Indice_0)-1)
        pivot = Indice_0[c] #choisi un zero aléatroire dans la liste des retour au depot intermédiaire
        
        a,b = rd.randint(0,pivot),rd.randint(pivot+1,n-1)
        d = n - pivot #pour choisir le plus long segment de la route (soit gauche soit droit)
        if d>pivot:
            n_s = applique_mouvement(n_s,[pivot,b])
            return (n_s,[4,pivot,b])
        else:
            n_s = applique_mouvement(n_s,[a, pivot])
            return (n_s,[4,a,pivot])

    
    def Two_Intra_Route_Swap(self,s,I):
        """5. Two Intra-Route Swap: fonction de voisinage qui consiste en l'échange de clients sur la même route,
        #ainsi que la fonction de voisinage d'échange intra-route. Cependant, dans la fonction Two Intra-Route Swap, 
        #deux clients consécutifs sont échangés avec deux autres clients consécutifs de la même route;"""
        n_s = s.copy()
        n = len(s)
        if not I:
            a,b = 0,len(s)
            i_1 = rd.randint(a+1, b-2)  
            i_2 = rd.randint(a+1, b-2)
            if abs(i_1-i_2)<3 or abs(i_1-len(s))<3 or abs(i_2-len(s))<3 :
                return n_s,[]
            n_s[i_1], n_s[i_1+1], n_s[i_2], n_s[i_2+1] = n_s[i_2], n_s[i_2+1],n_s[i_1], n_s[i_1+1]
            return n_s,[5,i_1,i_2]

        Indice_0 =[0]+I+[len(s)]
        i_zero = rd.randint(0,len(Indice_0)-2)
        a,b = Indice_0[i_zero], Indice_0[i_zero+1]
        i_1 = rd.randint(a, b)  
        i_2 = rd.randint(a, b)
        if abs(i_1-i_2)<3 or abs(i_1-len(s))<3 or abs(i_2-len(s))<3 :
                return n_s,[]

        n_s[i_1], n_s[i_1+1], n_s[i_2], n_s[i_2+1] = n_s[i_2], n_s[i_2+1],n_s[i_1], n_s[i_1+1]
        return n_s,[5,i_1,i_2]
    
    def Two_Intra_Route_Shift(self, s, I):
        """6. Two Intra-Route Shift: fonction de voisinage qui consiste en la relocalisation des clients sur la même route, ainsi que la fonction de voisinage
        de shift intra-route. Cependant, dans la fonction Two Intra-Route Shift, deux clients consécutifs sont retirés de leur position et réinsérés dans
        une autre position de la même route"""
        n_s = s.copy()
        n = len(s)
        if not I:
            a, b = 0, len(s)
            i_1 = rd.randint(a + 1, b - 2)  
            i_2 = rd.randint(a + 1, b - 2)
            if abs(i_1 - i_2) < 3 or abs(i_1 - len(s)) < 3 or abs(i_2 - len(s)) < 3 :
                return n_s, []
            n_s[i_1], n_s[i_1 + 1], n_s[i_2], n_s[i_2 + 1] = n_s[i_2], n_s[i_2 + 1], n_s[i_1], n_s[i_1 + 1]
            return n_s, [6,-i_1, -i_2]

        Indice_0 = [0] + I + [len(s)]
        i_zero = rd.randint(0, len(Indice_0) - 2)
        a, b = Indice_0[i_zero], Indice_0[i_zero + 1]
        i_1 = rd.randint(a, b)  
        i_2 = rd.randint(a, b)
        if abs(i_1 - i_2) < 4 or abs(i_1 - len(s)) < 4 or abs(i_2 - len(s)) < 4 :
            return n_s, []

        n_s[i_1], n_s[i_1 + 1], n_s[i_2], n_s[i_2 + 1] = n_s[i_2], n_s[i_2 + 1], n_s[i_1], n_s[i_1 + 1]
        return n_s, [6,-i_1, -i_2]
        #return (n_s,[])

    def pop_small_route(self,s, Indice_0):
        """
        7. Élimine la plus petite route: fonction de voisinage qui cherche à éliminer la plus petite route de la solution.
        Principe : trouver les 2 zeros les plus proche, en enlever 1
        Conséquance : un retour au depot est retirer (un vehicule) l'un des vehicule se retouve en charge de client du précédant
        
        """
        #print("pop_small_route")
        if not Indice_0:
            return (s,[])
        n_s = s.copy()
        n =len(Indice_0) 
        etape_min = len(s)
        indice = 0
        for k in range(n-1):
            d =Indice_0[k+1]- Indice_0[k]
            if d<etape_min:
                etape_min = d
                indice = k
        n_s.pop(Indice_0[indice])
        return (n_s,[7,Indice_0[indice]])

    
    def pop_random_route(self,s,Indice_0):
        """
        8. Élimine une route aléatoire: la fonction de voisinage Élimine la route aléatoire, 
        fonctionne de la même manière que la fonction Élimine la route la plus petite, mais la route à supprimer est choisi au hasard
        """
        #print("pop_random_route")
        if not Indice_0:
            return s,[]
        n_s = s.copy()
        zero = rd.choice(Indice_0)
        n_s.pop(zero)
        Indice_0 = self.find_zero(n_s)
        return n_s,[8,zero]
    

    def Action(self,s):
        a = rd.randint(1,8) #choix d'une action aléatoire
        
        Indice_0 = self.find_zero(s)
        if a ==1:
            #print("Intra_Route_Swap")
            return self.Intra_Route_Swap(s,Indice_0)
        if a==2:
            #print("Inter_Route_Swap")
            return self.Inter_Route_Swap(s,Indice_0)
        if a ==3:
            #print("Intra_Route_Shift")
            return self.Intra_Route_Shift(s,Indice_0)
        if a ==4:
           # print("Inter_Route_Shift")
            return self.Inter_Route_Shift(s,Indice_0)
        if a ==5:
            #print("Two_Intra_Route_Swap")
            return self.Two_Intra_Route_Swap(s,Indice_0)
        if a ==6:
            #print("Two_Intra_Route_Shift")
            return self.Two_Intra_Route_Shift(s,Indice_0)
        if a ==7:
            #print("pop_small_route")
            return self.pop_small_route(s,Indice_0)
        if a ==8:
            #print("pop_random_route")
            return self.pop_random_route(s,Indice_0)
"""
mvt = mouvement()
s = [0, 26, 42, 90, 4, 91, 46, 17, 45, 63, 38, 2, 21, 69, 65, 84, 6, 0, 39, 25, 59, 76, 93, 75, 67, 99, 7, 58, 15, 24, 18, 28, 88, 16, 0, 64, 50, 54, 0]
#Indice_0 =mvt.find_zero()
print("avant",s)
s,mv = mvt.Action(s)
print("après",s)
"""

