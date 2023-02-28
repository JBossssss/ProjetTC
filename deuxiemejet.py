# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 18:33:13 2023

@author: Jean Bériot
"""

import streamlit as st
import math as m
#from Utils_Projet import *

st.title("Synthèse de filtres RCAO")


st.header("Choix du filtre")
sel=st.selectbox("Avec quel type de filtre désirez-vous travailler?",['LPLQ (Passe-bas de Sallen-Key, Q<2)','HPLQ (Passe-haut de Sallen-Key, Q<2)','LPMQ (Passe-bas de Sallen-Key, Q<5)','HPMQ (Passe-haut de Sallen-Key, Q<5)',
                                                                      'BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)','BPLQR (Passe-bande de Rauch (de type R), Q<2)','BPLQC (Passe-bande de Rauch (de type C), Q<2)',
                                                                      'BPMQR (Passe-bande de Rauch (de type R), Q<10)','BPMQC (Passe-bande de Rauch (de type C), Q<10)','Passe-bas de Flieghe (Q<30)','Passe-bande de Flieghe (Q<30)',
                                                                      'Passe-haut de Flieghe (Q<30)','Réjecteur de fréquence de Flieghe (Q<30)'])

if sel =='LPLQ (Passe-bas de Sallen-Key, Q<2)':
   
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
                         
                           
      
elif sel =='HPLQ (Passe-haut de Sallen-Key, Q<2)':
   
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
                         
                            
    
elif sel =='LPMQ (Passe-bas de Sallen-Key, Q<5)':
   
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
                         
                           
    
elif sel =='HPMQ (Passe-haut de Sallen-Key, Q<5)':
   
    st.image('iHP-MQ.jpg')
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



elif sel =='BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)':

    st.image('iBR-LPN-HPN-MQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fz=st.number_input('**Choix de fz**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fz: ',fz,' Hertz.')
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C1=st.number_input('**Choix de C1**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C1: ',C1,' Farads.')
        C2=st.number_input('**Choix de C2**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C2: ',C2,' Farads.')
        C3=st.number_input('**Choix de C3**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C3: ',C3,' Farads.')
        C4=st.number_input('**Choix de C4**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C4: ',C4,' Farads.')
        R9=st.number_input('**Choix de R9 (Optionnel)**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de R9: ',R9,' Ohms.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            q_circ=1./(2*m.sqrt((1+(C2/C1))*(1+C2/C3)))
            R5=1/(4*m.pi*fz*q_circ*(C2+C3))
            CS=(C1*C2)/(C1+C2)
            R6=(1+C2/C1)/(R5*((2*m.pi*fz)*(2*m.pi*fz))*C2*C3)
            RS=R5+R6
            R7=1/(((2*m.pi*fz)*(2*m.pi*fz))*C1*C2*RS)
            H=((1+C4/CS)*((fp/fz)*(fp/fz)))-1
            
            if H<0.00:
                st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que**  $C4>=|(fz^2/fp^2-1)*(C1*C2)/(C1+C2)|$')
                C4ideal=abs(((fz*fz)/(fp*fp)-1)*(C1*C2)/(C1+C2))
                st.write('Nous vous conseillons donc une valeur de C4 supérieure à cette dernière:  ',C4ideal,'  Farads.')
                st.markdown('**Note**: Si cette valeur vous semble trop importante, il conviendra donc de : ')
                st.write('- Diminuer la valeur de fz')
                st.write('- Augmenter la valeur de fp')
                st.write('- Diminuer la valeur de C1 ou C2')
                
            else: 
                if H==0.00:
                    R8=float('inf')
                    
                else :
                    R8=(R5+R6)/H
                
                if R9==0.00:
                    R9=10e4
                
                R10=R9*q_circ*((1/(R8*CS*2*m.pi*fz))+(RS*C4*2*m.pi*fz)-((1+(C4/CS))*(fp/fz)/qp))
                GSP=qp*((1+(R10/R9))*(1+(R10/R9)))*((m.sqrt(R5*C3/(R6*CS))+m.sqrt(RS*C2/(R7*C1)))/((1+(C4/CS))*(fp/fz)))
                K=(1+(R10/R9))/(1+(C4/CS))
                
                st.header('Données calculées:')
                st.write('**R5 =** ',R5,' Ohms.')
                st.write('**R6 =** ',R6,' Ohms.')
                st.write('**R7 =** ',R7,' Ohms.')
                st.write('**R8 =** ',R8,' Ohms.')
                st.write('**R10 =** ',R10,' Ohms.')
                st.write('**K =** ',K)
                st.write('**GSP =** ',GSP)



elif sel=='BPLQR (Passe-bande de Rauch (de type R), Q<2)':
    
    st.image('iBP-LQ-R.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C2=st.number_input('**Choix de C2**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C2: ',C2,' Farads.')
        C3=st.number_input('**Choix de C3**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C3: ',C3,' Farads.')
        k=st.number_input('**Choix de K**',min_value=0.00,value=0.50,step=None)
        st.write('Valeur de K: ',k)
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            P=(qp*qp)*((2+(C2/C3)+(C3/C2)))
            R1=1/((2*m.pi*fp*m.sqrt(P*C2*C3)))
            R4=P*R1
            K0=(qp*qp)*(1+(C3/C2))
            GSP=K0
            
            if k==0:
                R11=R1
                R12=float('inf')
                K=K0
                
            if (K0-k)<=0 :
                R11=R1
                R12=float('inf')
                K=K0
                
            else :
                K=k
                R11=(K0/k)*R1
                R12=(K0/(K0-k))*R1
                
            st.header('Données calculées:')
            st.write('**R11 =** ',R11,' Ohms.')
            st.write('**R12 =** ',R12,' Ohms.')
            st.write('**R4 =** ',R4,' Ohms.')
            st.write('**K =** ',K)
            st.write('**GSP =** ',GSP)
            


elif sel=='BPLQC (Passe-bande de Rauch (de type C), Q<2)':
    
    st.image('iBP-LQ-C.jpg')
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
        C4=st.number_input('**Choix de C4**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C4: ',C4,' Farads.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            if (1/(2*(qp*qp)))*((C11+C12)/C4)>=2 :
                
                C1=C11+C12
                P=((C1/(2*(qp*qp)*C4))-1)+m.sqrt((((C1/(2*(qp*qp)*C4))-1)*((C1/(2*(qp*qp)*C4))-1))-1)
                R2=1/(2*m.pi*fp*m.sqrt(P*C1*C4))
                R3=P*R2
                GSP=qp*m.sqrt(C1/(P*C4))
                K=C11*GSP/C1
                
                st.header('Données calculées:')
                st.write('**R2 =** ',R2,' Ohms.')
                st.write('**R3 =** ',R3,' Ohms.')
                st.write('**K =** ',K)
                st.write('**GSP =** ',GSP)
            
            else :
                
                st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que  **  $C11+C12>=4*Qp^2*C4$')



elif sel=='BPMQR (Passe-bande de Rauch (de type R), Q<10)':
    
    st.image('iBP-MQ-R.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C2=st.number_input('**Choix de C2**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C2: ',C2,' Farads.')
        C3=st.number_input('**Choix de C3**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C3: ',C3,' Farads.')
        k=st.number_input('**Choix de K**',min_value=0.00,value=0.50,step=None)
        st.write('Valeur de K: ',k)
        R6=st.number_input('**Choix de R6 (Optionnel)**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de R6: ',R6,' Ohms.')
        
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            P=(C2/C3)/(4*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C3/C2))-1)*(m.sqrt(1+12*qp*qp*(1+C3/C2))-1)
            R1=1/(2*m.pi*fp*m.sqrt(P*C2*C3))
            R4=P*R1
            
            if R6==0:
                R6=1e4
            
            R5=R6*(1/P*(1+C2/C3)-m.sqrt(C2/(P*C3))/qp)
            K0=qp*(1+R5/R6)*m.sqrt(P*C3/C2)
            GSP=(1+R5/R6)*K0
            
            if k==0:
                R11=R1
                R12=float('inf')
                K=K0
                
            elif K0-k<=0:
                R11=R1
                R12=float('inf')
                K=K0
            
            else:
                K=k
                R11=K0/K*R1
                R12=K0/(K0-K)*R1
                
            st.header('Données calculées:')
            st.write('**R11 =** ',R11,' Ohms.')
            st.write('**R12 =** ',R12,' Ohms.')
            st.write('**R4 =** ',R4,' Ohms.')
            st.write('**R5 =** ',R5,' Ohms.')
            st.write('**K =** ',K)
            st.write('**P =** ',P)
            st.write('**GSP =** ',GSP)



elif sel=='BPMQC (Passe-bande de Rauch (de type C), Q<10)':
    
    st.image('iBP-MQ-C.jpg')
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
        C4=st.number_input('**Choix de C4**',min_value=0.00,value=0.00000001,step=None,format='%0.10f')
        st.write('Valeur de C4: ',C4,' Farads.')
        R6=st.number_input('**Choix de R6 (Optionnel)**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de R6: ',R6,' Ohms.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            C1=C11+C12
            P=(C1/C4)/(36*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C4/C1))+1)*(m.sqrt(1+12*qp*qp*(1+C4/C1))+1)
            R2=1/(2*m.pi*fp*m.sqrt(P*C1*C4))
            R3=P*R2
            
            if R6==0:
                R6=1e4
            
            R5=R6*(C4/C1*(1+P)-m.sqrt(P*C4/C1)/qp)
            K=C11/C1*(1+R5/R6)*qp*m.sqrt(C1/(P*C4))
            GSP=qp*(1+R5/R6)*(1+R5/R6)*m.sqrt(C1/(P*C4))
                    
            st.header('Données calculées:')
            st.write('**R2 =** ',R2,' Ohms.')
            st.write('**R3 =** ',R3,' Ohms.')
            st.write('**R5 =** ',R5,' Ohms.')
            st.write('**P =** ',P)
            st.write('**K =** ',K)
            st.write('**GSP =** ',GSP)
            


elif sel=='Passe-bas de Flieghe (Q<30)':
    
    st.image('iLP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C=st.number_input('**Choix de C (=C1=C4)**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C: ',C,' Farads.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            R_optimal=1/(2*m.pi*fp*C)
            R_optimal=int(R_optimal)
            minval=R_optimal-10
            maxval=R_optimal+10
            Rd=st.slider("Choix de Rd=R2=R3=R6 proche de R optimale calculée sur base de fp et C.",minval,maxval,R_optimal)
            C1=C
            C4=C
            R2=Rd
            R3=Rd
            R6=Rd
            R1=qp*R_optimal
            R7=(R_optimal*R_optimal)/Rd       
            
            st.header('Données calculées:')
            st.write('**R1 =** ',R1,' Ohms.')
            st.write('**R2 =** ',R2,' Ohms.')
            st.write('**R3 =** ',R3,' Ohms.')
            st.write('**R6 =** ',R6,' Ohms.')
            st.write('**R7 =** ',R7,' Ohms.')
            st.write('**C1 =** ',C1,' Farads.')
            st.write('**C4 =** ',C4,' Farads.')
            


elif sel=='Passe-bande de Flieghe (Q<30)':
    
    st.image('iBP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C=st.number_input('**Choix de C (=C1=C4)**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C: ',C,' Farads.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            R_optimal=1/(2*m.pi*fp*C)
            R_optimal=int(R_optimal)
            minval=R_optimal-10
            maxval=R_optimal+10
            Rd=st.slider("Choix de Rd=R2=R3=R6 proche de R optimale calculée sur base de fp et C.",minval,maxval,R_optimal)
            C3=C
            C8=C
            R2=Rd
            R1=Rd
            R6=Rd
            R7=qp*R_optimal
            R4=(R_optimal*R_optimal)/Rd       
            
            st.header('Données calculées:')
            st.write('**R1 =** ',R1,' Ohms.')
            st.write('**R2 =** ',R2,' Ohms.')
            st.write('**R4 =** ',R4,' Ohms.')
            st.write('**R6 =** ',R6,' Ohms.')
            st.write('**R7 =** ',R7,' Ohms.')
            st.write('**C3 =** ',C3,' Farads.')
            st.write('**C8 =** ',C8,' Farads.')



elif sel=='Passe-haut de Flieghe (Q<30)':
    
    st.image('iHP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C=st.number_input('**Choix de C (=C1=C4)**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C: ',C,' Farads.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            R_optimal=1/(2*m.pi*fp*C)
            R_optimal=int(R_optimal)
            minval=R_optimal-10
            maxval=R_optimal+10
            Rd=st.slider("Choix de Rd=R2=R3=R6 proche de R optimale calculée sur base de fp et C.",minval,maxval,R_optimal)
            C3=C
            C7=C
            R2=Rd
            R1=Rd
            R6=Rd
            R8=qp*R_optimal
            R4=(R_optimal*R_optimal)/Rd       
            
            st.header('Données calculées:')
            st.write('**R1 =** ',R1,' Ohms.')
            st.write('**R2 =** ',R2,' Ohms.')
            st.write('**R4 =** ',R4,' Ohms.')
            st.write('**R6 =** ',R6,' Ohms.')
            st.write('**R8 =** ',R8,' Ohms.')
            st.write('**C3 =** ',C3,' Farads.')
            st.write('**C7 =** ',C7,' Farads.')



elif sel=='Réjecteur de fréquence de Flieghe (Q<30)':
    
    st.image('iHP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
    
        st.header("Entrée des paramètres du filtre")
        fz=st.number_input('**Choix de fz**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fz: ',fz,' Hertz.')
        fp=st.number_input('**Choix de fp**',min_value=0.00,value=1000.00,step=None)
        st.write('Valeur de fp: ',fp,' Hertz.')
        qp=st.number_input('**Choix de Qp**',min_value=0.00,value=1.00,step=None)
        st.write('Valeur de Qp: ',qp)
        C=st.number_input('**Choix de C (=C1=C4)**',min_value=0.00,value=0.00001,step=None,format='%0.10f')
        st.write('Valeur de C: ',C,' Farads.')
    
        if st.checkbox('**Valider les données**:+1:',key=2):
            
            R_optimal=1/(2*m.pi*fp*C)
            R_optimal=int(R_optimal)
            minval=R_optimal-10
            maxval=R_optimal+10
            Rd=st.slider("Choix de Rd=R2=R3=R6 proche de R optimale calculée sur base de fp et C.",minval,maxval,R_optimal)
            C2=C
            C7=C
            R3=Rd
            R1=Rd
            R8=qp*R_optimal
            if fz==fp:
                st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que fz soit différent de fp** ')
                
            if fz<fp:
                R4=R8*(1-((fz/fp)*(fz/fp)))
                R5=(R_optimal*R_optimal)/R4      
                
                st.header('Données calculées:')
                st.write('**R1 =** ',R1,' Ohms.')
                st.write('**R3 =** ',R3,' Ohms.')
                st.write('**R4 =** ',R4,' Ohms.')
                st.write('**R5 =** ',R5,' Ohms.')
                st.write('**R8 =** ',R8,' Ohms.')
                st.write('**C2 =** ',C2,' Farads.')
                st.write('**C7 =** ',C7,' Farads.')
                
            if fz>fp:
                R4=R8*(((fz/fp)*(fz/fp))-1)
                R5=(R_optimal*R_optimal)/R4      
                
                st.header('Données calculées:')
                st.write('**R1 =** ',R1,' Ohms.')
                st.write('**R3 =** ',R3,' Ohms.')
                st.write('**R4 =** ',R4,' Ohms.')
                st.write('**R5 =** ',R5,' Ohms.')
                st.write('**R8 =** ',R8,' Ohms.')
                st.write('**C2 =** ',C2,' Farads.')
                st.write('**C7 =** ',C7,' Farads.')
            
#draw_repfreq("bite",[1], [1], 0, 1)

            


