#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:46:25 2019

@author: Touzari Liticia
@author : Djeddal Hanane
"""

import numpy as np
from random import *
import pulp



def constructionMatrice_Q(D):
    """
    Q(d,k) :la probabilité d'obtenir k points en jetant d dés sachant qu'aucun dé n'est tombé sur 1
    """
       
    Q=np.zeros([D+1,6*(D+1)])
    for k in range(2,7):#d=1
        Q[1][k]=1/5
    for d in range(1,D+1):
        Q[d][1]=0
        for k in range(2, 2*d):
            Q[d][k]=0
        for k in range(6*d+1,6*(D+1)):
            Q[d][k]=0
    for d in range(2,D+1):
        for k in range(2*d,6*d+1):
            for j in range(2,7):
                Q[d][k]+=Q[d-1][k-j]
            Q[d][k]=Q[d][k]/5
    return Q


def constructionMatrice_P(D):
    """
    P(d,k) :la probabilité qu'un joueur qui lance d dés obtienne k points
    """
    Q=constructionMatrice_Q(D)
    P=np.zeros([D+1,6*(D+1)])
    for d in range(1,D+1):
        P[d][1]=1-(5/6)**(d)
        for k in range(2, 2*d):
            P[d][k]=0
        for k in range(6*d+1,6*(D+1)):
            P[d][k]=0
        for k in range(2*d,6*d+1):
            P[d][k]=Q[d][k]*((5/6)**(d))
    return P


#================================== VARIANTE SEQUENTIELLE

def strategieAveugle(D):
    """
    Strategie Aveugle : retourne le d qui maximise l'esperance de points obtenus 
    EP(d)= (4*d-1)*((5/6)^(d+1))) +1
    """
    d_opt=0
    EGopt=0
    for d in range(D):
        EG=((4*(d+1)-1)*((5/6)**(d+1))) +1
        if(EGopt<EG):
            d_opt=d+1
            EGopt=EG
    return d_opt 
#=========================Programmationdynamique  


def constructionTableDynamique(N,D,P):

    """
    Table dynamique : retourne une table (N-1+6*D)x(N-1+6*D) des
    -esperances de gain
      tab[i,j] :l'espérance de gain du joueur 1 dans l'état (i, j) tq
      etat(i,j) :l'état où le premier joueur a cumulé i points, le deuxième joueur a cumulé j
      points, et c'est au joueur 1 de jouer
    -strategie : le nombre de dés à lancer dans l'état (i,j)
    """
    cap=N-1+6*D
    tab=np.zeros([cap+1,cap+1])
    strat=[[1]*(cap+1)]*(cap+1)  #une matrice qui, pour un etat i,j, retourne le numbre de dés à jouer
    for i in range (N,cap+1):
        for j in range (cap+1):
            if(i>j):
                tab[i][j]=1
            elif(i==j):
                tab[i][j]=0
            else:
                tab[i][j]=-1      
    for j in range (N,cap+1):
        for i in range (N):
            if(i>j):
                tab[i][j]=1
            elif(i==j):
                tab[i][j]=0
            else:
                tab[i][j]=-1      
    for i in range(N-1,-1,-1):
        for j in range(N-1,-1,-1):
            t=[0]*D
            for d in range(1,D+1):
                for k in range(1,6*d+1):
                    t[d-1]+=(P[d][k]*tab[j][i+k])
            strat[i][j]=t.index(min(t))+1
            tab[i][j]=-min(t)
    return tab,strat


def strategieOptimale(i,j,strat):
    """
    strategie Optimale : le nombre de dés à lancer dans l'état (i,j)
    """
    return int(strat[i][j])


def strategieAleatoire(D):
    """
    strategie aleatoire : un nombre aleatoire de dés à lancer.
    """
    return randint(1, D)


def simulation(N,D):
    """
        Simulation de 4 parties du jeu 
        [aveugle-aveugle, aveugle-optimale] [optimale-aveugle, optimale-optimale]
        retourne une matrice de gagnant dans chaque partie
    """
    #0: Strategie aveugle, 1:stratégie optimale
    
    P=constructionMatrice_P(D)
    result=np.empty([2,2])
    tab,strat=constructionTableDynamique(N,D,P)
    for a in range (2):
        for b in range(2):
            print("============== Nouvelle Partie: N=",N,' D=',D )
            if(a==0):
                print("Joueur 1 aveugle ")
            else:
                print("Joueur 1 optimale ")
            if(b==0):
                print("Joueur 2 aveugle ")
            else:
                print("Joueur 2 optimale ")
            g1=0
            g2=0
            while ((g1< N) and (g2<N)):
                if (a == 0):
                    print("Joueur 1 aveugle :")
                    d1=strategieAveugle(D)
                else :
                    print("Joueur 1 optimale :")
                    d1=strategieOptimale(g1,g2,strat)
                g=0
                for k in range (d1):
                    r=randint(1,6)
                    if (r == 1):
                        g=1
                        break
                    else:
                        g+=r
                g1+=g
                print("Tour Joueur 1, lance : ",d1," dés, gain :",g1 )
                if (b == 0):
                    print("Joueur 2 aveugle :")
                    d2=strategieAveugle(D)
                    
                else :
                    print("Joueur 2 optimale :")
                    d2=strategieOptimale(g2,g1,strat)
                g=0
                for k in range (d2):
                    
                    r=randint(1,6)
                    if (r == 1):
                        g=1
                        break
                    else:
                        g+=r
                g2+=g
                print("Tour Joueur 2, lance : ",d2," dés, gain :",g2 )
            if (g1==g2):
                result[a][b]=0
                print("Nulle")
            if (g1<g2):
                result[a][b]=2
                print("Joueur 2 gagne")
            if (g1>g2):
                print("Joueur 1 gagne")
                result[a][b]=1
    return result

   
def simulationGain(strat,N,D,s1,s2):
    """
    Simulation d'une partie du jeu, retourne le gain de chaque joueur
    """ 
    #s1,s2= 0: Strategie aveugle, 1:stratégie optimale 2:stratégie aléatoire
    g1=0
    g2=0
    while ((g1< N) and (g2<N)):
        if(s1 == 0):
            d1=strategieAveugle(D)
        if(s1 == 1):
            d1=strategieOptimale(g1,g2,strat)
        if(s1 == 2):
            d1=strategieAleatoire(D)
        g=0
        for k in range (d1):
            r=randint(1,6)
            if (r == 1):
                g=1
                break
            else:
                g+=r
        g1+=g
            
        if(s2 == 0):
            d2=strategieAveugle(D)
        if(s2 ==1 ) :
            d2=strategieOptimale(g2,g1,strat)
        if(s2 == 2):
            d2=strategieAleatoire(D)
        g=0
        for k in range (d2):
            r=randint(1,6)
            if (r == 1):
                g=1
                break
            else:
                g+=r
        g2+=g
                
    joueur1=0
    joueur2=0
    if (g1<g2):
        joueur2=1
    if (g1>g2):
        joueur1=1
    return joueur1, joueur2
              
            
def calculEsperanceGain_D(N,D):
    """
    Calcul d'espérance de gain en variant D
    """
    P=constructionMatrice_P(D)
    gain,tab=constructionTableDynamique(N,D,P)
    nb_parties=10
    A_O_1=[]
    A_O_2=[]
    O_A_1=[]
    O_A_2=[]
    A_A_1=[]
    A_A_2=[]
    O_O_1=[]
    O_O_2=[]
    A_R_1=[]
    A_R_2=[]
    R_O_1=[]
    R_O_2=[]
    
    print("aveugle vs optimale")
    
    for d in range(1,D+1):
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,N,d,0,1)
            G1+=g1
            G2+=g2
        print("D :",d)
        print("Esperance de gain du joueur 1 (aveugle) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (optimale) : ",G2/nb_parties)
        A_O_1.append(G1/nb_parties)
        A_O_2.append(G2/nb_parties)
    print("\n optimale vs aveugle")
    
    for d in range(1,D+1):
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,N,d,1,0)
            G1+=g1
            G2+=g2
        print("D :",d)
        print("Esperance de gain du joueur 1 (optimale) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (aveugle) : ",G2/nb_parties)
        O_A_1.append(G1/nb_parties)
        O_A_2.append(G2/nb_parties)
    print("\n aveugle vs aveugle")

    for d in range(1,D+1):
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,N,d,0,0)
            G1+=g1
            G2+=g2
        print("D :",d)
        print("Esperance de gain du joueur 1 (aveugle) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (aveugle) : ",G2/nb_parties)
        A_A_1.append(G1/nb_parties)
        A_A_2.append(G2/nb_parties)

    for d in range(1,D+1):
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,N,d,1,1)
            G1+=g1
            G2+=g2
        print("D :",d)
        print("Esperance de gain du joueur 1 (optimale) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (optimale) : ",G2/nb_parties)
        O_O_1.append(G1/nb_parties)
        O_O_2.append(G2/nb_parties)
        
    print("\n random vs optimale")

    for d in range(1,D+1):
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,N,d,2,1)
            G1+=g1
            G2+=g2
        print("D :",d)
        print("Esperance de gain du joueur 1 (random) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (optimale) : ",G2/nb_parties)
        R_O_1.append(G1/nb_parties)
        R_O_2.append(G2/nb_parties)
        
    print("\n aveugle vs random")

    for d in range(1,D+1):
        G1=0
        G2=0        
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,N,d,0,2)
            G1+=g1
            G2+=g2
        print("D :",d)
        print("Esperance de gain du joueur 1 (aveugle) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (random) : ",G2/nb_parties)
        A_R_1.append(G1/nb_parties)
        A_R_2.append(G2/nb_parties)
    
    return A_O_1, A_O_2, O_A_1, O_A_2, A_A_1, A_A_2, O_O_1, O_O_2, A_R_1, A_R_2, R_O_1, R_O_2



def calculEsperanceGain_N(D):
    """
    Calcul d'espérance de gain en variant N
    """
    A_O_1=[]
    A_O_2=[]
    O_A_1=[]
    O_A_2=[]
    A_A_1=[]
    A_A_2=[]
    O_O_1=[]
    O_O_2=[]
    A_R_1=[]
    A_R_2=[]
    R_O_1=[]
    R_O_2=[]
    nb_parties=20
    P=constructionMatrice_P(D)
    for n in range(50,550,50): 
        gain,tab=constructionTableDynamique(n,D,P)
        print("aveugle vs optimale")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,n,D,0,1)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (aveugle) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (optimale) : ",G2/nb_parties)
        A_O_1.append(G1/nb_parties)
        A_O_2.append(G2/nb_parties)
        
        print("\n optimale vs aveugle")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,n,D,1,0)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (optimale) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (aveugle) : ",G2/nb_parties)
        O_A_1.append(G1/nb_parties)
        O_A_2.append(G2/nb_parties)
        
        print("\n aveugle vs aveugle")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,n,D,0,0)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (aveugle) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (aveugle) : ",G2/nb_parties)
        A_A_1.append(G1/nb_parties)
        A_A_2.append(G2/nb_parties)
        
        print("\n optimale vs optimale")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,n,D,1,1)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (optimale) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (optimale) : ",G2/nb_parties)
        O_O_1.append(G1/nb_parties)
        O_O_2.append(G2/nb_parties)
        
        print("\n random vs optimale")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,n,D,2,1)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (random) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (optimale) : ",G2/nb_parties)
        R_O_1.append(G1/nb_parties)
        R_O_2.append(G2/nb_parties)
        
        print("\n aveugle vs random")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGain(tab,n,D,2,1)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (aveugle) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (random) : ",G2/nb_parties)
        A_R_1.append(G1/nb_parties)
        A_R_2.append(G2/nb_parties)
        
    
    return A_O_1, A_O_2, O_A_1, O_A_2, A_A_1, A_A_2, O_O_1, O_O_2, A_R_1, A_R_2, R_O_1, R_O_2 

#================================== VARIANTE SIMULTANÉE SIMPLE

   
def constructionEG(D,P):
    """
     Retourne la table d'espérances de gain 
    """ 
    EG=np.zeros([D+1,D+1])
    for i in range(1,D+1):
        for j in range(1,D+1):
            e1=0
            e2=0
            for k in range(1,(i*6)+1):
                e1+=P[i][k]*k
            for k in range(1,(j*6)+1):
                e2+=P[j][k]*k
            EG[i][j]=e1-e2
    return EG


def resolutionPL(D,EG):
    """
    Modélisation e résolution du programme linéaire 
    """ 
    p1=[0]*D
    my_lp_problem = pulp.LpProblem("My_LP_Problem", pulp.LpMaximize)
    z = pulp.LpVariable('z', cat='Continuous')
    for i in range(D):
        p1[i]=pulp.LpVariable('p'+str(i+1), lowBound=0, cat='Continuous')
    
    # Objective function
    my_lp_problem += z, "Z"
    # Constraints
    for j in range(1,D+1):
        #my_lp_problem += 0 <= p1[i-1]
        c= p1[0] * EG[1][j]
        for i in range(2,D+1):
            c+= + p1[i-1] * EG[i][j]
        my_lp_problem += z <= c   
    c=p1[0]
    for i in range(1,D):
        c+= + p1[i] 
    my_lp_problem += c <= 1
    my_lp_problem += c >= 1
    
    my_lp_problem.solve()
    pulp.LpStatus[my_lp_problem.status]
    L=[]
    for variable in my_lp_problem.variables():
        #print ("{} = {}".format(variable.name, variable.varValue))
        L.append(variable.varValue)
    return L


def strategieSimultane(D):
    """
    stratégie avec la résolution d'un programme linaire 
    """ 
    P=constructionMatrice_P(D)
    EG=constructionEG(D,P)
    p=resolutionPL(D,EG)
    return p.index(max(p))+1



def test_S_vs_A(Dmax):
    """
    Evaluation de l'espérance de gain 
    """
    G1=[0]*Dmax
    G2=[0]*Dmax
    for D in range(1,Dmax+1):
        for i in range(100):
            d1=strategieSimultane(D)#nb des du joueur 1
            d2=strategieAveugle(D)#nb des du joueur 2
            g1=0
            for k in range (d1):
                r=randint(1,6)
                if (r == 1):
                    g=1
                    break
                else:
                    g1+=r
            g2=0
            for k in range (d2):
                r=randint(1,6)
                if (r == 1):
                    g2=1
                    break
                else:
                    g2+=r
            if(g1>g2):
                G1[D-1]+=1
            else:
                G2[D-1]+=1
        G1[D-1]=G1[D-1]/100
        G2[D-1]=G2[D-1]/100
    return G1, G2

#================================== VARIANTE SIMULTANÉE GÉNÉRALE  

def construction_Eij(D,EG,P,i,j):
    """
    L'espérance de gain E(i, j) du joueur 1 etant donné l'état (i,j) en fonction de d1, d2 et EG1
    """
    E=np.zeros([D+1,D+1])
    for d1 in range(1,D+1):
        for d2 in range(1,D+1):
            for k1 in range(1,6*d1+1):
                for k2 in range(1,6*d2+1):
                    E[d1][d2]+=P[d1][k1]*P[d2][k2]*EG[i+k1][j+k2]
    return E


def construction_EG_General(N,D,P):
    """
    Table dynamique : retourne une table (N-1+6*D)x(N-1+6*D) des esperances de gain du joeur 1
    """
    cap=N-1+6*D
    EG=np.zeros([cap+1,cap+1])
    strat=[[1]*(cap+1)]*(cap+1)
    for i in range (N,cap+1):
        for j in range (cap+1):
            if(i>j):
                EG[i][j]=1
            elif(i==j):
                EG[i][j]=0
            else:
                EG[i][j]=-1      
    for j in range (N,cap+1):
        for i in range (N):
            if(i>j):
                EG[i][j]=1
            elif(i==j):
                EG[i][j]=0
            else:
                EG[i][j]=-1
    for i in range (N-1,-1,-1):
        for j in range (N-1,-1,-1):
            s=0
            E=construction_Eij(D,EG,P,i,j)
            p=resolutionPL(D,E)
            for k in range(D):
                s+=sum(E[k])/D*p[k]
            EG[i][j]+=s
            strat[i][j]=p.index(max(p))+1
    return EG,strat



def strategieSimultaneGeneral(i,j,strat):
    """
    strategie Optimale : le nombre de dés à lancer dans l'état (i,j)
    """
    return int(strat[i][j])


 
def simulationGainSimultane(stratSim, stratSeq,N,D,s1,s2):
    """
    Simulation d'une partie du jeu simultané, retourne le gain de chaque joueur
    """ 
    #s1,s2= 0: Strategie aveugle, 1:stratégie optimale Simultane 2:stratégie optimale Sequentielle
    g1=0
    g2=0
    while ((g1< N) and (g2<N)):
        d1=strategieSimultaneGeneral(g1,g2,stratSim)
        if(s2 == 0):
            d2=strategieAveugle(D)
        if(s2 == 1):
            d2=strategieSimultaneGeneral(g2,g1,stratSim)
        if(s2 == 2):
            d2=strategieOptimale(g2,g1,stratSeq)
        g=0
        for k in range (d1):
            r=randint(1,6)
            if (r == 1):
                g=1
                break
            else:
                g+=r
        g1+=g
        g=0
        for k in range (d2):
            r=randint(1,6)
            if (r == 1):
                g=1
                break
            else:
                g+=r
        g2+=g
                
    joueur1=0
    joueur2=0
    if (g1<g2):
        joueur2=1
    if (g1>g2):
        joueur1=1
    return joueur1, joueur2



def calculEsperanceGainGeneral_N(D):
    """
    Evaluation de l'espérance de gain en variant N
    """
    O_O=[]
    O_A=[]
    O_OSeq=[]
    P=constructionMatrice_P(D)
    nb_parties=20
    for n in range(5,160,20): 
        EGSim,stratSim=construction_EG_General(n,D,P)
        EGSeq,stratSeq=constructionTableDynamique(n,D,P)
        
        print("Optimale  vs Optimale")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGainSimultane(stratSim,[],n,D,1,1)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (Optimale) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (Optimale) : ",G2/nb_parties)
        O_O.append(G1/nb_parties)
        
        print("\n optimale vs aveugle")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGainSimultane(stratSim,[],n,D,1,0)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (optimale) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (aveugle) : ",G2/nb_parties)
        O_A.append(G1/nb_parties)
        
        print("\n Optimale vs Sequentielle Optimale ")
        G1=0
        G2=0
        for i in range(nb_parties):
            g1,g2=simulationGainSimultane(stratSim, stratSeq,n,D,1,2)
            G1+=g1
            G2+=g2
        print("N :",n,", D :",D )
        print("Esperance de gain du joueur 1 (Optimale) : ",G1/nb_parties)
        print("Esperance de gain du joueur 2 (Sequentielle optimale) : ",G2/nb_parties)
        O_OSeq.append(G1/nb_parties)
        
        
    return O_O, O_A,O_OSeq 
