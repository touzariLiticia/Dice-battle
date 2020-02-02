#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:01:40 2019

@author: Touzari Liticia
@author : Djeddal Hanane
"""
import strategies as st
import matplotlib.pyplot as plt

"""____________________________M A I N_______________________________"""   
N=50
D=10

#_____________Prg Dynamique Séquentielle
#P=st.constructionMatrice_P(D)
#tab,strat=st.constructionTableDynamique(N,D,P)

#print(strat)
#print(st.strategieAveugle(D))
#print(st.strategieOptimale(80,3,strat)) 

#_____________Simulation Séquentielle
#print(st.simulation(N,D))
"""  Graphes
t=st.calculEsperanceGain_N(D)
plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aveugle vs Optimale")
plt.plot([50,100,150,200,250,300,350,400,450,500],t[0])
plt.show()

plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Optimale vs Aveugle")
plt.plot([50,100,150,200,250,300,350,400,450,500],t[2])
plt.show()


plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aveugle vs Aveugle")
plt.plot([50,100,150,200,250,300,350,400,450,500],t[4])
plt.show()


plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Optimale vs Optimale")
plt.plot([50,100,150,200,250,300,350,400,450,500],t[6])
plt.show()

plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aveugle vs ALéatoire")
plt.plot([50,100,150,200,250,300,350,400,450,500],t[8])
plt.show()


plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aléatoire vs Optimale")
plt.plot([50,100,150,200,250,300,350,400,450,500],t[10])
plt.show()

print(t)
"""
"""
t=st.calculEsperanceGain_D(50,30)

plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aveugle vs Optimale")
plt.plot([i for i in range(1,31)],t[0])
plt.show()

plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Optimale vs Aveugle")
plt.plot([i for i in range(1,31)],t[2])
plt.show()


plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aveugle vs Aveugle")
plt.plot([i for i in range(1,31)],t[4])
plt.show()


plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Optimale vs Optimale")
plt.plot([i for i in range(1,31)],t[6])
plt.show()

plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aveugle vs Aléatoire")
plt.plot([i for i in range(1,31)],t[8])
plt.show()


plt.xlabel('Nombre de points à atteindre : N')
plt.ylabel('Espérance de Gain ')
plt.title("Aléatoire vs Optimale")
plt.plot([i for i in range(1,31)],t[10])
plt.show()

print(t)
"""
#_____________Prg linéaire Simultanée
#EG=st.constructionEG(D,P)
#print(st.resolutionPL(D,EG))

"""__Graphe  """


Dmax=30
t1,t2=st.test_S_vs_A(Dmax)
plt.xlabel('Nombre de dès : D')
plt.ylabel('Espérance de Gain ')
plt.title("Optimale vs Aveugle")
x=[i for i in range(1,Dmax+1)]
plt.plot(x,t1,"o--", label="joeur1 optimale")
plt.plot(x,t2,"o--", color='fuchsia',label="joeur2 aveugle")
plt.legend()
plt.show()

#_____________Simulation Simultanée
#g1,g2=st.test_S_vs_A(D)
#print("Esperance du gain Joeur 1 (optimale) :",g1, ". Esperance du gain Joeur 2 (aveugle) :",g2)


#_____________Prg Dynamique Simultanée
#EG2,strat=st.construction_EG_General(N,D,P)
#evalEG=st.calculEsperanceGainGeneral_N(D)
#print(evalEG)