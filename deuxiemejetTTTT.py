# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 18:33:13 2023

@author: Jean Bériot
Faire NUM avec les wp recalculer
Pouvoir modifier les données reçu
pouvoir en plus mettre un % erreur
choix pour théorie et pratique
"""
from ProjUtilsSF import *
import streamlit as st
import math as m

st.title("Synthèse de filtres RCAO")

st.header("Choix du filtre")
sel=st.selectbox("Avec quel type de filtre désirez-vous travailler?",['LPLQ (Passe-bas de Sallen-Key, Q<2)','HPLQ (Passe-haut de Sallen-Key, Q<2)','LPMQ (Passe-bas de Sallen-Key, Q<5)','HPMQ (Passe-haut de Sallen-Key, Q<5)',
                                                                      'BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)','BPLQR (Passe-bande de Rauch (de type R), Q<2)','BPLQC (Passe-bande de Rauch (de type C), Q<2)',
                                                                      'BPMQR (Passe-bande de Rauch (de type R), Q<10)','BPMQC (Passe-bande de Rauch (de type C), Q<10)','Passe-bas de Flieghe (Q<30)','Passe-bande de Flieghe (Q<30)',
                                                                      'Passe-haut de Flieghe (Q<30)','Réjecteur de fréquence de Flieghe (Q<30)','Passe-Bas de Tow-Thomas (Q<100)'])

if sel =='LPLQ (Passe-bas de Sallen-Key, Q<2)':
   st.image('iLP-LQ.jpg')
   if st.checkbox('**Choisir ce filtre**:+1:',key=1):
      
       [fp,qp,C2,C4,k]=Param(['fp','Qp','C2','C4','K (<1)'],2,1)
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
               
           N,D=getLP_ND(fp, qp, k)
           Result(['R11','R12','R3','GSP'], [R11,R12,R3,GSP],N,D)   
          
      
elif sel =='HPLQ (Passe-haut de Sallen-Key, Q<2)':
   
    st.image('iHP-LQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C11,C12,C3]=Param(['fp','Qp','C11','C12','C3'],2)

        C1=(C11+C12)
        P=((qp*qp)*(2+(C3/C1)+(C1/C3)))
        R2=(1/(2*m.pi*fp*m.sqrt(P*C1*C3)))
        R4=(P*R2)
        GSP=(qp*m.sqrt(P*C3/C1))
        K=(C11/C1)
        N,D=getHP_ND(fp, qp, K)
        Result(['C1','R2','R4','GSP','K'], [C1,R2,R4,GSP,K],N,D) 
                            
    
elif sel =='LPMQ (Passe-bas de Sallen-Key, Q<5)':
   
    st.image('iLP-MQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C2,C4,k,R5]=Param(['fp','Qp','C2','C4','K','R5 (Optionnel)'],5)
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
            
        N,D=getLP_ND(fp, qp, K)
        Result(['R11','R12','R3','R6','GSP','K'], [R11,R12,R3,R6,GSP,K],N,D) 
                           
    
elif sel =='HPMQ (Passe-haut de Sallen-Key, Q<5)':
   
    st.image('iHP-MQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C11,C12,C3,R5]=Param(['fp','Qp','C11','C12','C3','R5 (Optionnel)'],5)

        C1=C11+C12
        P=(C1/C3)/(4*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)
    
        R2=1/(2*m.pi*fp*m.sqrt(P*C1*C3))
        R4=P*R2
        
        if R5==0:
            R5=1e4
        
        R6=R5*(1/P*(1+C1/C3)-m.sqrt(C1/(P*C3))/qp)
        K=C11/C1*(1+R6/R5)
        GSP=qp*(1+R6/R5)*(1+R6/R5)*m.sqrt((P*C3)/C1)
                                          
        N,D=getHP_ND(fp, qp, K)
        Result(['R2','R4','R6','GSP'], [R2,R4,R6,GSP],N,D)
        

elif sel =='BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)':

    st.image('iBR-LPN-HPN-MQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fz,fp,qp,C1,C2,C3,C4,R9]=Param(['fz','fp','Qp','C1','C2','C3','C4','R9 (Optionnel)'],5)
        
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
            if fz==fp or fz>fp:
                st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que fz soit inférieur à fp** ')
                
            if fz<fp:    
                N,D=getBR_ND(fp, qp, K, fz)
                Result(['R5','R6','R7','R8','R10','K','GSP'], [R5,R6,R7,R8,R10,K,GSP],N,D)

elif sel=='BPLQR (Passe-bande de Rauch (de type R), Q<2)':
    
    st.image('iBP-LQ-R.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C2,C3,k]=Param(['fp','Qp','C2','C3','K'],2)
        
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
        N,D=getPB_ND(fp, qp, K)
        Result(['R11','R12','R4','K','GSP'], [R11,R12,R4,K,GSP],N,D)

elif sel=='BPLQC (Passe-bande de Rauch (de type C), Q<2)':
    
    st.image('iBP-LQ-C.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C11,C12,C4]=Param(['fp','Qp','C11','C12','C4'],2)
        
        if (1/(2*(qp*qp)))*((C11+C12)/C4)>=2 :
            C1=C11+C12
            P=((C1/(2*(qp*qp)*C4))-1)+m.sqrt((((C1/(2*(qp*qp)*C4))-1)*((C1/(2*(qp*qp)*C4))-1))-1)
            R2=1/(2*m.pi*fp*m.sqrt(P*C1*C4))
            R3=P*R2
            GSP=qp*m.sqrt(C1/(P*C4))
            K=C11*GSP/C1

            N,D=getPB_ND(fp, qp, K)
            Result(['R2','R3','K','GSP'], [R2,R3,K,GSP],N,D)
        else :            
            st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que  **  $C11+C12>=4*Qp^2*C4$')

elif sel=='BPMQR (Passe-bande de Rauch (de type R), Q<10)':
    
    st.image('iBP-MQ-R.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        
        [fp,qp,C2,C3,k,R6]=Param(['fp','Qp','C2','C3','K','R6  (Optionnel)'],10)

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
            
        N,D=getPB_ND(fp, qp, K)
        Result(['R11','R12','R4','R5','K','P','GSP'], [R11,R12,R4,R5,k,P,GSP],N,D)

elif sel=='BPMQC (Passe-bande de Rauch (de type C), Q<10)':
    
    st.image('iBP-MQ-C.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C11,C12,C4,R6]=Param(['fp','Qp','C11','C12','C4','R6  (Optionnel)'],10)
        
        C1=C11+C12
        P=(C1/C4)/(36*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C4/C1))+1)*(m.sqrt(1+12*qp*qp*(1+C4/C1))+1)
        R2=1/(2*m.pi*fp*m.sqrt(P*C1*C4))
        R3=P*R2
        if R6==0:
            R6=1e4
        R5=R6*(C4/C1*(1+P)-m.sqrt(P*C4/C1)/qp)
        K=C11/C1*(1+R5/R6)*qp*m.sqrt(C1/(P*C4))
        GSP=qp*(1+R5/R6)*(1+R5/R6)*m.sqrt(C1/(P*C4))
            
        N,D=getPB_ND(fp, qp, K)
        Result(['R2','R3','R5','K','P','GSP'], [R2,R3,R5,K,P,GSP],N,D)
        
elif sel=='Passe-bas de Flieghe (Q<30)':
    
    st.image('iLP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C]=Param(['fp','Qp','C'],30)
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
        k=fp*R1*C1    
        N,D=getLP_ND(fp, qp, k)
        Result(['R1','R2','R3','R6','R7','C1','C4'], [R1,R2,R3,R6,R7,C1,C4],N,D)

elif sel=='Passe-bande de Flieghe (Q<30)':
    
    st.image('iBP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        
        [fp,qp,C]=Param(['fp','Qp','C'],30)
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
        K=1+R2/R6
        N,D=getPB_ND(fp, qp, K)
        Result(['R1','R2','R4','R6','R7','C3','C8'], [R1,R2,R4,R6,R7,C3,C8],N,D)      


elif sel=='Passe-haut de Flieghe (Q<30)':
    
    st.image('iHP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        [fp,qp,C]=Param(['fp','Qp','C'],30)
 
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
        K=1+R2/R6   
        
        N,D=getHP_ND(fp, qp, K)
        Result(['R1','R2','R4','R6','R8','C3','C7'], [R1,R2,R4,R6,R8,C3,C7],N,D)

elif sel=='Réjecteur de fréquence de Flieghe (Q<30)':
    
    st.image('iHP-HQ.jpg')
    if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        
        [fz,fp,qp,C]=Param(['fz','fp','Qp','C'],30)
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
        if fz==fp or fz>fp:
            st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que fz soit inférieur à fp** ')
            
        if fz<fp:
            R4=R8*(1-((fz/fp)*(fz/fp)))
            R5=(R_optimal*R_optimal)/R4 
            fpr=2*m.pi*m.sqrt(R3/(R1*R4*R5*C2*C7))
            qpr=(fpr*C7*R8)/(2*m.pi)
            fzr=(fpr/(2*m.pi))*m.sqrt(1+R4/R8)
            N,D=getBR_ND(fp, qp, 1, fz)
            n,d=getBR_ND(fpr, qpr, 1, fzr)
            Result(['R1','R3','R4','R5','R8','C2','C7'], [R1,R3,R4,R5,R8,C2,C7],N,D,n,d)
        
# elif sel=='Passe-Bas de Tow-Thomas (Q<100)':
    
#     st.image('ane.png')
#     if st.checkbox('**Choisir ce filtre**:+1:',key=1):
        
#         [fp,qp,C9,C10]=Param(['fp','Qp','C9','C10'],100)
        
#         R_optimal=1/(2*m.pi*fp*C9)
#         R_optimal=int(R_optimal)
#         minval=R_optimal-10
#         maxval=R_optimal+10
#         Rd=st.slider("Choix de Rd=R2=R3=R7 proche de R optimale calculée sur base de fp et C.",minval,maxval,R_optimal)
#         R2=Rd
#         R3=Rd
#         R7=Rd
#         R=Rd**3
#         wp=m.pi*2*fp
#         R8=(wp**2)*R*C10*C9
#         R1=qp*m.sqrt((R*C9*C10)/(R8))
        
#         R4=float('inf')
#         R6=float('inf')
#         R5=(R6*R8)/R2
#         K=-R8/R6
#         fpr=2*m.pi*m.sqrt(R8/(R2*R3*R7*C9*C10))
#         qpr=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
#         N,D=getLP_ND(fp, qp, 1)
#         n,d=getLP_ND(fpr, qpr, K)
#         Result(['R1','R2','R3','R4','R5','R6','R7','R8'], [R1,R2,R3,R4,R5,R6,R7,R8],N,D,n,d)


            


