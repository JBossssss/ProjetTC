# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 18:33:13 2023

@author: Jean Bériot
"""

import streamlit as st
import math as m

st.title("Synthèse de filtres RCAO")


st.header("Choix du filtre")
sel=st.selectbox("Avec quel type de filtre désirez-vous travailler?",['LPLQ (Passe-Bas de Sallen-Key, Q<2)','HPLQ (Passe-Haut de Sallen-Key, Q<2)','LPMQ (Passe-Bas de Sallen-Key, Q<5)','HPMQ (Passe-Haut de Sallen-Key, Q<5)',
                                                                      'BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)'])

if sel =='LPLQ (Passe-Bas de Sallen-Key, Q<2)':
   
   st.image('iLP-LQ.jpg')
   if st.checkbox('**Choisir ce filtre**:+1:',key=1):
       
       st.header("Entrée des paramètres du filtre")
       fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
       st.write('Valeur de fp: ',fp,' Hertz.')
       qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
       st.write('Valeur de Qp: ',qp)
       C2=st.number_input('**Choix de C2**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
       st.write('Valeur de C2: ',C2,' Farads.')
       C4=st.number_input('**Choix de C4**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
       st.write('Valeur de C4: ',C4,' Farads.')
       k=st.number_input('**Choix de K (<=1)**',min_value=0.00,max_value=1.00,value=0.50,step=None)
       st.write('Valeur de K: ',k)
       
       if st.checkbox('**Valider les données**:+1:',key=2):
           
           if (1/(2*qp*qp)) * C2/C4 <=2:
               st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que**  $C2>=4*Qp^2*C4$')
               
           else :
               P = ( (1/(2*qp*qp)) * C2/C4 -1) + m.sqrt( ((1/(2*qp*qp)) * C2/C4 -1)*((1/(2*qp*qp)) * C2/C4 -1) -1 )
               R1 = 1/(2*m.pi*fp*m.sqrt(P*C2*C4))
               R3=P*R1
               GSP=qp*m.sqrt(C2/(P*C4));
               
               if k==0.00:
                   R11=R1
                   R12=float('inf')
                   k=1
            
               else :
                   R11=R1*k
                   R12=R1/(1-k)
           
               st.header('Données calculées:')
               st.write('**R11 =** ',R11,' Ohms.')
               st.write('**R12 =** ',R12,' Ohms.')
               st.write('**R3 =** ',R3,' Ohms.')
               st.write('**GSP =** ',GSP)
                         
                           
      
if sel =='HPLQ (Passe-Haut de Sallen-Key, Q<2)':
   
    st.image('iHP-LQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C11=st.number_input('**Choix de C11**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C11: ',C11,' Farads.')
        C12=st.number_input('**Choix de C12**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C12: ',C12,' Farads.')
        C3=st.number_input('**Choix de C3**',min_value=0.00,value=0.50,step=None,format='%0.10f')
        st.write('Valeur de C3: ',C3)
        
        if st.checkbox('**Valider les données**:+1:',key=2):
            
                C1=(C11+C12)
                P=((qp*qp)*(2+(C3/C1)+(C1/C3)))
                R2=(1/(2*m.pi*fp*m.sqrt(P*C1*C3)))
                R4=(P*R2)
                GSP=(qp*m.sqrt(P*C3/C1))
                K=(C11/C1)

                st.header('Données calculées:')
                st.write('**C1 =** ',C1,' Farads.')
                st.write('**R2 =** ',R2,' Ohms.')
                st.write('**R4 =** ',R4,' Ohms.')
                st.write('**GSP =** ',GSP)
                st.write('**K =** ',K)
                         
                            
    
if sel =='LPMQ (Passe-Bas de Sallen-Key, Q<5)':
   
    st.image('iLP-MQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C2=st.number_input('**Choix de C2**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C2: ',C2,' Farads.')
        C4=st.number_input('**Choix de C4**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C4: ',C4,' Farads.')
        k=st.number_input('**Choix de K**',min_value=0.00,value=0.50,step=None)
        st.write('Valeur de K: ',k)
        R5=st.number_input('**Choix de R5 (Optionnel)**',min_value=0.00,value=100.00,step=None)
        st.write('Valeur de R5: ',R5,' Ohms.')
        
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            P=(C2/C4)/(36*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C4/C2))+1)*(m.sqrt(1+12*qp*qp*(1+C4/C2))+1)
            R1=1/(2*m.pi*fp*m.sqrt(P*C2*C4))
            R3=P*R1
            if R5==0:
                R5=1e4
          
            R6=R5*(C4/C2*(1+P)-m.sqrt(P*C4/C2)/qp)
            K0=1+R6/R5
            GSP=qp*K0*K0*m.sqrt(C2/(P*C4))
            
            if k==0.00 :
                R11=R1
                R12=1e90
                K=K0
            if K0-k<=0.00:
                R11=R1
                R12=1e90
                K=K0
            else:
                K=k
                R11=K0/K*R1
                R12=K0/(K0-K)*R1
            
            st.header('Données calculées:')
            st.write('**R11 =** ',R11,' Farads.')
            st.write('**R12 =** ',R12,' Ohms.')
            st.write('**R3 =** ',R3,' Ohms.')
            st.write('**R6 =** ',R6,' Ohms.')
            st.write('**GSP =** ',GSP)
            st.write('**K =** ',K)
                         
                            
    
if sel =='HPMQ (Passe-Haut de Sallen-Key, Q<5)':
   
    st.image('iHP-MQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        
        C2=st.number_input('Choix de C2',min_value=0.00,value=0.00000001,step=0.0000001)
        st.write('Valeur de C2: ',C2,' Farads.')
        C4=st.number_input('Choix de C4',min_value=0.00,value=0.00000001,step=0.0000001,format="%0.12f")
        st.write('Valeur de C4: ',C4,' Farads.')
        k=st.number_input('Choix de K (<=1)',min_value=0.00,max_value=1.00,value=0.50,step=None)
        st.write('Valeur de K: ',k)

        C11=st.number_input('**Choix de C11**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C11: ',C11,' Farads.')
        C12=st.number_input('**Choix de C12**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C12: ',C12,' Farads.')
        C3=st.number_input('**Choix de C3**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C3: ',C3,' Farads.')
        R5=st.number_input('**Choix de R5 (Optionnel)**',min_value=0.00,value=100.00,step=None)
        st.write('Valeur de R5: ',R5,' Ohms.')
        
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            C1=C11+C12
            P=(C1/C3)/(4*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)
        
            R2=1/(2*m.pi*fp*m.sqrt(P*C1*C3))
            R4=P*R2
            
            if R5==0:
                R5=1e4
            
            R6=R5*(1/P*(1+C1/C3)-m.sqrt(C1/(P*C3))/qp)
            K=C11/C1*(1+R6/R5)
            GSP=qp*(1+R6/R5)*(1+R6/R5)*m.sqrt((P*C3)/C1)

            
            st.header('Données calculées:')
            st.write('**R2 =** ',R2,' Ohms.')
            st.write('**R4 =** ',R4,' Ohms.')
            st.write('**R6 =** ',R6,' Ohms.')
            st.write('**GSP =** ',GSP)

if sel =='BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)':

    st.image('iBR-LPN-HPN-MQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C11=st.number_input('**Choix de C11**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C11: ',C11,' Farads.')
        C12=st.number_input('**Choix de C12**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C12: ',C12,' Farads.')
        C3=st.number_input('**Choix de C3**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C3: ',C3,' Farads.')
        R5=st.number_input('**Choix de R5 (Optionnel)**',min_value=0.00,value=100.00,step=None)
        st.write('Valeur de R5: ',R5,' Ohms.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            C1=C11+C12
            P=(C1/C3)/(4*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)
            
            R2=1/(2*m.pi*fp*m.sqrt(P*C1*C3))
            R4=P*R2
            
            if R5==0:
                R5=1e4
                
            R6=R5*(1/P*(1+C1/C3)-m.sqrt(C1/(P*C3))/qp)
            K=C11/C1*(1+R6/R5)
            GSP=qp*(1+R6/R5)*(1+R6/R5)*m.sqrt((P*C3)/C1)
            
            
            st.header('Données calculées:')
            st.write('**R2 =** ',R2,' Ohms.')
            st.write('**R4 =** ',R4,' Ohms.')
            st.write('**R6 =** ',R6,' Ohms.')
            st.write('**GSP =** ',GSP)




