from Mouvement import *
from utils import *
from Renforcement import *

def applique_mouvement(solution, mouvmement):
    nouvelle_solution = solution.copy()
    i = mouvmement[0]
    j = mouvmement[1]
    nouvelle_solution[i], nouvelle_solution[j] = nouvelle_solution[j], nouvelle_solution[i] 
    return nouvelle_solution

def best_solution(V,A):
    """revoie la meilleur solution d'un voisinage"""
    n = len(V)
    eval_min = A
    indice_sol =0
    for k in range(n-1):
        val = cout(V[k][0],clients)
        if val<eval_min:
            eval_min = val
            indice_sol = k
    return V[indice_sol]

def MAJ_tabou(T, max_tab):
    """gestion de la liste tabou"""
    n = len(T)
    val = T[0][-1]
    mv = T[-1]
    if n>max_tab:
        pop_worst_mouvement(T)
    return T

def pop_worst_mouvement(Tabou):
    """suppresion d'un nombre aléatoire des plus mauvais mouvement de la liste tabou"""
    if not Tabou:
        return
    a = rd.randint(0,len(Tabou)//2-1)
    val = Tabou[a][-1]
    i = rd.randint(1,len(Tabou) - 1)
    while i >= 0:
        a = rd.randint(0,len(Tabou)-1)
        Tabou.pop(a)
        i -= 1
    
def cut_sol(solution):
    L = []
    n = len(solution)
    a= 0
    for k in range(1,n):
        if solution[k]==0:
            L.append(solution[a:k] + [0])
            a = k
    return L

def capacity(s,C):
    """ajoute des retour au depot ie des vehicule si la capacité de ceux ci n'est pas sufisante pour traiter la route générer
    NB :la capacité est ici homogène a une nombre de clients
    """
    n = len(s)
    a=0
    for k in range(1,n-2):
        if s[k]==0:
            a =k+2
            if s[k+1]==0:
                s.pop(k)

        if k-a>C:
            s.insert(k,0)
            a =k+2
    if s[0]!=0:
        s.insert(0,0)

def perform_action(s, action):
    action = action +1
    mvt = mouvement()
    sol = s.copy()
    mv = None
    Indice_zero = mvt.find_zero(s)
    #print(action)
    while mv is None:
        if action == 1:
            # Intra-Route Swap
            sol, mv = mvt.Intra_Route_Swap(sol,Indice_zero)
        elif action == 2:
            # Inter-Route Swap
            sol, mv = mvt.Inter_Route_Swap(sol,Indice_zero)
        elif action == 3:
            # Intra-Route Shift
            sol, mv = mvt.Intra_Route_Shift(sol,Indice_zero)
        elif action == 4:
            # Inter-Route Shift
            sol, mv = mvt.Inter_Route_Shift(sol,Indice_zero)
        elif action == 5:
            # Two Intra-Route Swap
            sol, mv = mvt.Two_Intra_Route_Swap(sol,Indice_zero)
        elif action == 6:
            # Two Intra-Route Shift
            sol, mv = mvt.Two_Intra_Route_Shift(sol,Indice_zero)
        elif action == 7:
            # Pop Small Route
            sol, mv = mvt.pop_small_route(sol,Indice_zero)
        elif action == 8:
            # Pop Random Route
            sol, mv = mvt.pop_random_route(sol,Indice_zero)
        else:
            raise ValueError("Invalid action")

    return sol, mv


def gen_vois(s,taille_vois,Tabou,max_tab):
    
    mvt = mouvement()
    eval = cout(s,clients)
    c = 0
    b =0
    V = []
    state = q_agent.previous_state
    while c<taille_vois:
        action = q_agent.e_greedy(state)
        #print(action)
        new_sol, mv = perform_action(s, action)
        while mv ==[]:
            action = q_agent.e_greedy(state)
            #print(action)
            new_sol, mv = perform_action(s, action)
        mv.append(eval)
        #capacity(new_sol,60)
        #new_eval = cout(new_sol, clients)
        #reward = q_agent.reward(new_eval, eval)
        #q_agent.update_q_table(state, action, reward, mv[0]-1)
        #q_agent.previous_state = mv[0]-1
        if mv not in Tabou and new_sol not in V:
            V.append((new_sol,mv))
            c = c+1
        else:
            b =b+1
            if b>100:
                Tabou.pop(0)
                b=b-1
    return V

q_agent = QLearningAgent()

def TB_RL(b_s,nb_iter_max, max_tabou, taille_vois,Capacite=1000):
    global demande_client
    global clients
    meilleur_cout = []
    current_cout = []
    s = [0]
    for r in b_s:
        s = s+r+[0]
    capacity(s,Capacite)
    s_etoile = s.copy()
    A = cout(s_etoile,clients)
    cout_solution = A
    meilleur_cout.append(A)
    nbiter = 0
    T = []
    meil_iter = 0
    inf = 0
    print(s_etoile)
    while cout_solution > inf and (nbiter - meil_iter < nb_iter_max):
        nbiter += 1
        V = gen_vois(s.copy(),taille_vois,T,max_tabou)
        s_prim,mv = best_solution(V,A)
        A = mv[-1]
        T.append(mv)
        T = MAJ_tabou(T, max_tabou)
        
        current_cout.append(A)
        s = s_prim.copy()
        capacity(s,Capacite)
        
        cout_solution = cout(s,clients)
        if cout_solution<cout(s_etoile,clients):
            s_etoile = s.copy()
            #print(s_etoile)
            reward = q_agent.reward(cout_solution, meilleur_cout[-1])
            q_agent.update_q_table(q_agent.previous_state-1,  mv[0]-1, reward, mv[0]-1)
            q_agent.previous_state = mv[0]-1
            np.set_printoptions(linewidth=np.inf)
            print(q_agent.q_table)
            print("\n")
            meilleur_cout.append(cout_solution)
            meil_iter = nbiter
       
 
    S = cut_sol(s_etoile)
    plt.figure()
    plt.plot(current_cout)
    plt.figure()
    plt.plot(meilleur_cout, c = 'red')
    plt.figure()

    return (cout(s_etoile,clients), S)