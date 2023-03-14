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
    ast=st.number_input("**Choix de As (Atténuation minimum après Ws)**",min_value=0.00,value=45.00,step=None)
    st.write('Valeur de As: ',ast,' dB.')
    
    if st.checkbox('**Valider les données**:+1:',key=1):
        
        wcn=wc/wc
        wsn=ws/wc
        
        approx=st.selectbox("**Quel type d'approximation voulez-vous utiliser?**",['Butterworth','Chebychev I','Chebychev II','Cauer','Bessel'])
        
        if approx=='Butterworth':
            [n,wn]=sc.buttord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z,p,k]=sc.butter(n,wn,analog=True,output='zpk')
            st.write("Degré du filtre:  ",n)
            st.write("Z,P et K:  ",z,"    ",p,"    ",k)
            
            if (n%2)!=0:
                nsupfloat=(n-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p[nsupint]
                # st.write(pdeg1)
                p=np.delete(p,nsupint)
                # st.write(p)
                
            else:
                nsupfloat=n/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z, p, k, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
            
        if approx=='Chebychev I':
            [n1,wn1]=sc.cheb1ord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z1,p1,k1]=sc.cheby1(n1,ap,wn1,analog=True,output='zpk');
            st.write("Degré du filtre:  ",n1)
            if (n1%2)!=0:
                nsupfloat=(n1-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p1[nsupint]
                # st.write(pdeg1)
                p1=np.delete(p1,nsupint)
                # st.write(p1)
                
            else:
                nsupfloat=n1/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z1, p1, k1, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
            
        if approx=='Chebychev II':
            [n2,wn2]=sc.cheb2ord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z2,p2,k2]=sc.cheby2(n2,ap,wn2,analog=True,output='zpk');
            st.write("Degré du filtre:  ",n2)
            if (n2%2)!=0:
                nsupfloat=(n2-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p2[nsupint]
                # st.write(pdeg1)
                p2=np.delete(p2,nsupint)
                # st.write(p2)
                
            else:
                nsupfloat=n2/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z2, p2, k2, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
        if approx=='Cauer':
            [n3,wn3]=sc.ellipord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z3,p3,k3]=sc.ellip(n3,ap,ast,wn3,analog=True,output='zpk')
            # freq3=sc.sosfreqz(sos3, worN=512, whole=False, fs=2*m.pi)
            # sc.sosfilt()
            st.write("Degré du filtre:  ",n3)
            if (n3%2)!=0:
                nsupfloat=(n3-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p3[nsupint]
                # st.write(pdeg1)
                p3=np.delete(p3,nsupint)
                # st.write(p3)
                
            else:
                nsupfloat=n3/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z3, p3, k3, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
        if approx=='Bessel':
            st.write('Coming soon...')
            
elif typ=='Passe-haut':
    
    ws=st.number_input("**Choix de Ws (Pulsation de fin de bande atténuée)**",min_value=0.00,value=1000.00,step=None)
    st.write('Valeur de Ws: ',ws,' Radians/seconde.')
    wc=st.number_input("**Choix de Wc (Pulsation de début de bande passante)**",min_value=0.00,value=2000.00,step=None)
    st.write('Valeur de Wc: ',wc,' Radians/seconde.')
    ap=st.number_input("**Choix de Ap (Ripple maximum en bande passante)**",min_value=0.00,value=1.00,step=None)
    st.write('Valeur de Ap: ',ap,' dB.')
    ast=st.number_input("**Choix de As (Atténuation minimum avant Ws)**",min_value=0.00,value=45.00,step=None)
    st.write('Valeur de As: ',ast,' dB.')
    
    if st.checkbox('**Valider les données**:+1:',key=2):
        
        wcn=wc/wc  #normalement c'est -wc/wc
        wsn=wc/ws  #normalement c'est -wc/ws
        approx=st.selectbox("**Quel type d'approximation voulez-vous utiliser?**",['Butterworth','Chebychev I','Chebychev II','Cauer','Bessel'])
        
        if approx=='Butterworth':
            [n,wn]=sc.buttord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z,p,k]=sc.butter(n,wn,analog=True,output='zpk')
            st.write("Degré du filtre:  ",n)
            # st.write("Z,P et K:  ",z,"    ",p,"    ",k)
            
            if (n%2)!=0:
                nsupfloat=(n-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p[nsupint]
                # st.write(pdeg1)
                p=np.delete(p,nsupint)
                # st.write(p)
                
            else:
                nsupfloat=n/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z, p, k, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
            
        if approx=='Chebychev I':
            [n1,wn1]=sc.cheb1ord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z1,p1,k1]=sc.cheby1(n1,ap,wn1,analog=True,output='zpk');
            st.write("Degré du filtre:  ",n1)
            if (n1%2)!=0:
                nsupfloat=(n1-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p1[nsupint]
                # st.write(pdeg1)
                p1=np.delete(p1,nsupint)
                # st.write(p1)
                
            else:
                nsupfloat=n1/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z1, p1, k1, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
            
        if approx=='Chebychev II':
            [n2,wn2]=sc.cheb2ord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z2,p2,k2]=sc.cheby2(n2,ap,wn2,analog=True,output='zpk');
            st.write("Degré du filtre:  ",n2)
            if (n2%2)!=0:
                nsupfloat=(n2-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p2[nsupint]
                # st.write(pdeg1)
                p2=np.delete(p2,nsupint)
                # st.write(p2)
                
            else:
                nsupfloat=n2/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z2, p2, k2, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
        if approx=='Cauer':
            [n3,wn3]=sc.ellipord(wcn, wsn, ap, ast, analog=True,fs=None)
            [z3,p3,k3]=sc.ellip(n3,ap,ast,wn3,analog=True,output='zpk')
            # freq3=sc.sosfreqz(sos3, worN=512, whole=False, fs=2*m.pi)
            # sc.sosfilt()
            st.write("Degré du filtre:  ",n3)
            if (n3%2)!=0:
                nsupfloat=(n3-1)/2
                nsupint=int(nsupfloat)
                # st.write(nsupint)
                pdeg1=p3[nsupint]
                # st.write(pdeg1)
                p3=np.delete(p3,nsupint)
                # st.write(p3)
                
            else:
                nsupfloat=n3/2
                nsupint=int(nsupfloat)
              
            sos=sc.zpk2sos(z3, p3, k3, pairing=None, analog=True)
            st.write(sos)
            for i in range(nsupint):
                st.write("**Section du second degré** ",i+1)
                # st.write(sos[i,0])
                coefpcarrenum=round(sos[i,0],2)
                coefpnum=round(sos[i,1],2)
                tindnum=round(sos[i,2],2)
                # st.write(tindnum)
                # coefpcarredenum=int(sos[i,5])
                # coefpdenum=int(sos[i,4])
                # tinddenum=int(sos[i,3])
                
                
                if coefpcarrenum==0.00:
                    
                    if coefpnum==0.00:
                        st.write("C'est une section Passe-Bas")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Bande")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<2),Rauch type C(Q<2),Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<2)','Rauch type C(Q<2)','Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Rauch type R(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<10.00:
                            st.write("Qp est inférieur à 10, ce qui vous laisse le choix entre utiliser une section de Rauch type R(Q<10),Rauch type C(Q<10) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Rauch type R(Q<10)','Rauch type C(Q<10)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Rauch type R(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Rauch type C(Q<10)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                elif coefpnum==0.00:
                    
                    if tindnum==0.00:
                        st.write("C'est une section Passe-Haut")
                        wp=m.sqrt(sos[i,5])
                        qp=wp/sos[i,4]
                        wp=wp*wc        
                        if qp<2.00:
                            st.write("Qp est inférieur à 2, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<2),Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key(Q<2)':
                                st.write("Coming soon")
                            elif typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+20)    
                            if typsos=='Sallen-key(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
                                
                    else:
                        st.write("C'est une section Réjecteur de fréquence")
                        wp=m.sqrt(sos[i,5])
                        wz=m.sqrt(sos[i,2]/sos[i,0])
                        qp=wp/sos[i,4]
                        wp=wp*wc 
                        wz=wz*wc
                        if qp<5.00:
                            st.write("Qp est inférieur à 5, ce qui vous laisse le choix entre utiliser une section de Sallen-key double T(Q<5) ou Flieghe(Q<30).")
                            typsos=st.selectbox("**Choix du type de filtre**",['Sallen-key(Q<2)','Sallen-key(Q<5)','Flieghe(Q<30)'],key=i+10)
                            if typsos=='Sallen-key double T(Q<5)':
                                st.write("Coming soon")
                            elif typsos=='Flieghe(Q<30)':
                                st.write("Coming soon")
                        elif qp<30.00:
                            st.write("Qp est inférieur à 30, ce qui vous oblige à utiliser une section de Flieghe(Q<30).")
                            
                        else :
                            st.write("Qp est trop élevé (",qp,"). Veuillez modifier les paramètres généraux du filtre.")
        if approx=='Bessel':
            st.write('Coming soon...')
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








