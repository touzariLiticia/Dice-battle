#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 20:09:03 2019

@author: h_djeddal
"""
from tkinter import * 
import numpy as np
from random import *
import strategies as st

#============== Contre Ordinateur

N=100
D=5
inst="TRY TO REACH "+str(N)+" POINTS FIRST!" 
score_val=0
score_comp_val=100
result_val=80

P=st.constructionMatrice_P(D)
tab,strat=st.constructionTableDynamique(N,D,P)

#======================== Fonctions de Controle
def popup(t1,t2):
    fwin = Toplevel()		  
    fwin.title(t1)
    fwin.geometry('250x150')
    Label(fwin,text=t2).pack(side=TOP,padx=5,pady=15)
    
    frm=Frame(fwin, borderwidth=0)
    frm.pack(side=BOTTOM, padx=5, pady=5)

    Button(frm, text='New Game', command=lambda:[fwin.destroy(),start()]).pack(side=LEFT,padx=10, pady=10)
    Button(frm, text='Quit', command=fwin.destroy).pack(side=RIGHT, padx=10, pady=10)
    fwin.transient(fenetre) 	  # Réduction popup impossible 
    fwin.grab_set()		  # Interaction avec fenetre jeu impossible
    fenetre.wait_window(fenetre)
    
def start () :
    BoutonLancer['state']='normal'
    BoutonComp['state']='disabled'
    BoutonRestart['text']="Restart"
    global D
    for i in range(D):
        tirages[i].set('0')
        tirages2[i].set('0')
    for child in Choix_Frame.winfo_children():
        if child.winfo_class() == 'Radiobutton':
            child['state'] = 'active'
    score.set('0')
    score_comp.set('0')
    result.set('0')
    
    
def throw() :
    BoutonComp['state']='normal'
    d_val=int(d.get())
    som=True
    g=0
    for k in range (d_val):
        r=randint(1,6)
        tirages[k].set(str(r))
        if (r == 1):
            g=1
            som=False
        else:
            if(som):
                g+=r
    for k in range(d_val,D):
        tirages[k].set('0')
    s=int(score.get())+g
    result.set(str(g))
    score.set(str(s))
    global N
    BoutonLancer['state']='disabled'
    for child in Choix_Frame.winfo_children():
        if child.winfo_class() == 'Radiobutton':
            child['state'] = 'disabled'
    if (s>= N):
        popup("Hoory!", "You Won. :D")
   
    #----------Computer Turn
def computer():
    BoutonComp['state']='disabled'
    for child in Choix_Frame.winfo_children():
        if child.winfo_class() == 'Radiobutton':
            child['state'] = 'disabled'       
    global tab
    d2=st.strategieOptimale(int(score_comp.get()),int(score.get()),strat)
    som=True
    g=0
    for k in range (d2):
        r=randint(1,6)
        tirages2[k].set(str(r))
        if (r == 1):
            g=1
            som=False
        else:
            if(som):
                g+=r
    for k in range(d2,D):
        tirages2[k].set('0')
    s=int(score_comp.get())+g
    result.set(str(g))
    score_comp.set(str(s))
    BoutonLancer['state']='normal'
    for child in Choix_Frame.winfo_children():
        if child.winfo_class() == 'Radiobutton':
            child['state'] = 'active'
    if (s>= N):
        popup("Ooops!", "The Computer won. :/")
    
fenetre = Tk()
fenetre.geometry('450x400')
fenetre.title('DICE BATTLE')

Setting_Frame = Frame(fenetre, borderwidth=1, relief=GROOVE)
Setting_Frame.pack(side=BOTTOM, padx=1, pady=1)

BoutonRestart = Button(Setting_Frame, text ='Start', command = start)
BoutonRestart.pack(side = LEFT, padx = 5, pady = 5)

BoutonComp = Button(Setting_Frame, text ='Computer', state='disabled',command = computer)
BoutonComp.pack(side = LEFT, padx = 5, pady = 5)

BoutonQuitter = Button(Setting_Frame, text ='Quit', command = fenetre.destroy)
BoutonQuitter.pack(side = RIGHT, padx = 70, pady = 5)



Head_Frame=Frame(fenetre, width=440, height=350,borderwidth=1, relief=GROOVE)
Head_Frame.pack(side=TOP, padx=1, pady=1)

Label(Head_Frame,text=inst).pack(side=TOP,padx=5,pady=5)

Score_Frame=Frame(Head_Frame, borderwidth=1)
Score_Frame.pack(side=TOP, padx=1, pady=1)

score =StringVar()

AgentScore_Frame=Frame(Score_Frame, borderwidth=1)
AgentScore_Frame.pack(side=LEFT, padx=55, pady=1)
Label(AgentScore_Frame,text="SCORE : ").pack(side=LEFT,padx=1,pady=1)
Label(AgentScore_Frame,textvariable=score).pack(side=LEFT,padx=1,pady=1)

score_comp =StringVar()

CompScore_Frame=Frame(Score_Frame, borderwidth=1)
CompScore_Frame.pack(side=RIGHT, padx=35, pady=1)
Label(CompScore_Frame,textvariable=score_comp).pack(side=RIGHT,padx=1,pady=1)
Label(CompScore_Frame,text="COMPUTER SCORE : ").pack(side=RIGHT,padx=1,pady=1)


result =StringVar()

Control_Frame=Frame(fenetre, width=440, height=350,borderwidth=0, relief=GROOVE)
Control_Frame.pack(side=TOP, padx=1, pady=1)
Label(Control_Frame,textvariable=result).pack(side=RIGHT,padx=5,pady=5)
Label(Control_Frame,text="Result : ").pack(side=RIGHT,padx=5,pady=5)
BoutonLancer = Button(Control_Frame, text ='Throw', state='disabled',command = throw)
BoutonLancer.pack(side = LEFT, padx = 60, pady = 5)

Game_Frame=Frame(fenetre, width=440, height=350,borderwidth=0, relief=GROOVE)
Game_Frame.pack(side=LEFT, padx=5, pady=5)
Agent_Frame=Frame(Game_Frame, width=440, height=350,borderwidth=1, relief=GROOVE)
Agent_Frame.pack(side=LEFT, padx=1, pady=1)

Choix_Frame=Frame(Agent_Frame, width=440, height=350,borderwidth=0, relief=GROOVE)
Choix_Frame.pack(side=LEFT, padx=1, pady=1)

Result_Frame=Frame(Agent_Frame, width=440, height=350,borderwidth=0, relief=GROOVE)
Result_Frame.pack(side=RIGHT, padx=1, pady=1)
Label(Choix_Frame,text="Choose your dice").pack(side=TOP,padx=5,pady=5)

d = StringVar()
dice = {"1 Dice" : "1", 
          "2 Dice" : "2", 
          "3 Dice" : "3", 
          "4 Dice" : "4", 
          "5 Dice" : "5"} 
tirages=[]
for (text, value) in dice.items(): 
    Radiobutton(Choix_Frame, text = text, variable = d,  value = value, state='disabled').pack(side=TOP,ipadx=5, ipady=5)
Label(Result_Frame, text="").pack(side=TOP,ipadx=5, ipady=5)
for i in range(D):
    tirages.append(StringVar())
    Label(Result_Frame, textvariable = tirages[i]).pack(side=TOP,ipadx=5, ipady=5)
  
tirages2=[]
Computer_Frame=Frame(Game_Frame, width=440, height=350,borderwidth=0, relief=GROOVE)
Computer_Frame.pack(side=TOP, padx=105, pady=5)
Label(Computer_Frame,text="Computer").pack(side=TOP,padx=1,pady=1)
Result2_Frame=Frame(Computer_Frame, width=440, height=350,borderwidth=0, relief=GROOVE)
Result2_Frame.pack(side=RIGHT, padx=5, pady=5)
for i in range(D): 
    tirages2.append(StringVar())
    Label(Result2_Frame, textvariable = tirages2[i]).pack(side=TOP,ipadx=5, ipady=5)
    
    

    

fenetre.mainloop()
