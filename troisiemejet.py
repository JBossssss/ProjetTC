# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:21:50 2023

@author: Jean Bériot
"""
import streamlit as st
import math as m
from Utils_Projet import *
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams
import scipy.signal as sc

st.title("Synthèse de filtres RCAO")

st.header("Choix du type de filtre")
typ=st.selectbox("**Avec quel type de filtre désirez-vous travailler?**",['Passe-bas','Passe-haut','Passe-bande','Coupe-bande'])

if typ=='Passe-bas':
    
    wc=st.number_input("**Choix de Wc (Pulsation de début d'atténuation)**",min_value=0.00,value=1000.00,step=None)
    st.write('Valeur de Wc: ',wc,' Radians/seconde.')
    ws=st.number_input("**Choix de Ws (Pulsation de fin d'atténuation)**",min_value=0.00,value=2000.00,step=None)
    st.write('Valeur de Ws: ',ws,' Radians/seconde.')
    ap=st.number_input("**Choix de Ap (Ripple maximum avant atténuation)**",min_value=0.00,value=1.00,step=None)
    st.write('Valeur de Ap: ',ap,' dB.')
    ast=st.number_input("**Choix de As (Atténuation minimum après Ws)**",min_value=0.00,value=40.00,step=None)
    st.write('Valeur de As: ',ast,' dB.')
    
    if st.checkbox('**Valider les données**:+1:',key=1):
        
        wcn=wc/wc
        wsn=ws/wc
        
        approx=st.selectbox("**Quel type d'approximation voulez-vous utiliser?**",['Butterworth','Chebychev I','Chebychev II','Cauer','Bessel'])
        
        if approx=='Butterworth':
            [n,wn]=sc.buttord(wcn, wsn, ap, ast, analog=True,fs=None)
            [N,D]=sc.butter(n,wn,analog=True)
            M=D.shape
            deg=M[0]-1
            st.write("Degré du filtre:  ",deg)
            
        if approx=='Chebychev I':
            st.write('Coming soon...')
            
        if approx=='Chebychev II':
            st.write('Coming soon...')
            
        if approx=='Cauer':
            st.write('Coming soon...')
        
        if approx=='Bessel':
            st.write('Coming soon...')
            
elif typ=='Passe-haut':
    
    ws=st.number_input("**Choix de Ws (Pulsation de fin de bande atténuée)**",min_value=0.00,value=1000.00,step=None)
    st.write('Valeur de Ws: ',ws,' Radians/seconde.')
    wc=st.number_input("**Choix de Wc (Pulsation de début de bande passante)**",min_value=0.00,value=2000.00,step=None)
    st.write('Valeur de Wc: ',wc,' Radians/seconde.')
    
    if st.checkbox('**Valider les données**:+1:',key=2):
        
        wcn=-wc/wc
        wsn=-wc/ws

elif typ=='Passe-bande':
    
    wsinf=st.number_input("**Choix de Ws- (Pulsation de fin de bande atténuée inférieure)**",min_value=0.00,value=1000.00,step=None)
    st.write('Valeur de Ws-: ',wsinf,' Radians/seconde.')
    wcinf=st.number_input("**Choix de Wc- (Pulsation de début de bande passante)**",min_value=0.00,value=2000.00,step=None)
    st.write('Valeur de Wc-: ',wcinf,' Radians/seconde.')
    wcsup=st.number_input("**Choix de Wc+ (Pulsation de fin de bande passante)**",min_value=0.00,value=3000.00,step=None)
    st.write('Valeur de Wc+: ',wcsup,' Radians/seconde.')
    wssup=st.number_input("**Choix de Ws+ (Pulsation de début de bande atténuée supérieure)**",min_value=0.00,value=4000.00,step=None)
    st.write('Valeur de Ws+: ',wssup,' Radians/seconde.')
    
    if st.checkbox('**Valider les données**:+1:',key=3):
        
        B=wcsup-wcinf
        w0=m.sqrt(wcsup*wcinf)
        wsinfn=(wsinf^2-w0^2)/(B*wsinf)
        wcinfn=(wcinf^2-w0^2)/(B*wcinf)
        wcsupn=(wcsup^2-w0^2)/(B*wcsup)
        wssupn=(wssup^2-w0^2)/(B*wssup)

elif typ=='Coupe-bande':
    
    wcinf=st.number_input("**Choix de Wc- (Pulsation de fin de bande passante inférieure)**",min_value=0.00,value=1000.00,step=None)
    st.write('Valeur de Wc-: ',wcinf,' Radians/seconde.')
    wsinf=st.number_input("**Choix de Ws- (Pulsation de début de bande atténuée)**",min_value=0.00,value=2000.00,step=None)
    st.write('Valeur de Ws-: ',wsinf,' Radians/seconde.')
    wssup=st.number_input("**Choix de Ws+ (Pulsation de fin de bande atténuée)**",min_value=0.00,value=3000.00,step=None)
    st.write('Valeur de Ws+: ',wssup,' Radians/seconde.')
    wcsup=st.number_input("**Choix de Wc+ (Pulsation de début de bande passante supérieure)**",min_value=0.00,value=4000.00,step=None)
    st.write('Valeur de Wc+: ',wcsup,' Radians/seconde.')
    
    if st.checkbox('**Valider les données**:+1:',key=4):
        
        B=wcsup-wcinf
        w0=m.sqrt(wcsup*wcinf)
        wcinfn=(B*wcinf)/(w0^2-wcinf^2)
        wsinfn=(B*wsinf)/(w0^2-wsinf^2)
        wssupn=(B*wssup)/(w0^2-wssup^2)
        wcsupn=(B*wcsup)/(w0^2-wcsup^2)








