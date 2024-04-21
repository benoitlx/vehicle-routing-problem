from Mouvement_classification import *
import numpy as np
import matplotlib.pyplot as plt
def recherche_classifier(S,nb_iter_max,clients,Capacite):
    s = []
    if S[0][0]!=0:
        s.append(0)
    for r in S:
        s = s+r + [0]
        if s[-1]!=0:
            s.append(0)

    s_etoile = s.copy()
    A = cout(s_etoile,clients)
    cout_solution = A
    meilleur_cout = []
    meilleur_cout.append(A)
    nbiter = 0
    meil_iter = 0
    inf = 0
    while cout_solution > inf and (nbiter - meil_iter < nb_iter_max):
        nbiter += 1
        s_prim = s.copy()
        A = cout(s,clients)

        if nbiter%2==0:
            L_realtif = inter_distance(s_prim,clients)
            a = 0.9*max(L_realtif)
            epsi = a + a*np.sin(0.7*nbiter/(2*np.pi))
            s_prim = shift_all_cluster(s_prim.copy(),epsi,clients) 
        else:
            b = 1/len(s_prim)
            epsi = b + b*np.sin(0.7*nbiter/(2*np.pi))
            s_prim = shift_all_outlier(s_prim.copy(),epsi,clients)
        s = s_prim.copy()
        cout_solution = cout(s,clients)
        if cout_solution<cout(s_etoile,clients):
            s_etoile = s.copy()
            meilleur_cout.append(cout_solution) 
            meil_iter = nbiter
    
    S = cut_sol(s_etoile)
    return (cout(s_etoile,clients), S)