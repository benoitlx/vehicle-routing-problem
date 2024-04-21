from utils import *
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

#########################################################################################################
def inter_distance(s,clients): 
    """calcule la distance realtive entre les different clients : distibution du cout dans séquence"""
    d_t = 0
    L_relatif = []
    for k in range(len(s)-1):
        d_t = d_t+distance_squared(clients[s[k]],clients[s[k+1]])

    for k in range(len(s)-1):
        d = distance_squared(clients[s[k]],clients[s[k+1]])
        L_relatif.append(d/d_t)
    return L_relatif


def find_cluster(s,epsi,clients):
    """Localise les points relativement proche (a un epsilon donné)"""
    L_distance = inter_distance(s,clients)
    n = len(L_distance)
    cluster = []
    c = 0
    while c<n-1:
        segement = []
        k = c
        while k<n and L_distance[k]<epsi  :
            segement.append(k)
            k = k+1
        segement.append(k)
        if len(segement)>1:
            cluster.append(segement)
        c = k+1
    return cluster

def barycentre(s,segement,clients):
    """calcule le barycentre d'une suite de points"""
    n = len(segement)
    g_lon = 0
    g_lat = 0
    for k in range(n):
        g_lat = g_lat +clients[segement[k]][0]
        g_lon = g_lon +clients[segement[k]][1]
    return [g_lat/n,g_lon/n]

def neer_from_cluster(s,one_cluster,clients):
    """Trouve le point le plus proche du barycentre d'un segment"""
    n = len(s)
    s_cluster = [i for i in one_cluster]
    G = barycentre(s,one_cluster,clients)
    d_min = distance_squared(clients[s[0]],G)
    indice_min =0
    for k in range(n):
        if s[k] not in s_cluster:
            d = distance_squared(clients[s[k]],G)
            if d<d_min:
                d_min = d
                indice_min = k
    return indice_min

def shift_cluster(s,one_cluster,clients):
    """deplace une sous partie de la solution au meilleur endroit"""
    restriced_s = [c for c in s if c not in one_cluster]
    if len(restriced_s)<2:
        return s
    G = barycentre(s,one_cluster,clients)
    indice_insertion = neer_from_cluster(restriced_s,one_cluster,clients)
    g = restriced_s[:indice_insertion]
    d = restriced_s[indice_insertion:]
    n_s = g + one_cluster + d
    if n_s[-1]!=0:
        n_s.append(0)
    if s[0]!=0:
        s.insert(0,0)
    return n_s

def shift_all_cluster(s,epsi,clients):
    """deplace tout les sous parties d'une solution"""
    cluster_cycle = liste_cluster(s,epsi,clients)
    for k in range(len(cluster_cycle)):
        s = shift_cluster(s.copy(),cluster_cycle[k],clients)
    if s[-1]!=0:
        s.append(0)
    if s[0]!=0:
        s.insert(0,0)
    return s

def liste_cluster(s,epsi,clients):
    """localise tout les clusters"""
    L_cluster = find_cluster(s,epsi,clients)
    cluster_cycle = []
    for k in range(len(L_cluster)):
        s_cluster = [s[i] for i in L_cluster[k]]
        cluster_cycle.append(s_cluster)
    return cluster_cycle

def find_outlier_point(s,epsi,clients):
    """localise les points aberent"""
    L_distance = inter_distance(s,clients)
    n = len(L_distance)
    L_outlier = []
    c = 0
    while c<n:
        segement = []
        k = c
        while k<n-1 and L_distance[k]>epsi:
            segement.append(k)
            k = k+1
        if len(segement)>1:
            segement.pop(0)
            L_outlier.append(segement)
        c = k+1
    return L_outlier

def liste_outlier(s,epsi,clients):
    """localise tous les points aberent"""
    L_outlier = find_outlier_point(s,epsi,clients)
    outlier_cycle = []
    for k in range(len(L_outlier)):
        s_outlier = [s[i] for i in L_outlier[k]]
        outlier_cycle.append(s_outlier)
    return outlier_cycle

def shift_outlier(s,one_outlier,clients):
    """deplace un point aberent au meilleur endroit"""
    restriced_s = [c for c in s if c not in one_outlier]
    if len(restriced_s)<2:
        return s
    n_s = s.copy()
    for k in range(len(one_outlier)):
        G = barycentre(n_s,one_outlier[k],clients)
        indice_insertion = neer_from_cluster(restriced_s,one_outlier,clients)
        g = restriced_s[:indice_insertion]
        d = restriced_s[indice_insertion:]
        n_s = g + one_outlier + d
        if n_s[-1]!=0:
            n_s.append(0)
    return n_s

def shift_all_outlier(s,epsi,clients):
    """deplace tous les point aberents"""
    outlier_cycle = liste_outlier(s,epsi,clients)
    for k in range(len(outlier_cycle)):
        s = shift_cluster(s.copy(),outlier_cycle[k],clients)
    if s[-1]!=0:
        s.append(0)
    return s