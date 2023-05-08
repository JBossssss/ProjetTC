

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 18:33:13 2023
@author: Jean Bériot
 
"""
from ProjUtilsV9 import *
import streamlit as st
import math as m


def filter(p):
    st.header("Choix du filtre")
    sel=st.selectbox("Avec quel type de filtre désirez-vous travailler?",['LPLQ (Passe-bas de Sallen-Key, Q<2)','HPLQ (Passe-haut de Sallen-Key, Q<2)','LPMQ (Passe-bas de Sallen-Key, Q<5)','HPMQ (Passe-haut de Sallen-Key, Q<5)',
                                                                      'BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)','BPLQR (Passe-bande de Rauch (de type R), Q<2)','BPLQC (Passe-bande de Rauch (de type C), Q<2)',
                                                                      'BPMQR (Passe-bande de Rauch (de type R), Q<10)','BPMQC (Passe-bande de Rauch (de type C), Q<10)','Passe-bas de Flieghe (Q<30)','Passe-bande de Flieghe (Q<30)',
                                                                      'Passe-haut de Flieghe (Q<30)','Réjecteur de fréquence de Flieghe (Q<30)','Cellule Universelle de Tow-Thomas (Q<100)'],key=p)
    name=[]
    data=[]
    image=''
    plot='iLP-MQ.jpg'
    if sel =='LPLQ (Passe-bas de Sallen-Key, Q<2)':
       image= 'iLP-LQ.jpg'
       st.image(image,width=800)
       if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
      
           [fp,qp,C2,C4,k]=Param(['fp','Qp','C2','C4','K (<1)'],2,p,1)
           if (1/(2*qp*qp)) * C2/C4 <=2:
               st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que**  $C2>=4*Qp^2*C4$')
                   
           else :
               P = ( (1/(2*qp*qp)) * C2/C4 -1) + m.sqrt( ((1/(2*qp*qp)) * C2/C4 -1)*((1/(2*qp*qp)) * C2/C4 -1) -1 )
               R1 = 1/(2*m.pi*fp*m.sqrt(P*C2*C4))
               R3=P*R1
               GSP=qp*m.sqrt(C2/(P*C4))
                   
               if k==0.00:
                   R11=R1
                   R12=float('inf')
                   k=1
                
               else :
                   R11=R1/k
                   R12=R1/(1-k)
        

                   [R11m,R12m,R3m,C2m,C4m,GSPm]= Result(['R11','R12','R3','C2','C4','GSP'], [R11,R12,R3,C2,C4,GSP],p)
                   [C2m,C4m],[R11m,R12m,R3m]=standardisation(['C2','C4'], [C2m,C4m],['R11','R12','R3'], [R11m,R12m,R3m],p)                   
                   Km=R12m/(R11m+R12m)
                   R1m=(R11m*R12m)/(R11m+R12m)
                   wp=m.sqrt(1/(R1m*C2m*R3m*C4m))
                   fpr=wp/(2*m.pi)
                   qpr=(m.sqrt((R3m*C2m)/(R1m*C4m)))/(1+R3m/R1m)
                   n,d=getLP_ND(fpr, qpr, Km)    
                   N,D=getLP_ND(fp, qp, k)
                   plot=Aff(N, D, n, d,p)
                   
                   name=['fp','Qp','R11','R12','R3','C2','C4','GSP']
                   data=[fpr,qpr,R11m,R12m,R3m,C2m,C4m,GSPm]
                   
                   st.header("Analyse de sensibilité de Wp et Qp")
                   sensi=st.expander('Afficher la sensibilité')
                   d1,d2=sensi.columns([1,1])
                   var=1
                   with d1:
                       st.write("S(Qp):") 
                       fprs=fp
                       qprs=1.01*qp
                       ns,ds=getLP_ND(fprs, qprs, k)
                       draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                       
                   with d2:
                       
                       st.write("S(Wp):")
                       fprs=fp*1.01
                       qprs=qp
                       ns,ds=getLP_ND(fprs, qprs, k)
                       draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                       
                       
                       
                   st.header("Analyse de sensibilité des capacités")
                   sensi=st.expander('Afficher la sensibilité')
                   d1,d2=sensi.columns([1,1])
                   var=1
                   with d1:

                       st.write("S(C2):")
                       C2s=1.01*C2
                       wps=m.sqrt(1/(R1*C2s*R3*C4))
                       fprs=wps/(2*m.pi)
                       qprs=(m.sqrt((R3*C2s)/(R1*C4)))/(1+R3/R1)
                       ns,ds=getLP_ND(fprs, qprs, k)
                       draw_sensi('S(C2)',N,D,ns,ds,fp,var)
                   with d2:
                       
                       st.write("S(C4):")
                       C4s=1.01*C4
                       wps=m.sqrt(1/(R1*C2*R3*C4s))
                       fprs=wps/(2*m.pi)
                       qprs=(m.sqrt((R3*C2)/(R1*C4s)))/(1+R3/R1)
                       ns,ds=getLP_ND(fprs, qprs, k)
                       draw_sensi('S(C4)',N,D,ns,ds,fp,var)
                       
                
                   st.header("Analyse de sensibilité des résistances")
                   sensi=st.expander('Afficher la sensibilité')
                   d1,d2,d3=sensi.columns([1,1,1])
                   var=1
                   with d1:

                       st.write("S(R11):")
                       R11s=1.01*R11
                       Ks=R12/(R11s+R12)
                       R1s=R11s*Ks
                       wps=m.sqrt(1/(R1s*C2*R3*C4))
                       fprs=wps/(2*m.pi)
                       qprs=(m.sqrt((R3*C2)/(R1s*C4)))/(1+R3/R1s)
                       ns,ds=getLP_ND(fprs, qprs, Ks)
                       draw_sensi('S(R11)',N,D,ns,ds,fp,var)
                   with d2:
                       
                       st.write("S(R12):")
                       R12s=1.01*R12
                       Ks=R12s/(R11+R12s)
                       R1s=(R11*R12s)/(R11+R12s)
                       wps=m.sqrt(1/(R1s*C2*R3*C4))
                       fprs=wps/(2*m.pi)
                       qprs=(m.sqrt((R3*C2)/(R1s*C4)))/(1+R3/R1s)
                       ns,ds=getLP_ND(fprs, qprs, Ks)
                       draw_sensi('S(R12)',N,D,ns,ds,fp,var)
                   with d3:
                       
                       st.write("S(R3):")
                       R3s=1.01*R3
                       wps=m.sqrt(1/(R1*C2*R3s*C4))
                       fprs=wps/(2*m.pi)
                       qprs=(m.sqrt((R3s*C2)/(R1*C4)))/(1+R3s/R1)
                       ns,ds=getLP_ND(fprs, qprs, k)
                       draw_sensi('S(R3)',N,D,ns,ds,fp,var)

                    
                       
    elif sel =='HPLQ (Passe-haut de Sallen-Key, Q<2)':
        image='iHP-LQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C11,C12,C3]=Param(['fp','Qp','C11','C12','C3'],2,p)
    
            C1=(C11+C12)
            P=((qp*qp)*(2+(C3/C1)+(C1/C3)))
            R2=(1/(2*m.pi*fp*m.sqrt(P*C1*C3)))
            R4=(P*R2)
            GSP=(qp*m.sqrt(P*C3/C1))
            K=(C11/C1)
    
            [C11m,C12m,C3m,R2m,R4m,GSPm,Km]=Result(['C11','C12','C3','R2','R4','GSP','K'], [C11,C12,C3,R2,R4,GSP,K],p)
            [C11m,C12m,C3m],[R2m,R4m]=standardisation(['C11','C12','C3'], [C11m,C12m,C3m], ['R2','R4'], [R2m,R4m],p)
            Km=C11m/(C11m+C12m)
            C1m=C11m+C12m
            wp=m.sqrt(1/(R2m*C1m*R4m*C3m))
            fpr=wp/(2*m.pi)
            qpr=(m.sqrt((R4m*C1m)/(R2m*C3m)))/(1+C1m/C3m)     
            n,d=getHP_ND(fpr, qpr, Km) 
            N,D=getHP_ND(fp, qp, K)
            plot=Aff(N, D, n, d,p)
            
            name=['fp','Qp','C11','C12','C3','R2','R4','GSP']
            data=[fpr,qpr,C11m,C12m,C3m,R2m,R4m,GSPm]
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                
            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                
                
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d1:
                
                st.write("S(C12):")
                C12s=1.01*C12
                C1s=C11+C12s
                Ks=C11/(C11+C12s)
                wps=m.sqrt(1/(C1s*R2*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1s)/(R2*C3)))/(1+C1s/C3) 
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(C12)',N,D,ns,ds,fp,var)
                
            with d2:
                
                st.write("S(C3):")
                C3s=1.01*C3
                wps=m.sqrt(1/(C1*R2*C3s*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1)/(R2*C3s)))/(1+C1/C3s) 
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(C3)',N,D,ns,ds,fp,var)
                
                
            with d3:
                st.write("S(C11):")
                C11s=1.01*C11
                C1s=C11s+C12
                Ks=C11s/(C11s+C12)
                wps=m.sqrt(1/(C1s*R2*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1s)/(R2*C3)))/(1+C1s/C3) 
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(C11)',N,D,ns,ds,fp,var)
            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                
                st.write("S(R2):")
                R2s=1.01*R2
                wps=m.sqrt(1/(C1*R2s*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1)/(R2s*C3)))/(1+C1/C3) 
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                
                
            with d2:
                st.write("S(R4):")
                R4s=1.01*R4
                wps=m.sqrt(1/(C1*R2*C3*R4s))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4s*C1)/(R2*C3)))/(1+C1/C3) 
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                
                
                
            
                            
                             
    elif sel =='LPMQ (Passe-bas de Sallen-Key, Q<5)':
        image= 'iLP-MQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C2,C4,k,R5]=Param(['fp','Qp','C2','C4','K','R5 (Optionnel)'],5,p)
            P=(C2/C4)/(36*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C4/C2))+1)*(m.sqrt(1+12*qp*qp*(1+C4/C2))+1)
            R1=1/(2*m.pi*fp*m.sqrt(P*C2*C4))
            R3=P*R1
            if R5==0:
                R5=1e4
          
            R6=R5*(C4/C2*(1+P)-m.sqrt(P*C4/C2)/qp)
            if R6<=0:
                st.markdown(":warning: **La valeur de R6 est inférieure à 0. Pour éviter cela, veuillez augmenter C4 ou diminuer C2.**")
                st.write("R6 calculée =",R6,"Ohms")
            else :
                
                K0=1+R6/R5
                GSP=qp*K0*K0*m.sqrt(C2/(P*C4))
                
                if k==0.00 :
                    R11=R1
                    R12=1e90
                    K=K0
                elif K0-k<=0.00:
                    R11=R1
                    R12=1e90
                    K=K0
                else:
                    K=k
                    R11=K0/K*R1
                    R12=K0/(K0-K)*R1
                [R11m,R12m,R3m,R5m,R6m,C2m,C4m,GSPm,Km]=Result(['R11','R12','R3','R5','R6','C2','C4','GSP','K'], [R11,R12,R3,R5,R6,C2,C4,GSP,K],p+20)
                [C2m,C4m,R5m], [R11m,R12m,R3m,R6m]=standardisation(['C2','C4','R5'], [C2m,C4m,R5m], ['R11','R12','R3','R6'], [R11m,R12m,R3m,R6m],p)
                R1m=(R11m*R12m)/(R11m+R12m)
                Km=(1+R6m/R5m)*R12m/(R11m+R12m)
                wp=m.sqrt(1/(R1m*C2m*R3m*C4m))
                fpr=wp/(2*m.pi)
                qpr=(m.sqrt((R3m*C2m)/(R1m*C4m)))/(1+R3m/R1m-R6m*C2m/(R5m*C4m))
                n,d=getLP_ND(fpr, qpr, Km)     
                N,D=getLP_ND(fp, qp, K)
                plot=Aff(N, D, n, d,p)
                
                name=['fp','Qp','R11','R12','R3','R5','R6','C2','C4','GSP']
                data=[fpr,qpr,R11m,R12m,R3m,R5m,R6m,C2m,C4m,GSPm]
                
                st.header("Analyse de sensibilité de Wp et Qp")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d1:
                    st.write("S(Qp):") 
                    fprs=fp
                    qprs=1.01*qp
                    ns,ds=getLP_ND(fprs, qprs, K)
                    draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
        
                with d2:
                    st.write("S(Wp):")
                    fprs=fp*1.01
                    qprs=qp
                    ns,ds=getLP_ND(fprs, qprs, K)
                    draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                    
                st.header("Analyse de sensibilité des capacités")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d1:
                    st.write("S(C2):")
                    C2s=1.01*C2
                    wps=m.sqrt(1/(R1*C2s*R3*C4))
                    fprs=wps/(2*m.pi)
                    qprs=(m.sqrt((R3*C2s)/(R1*C4)))/(1+R3/R1-R6*C2s/(R5*C4))
                    ns,ds=getLP_ND(fprs, qprs, K)
                    draw_sensi('S(C2)',N,D,ns,ds,fp,var)
                    
        
                with d2:
                    st.write("S(C4):")
                    C4s=1.01*C4
                    wps=m.sqrt(1/(R1*C2*R3*C4s))
                    fprs=wps/(2*m.pi)
                    qprs=(m.sqrt((R3*C2)/(R1*C4s)))/(1+R3/R1-R6*C2/(R5*C4s))
                    ns,ds=getLP_ND(fprs, qprs, K)
                    draw_sensi('S(C4)',N,D,ns,ds,fp,var)
                    

                
                st.header("Analyse de sensibilité des résistances")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2,d3=sensi.columns([1,1,1])
                var=1
                with d1:
                    st.write("S(R11):")
                    R11s=1.01*R11
                    R1s=(R11s*R12)/(R11s+R12)
                    Ks=(1+R6/R5)*R12/(R11s+R12)
                    wps=m.sqrt(1/(R1s*C2*R3*C4))
                    fprs=wps/(2*m.pi)
                    qprs=(m.sqrt((R3*C2)/(R1s*C4)))/(1+R3/R1s-R6*C2/(R5*C4))
                    ns,ds=getLP_ND(fprs, qprs, Ks)
                    draw_sensi('S(R11)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R5):")
                    R5s=1.01*R5
                    Ks=(1+R6/R5s)*R12/(R11+R12)
                    wps=m.sqrt(1/(R1*C2*R3*C4))
                    fprs=wps/(2*m.pi)
                    qprs=(m.sqrt((R3*C2)/(R1*C4)))/(1+R3/R1-R6*C2/(R5s*C4))
                    ns,ds=getLP_ND(fprs, qprs, Ks)
                    draw_sensi('S(R5)',N,D,ns,ds,fp,var)
        
                with d2:
                    
                    st.write("S(R12):")
                    R12s=1.01*R12
                    R1s=(R11*R12s)/(R11+R12s)
                    Ks=(1+R6/R5)*R12/(R11+R12s)
                    wps=m.sqrt(1/(R1s*C2*R3*C4))
                    fprs=wps/(2*m.pi)
                    qprs=(m.sqrt((R3*C2)/(R1s*C4)))/(1+R3/R1s-R6*C2/(R5*C4))
                    ns,ds=getLP_ND(fprs, qprs, Ks)
                    draw_sensi('S(R12)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R6):")
                    R6s=1.01*R6
                    Ks=(1+R6s/R5)*R12/(R11+R12)
                    wps=m.sqrt(1/(R1*C2*R3*C4))
                    fprs=wps/(2*m.pi)
                    qprs=(m.sqrt((R3*C2)/(R1*C4)))/(1+R3/R1-R6s*C2/(R5*C4))
                    ns,ds=getLP_ND(fprs, qprs, Ks)
                    draw_sensi('S(R6)',N,D,ns,ds,fp,var)
        
                with d3:
                    
                    st.write("S(R3):")
                    R3s=1.01*R3
                    wps=m.sqrt(1/(R1*C2*R3s*C4))
                    fprs=wps/(2*m.pi)
                    qprs=(m.sqrt((R3s*C2)/(R1*C4)))/(1+R3s/R1-R6*C2/(R5*C4))
                    ns,ds=getLP_ND(fprs, qprs, k)
                    draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                    
                    
                 
    elif sel =='HPMQ (Passe-haut de Sallen-Key, Q<5)':
        image='iHP-MQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C11,C12,C3,R5]=Param(['fp','Qp','C11','C12','C3','R5 (Optionnel)'],5,p)
        
            C1=C11+C12
            P=(C1/C3)/(4*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)*(m.sqrt(1+12*qp*qp*(1+C3/C1))-1)
        
            R2=1/(2*m.pi*fp*m.sqrt(P*C1*C3))
            R4=P*R2
            
            if R5==0:
                R5=1e4
            
            R6=R5*(1/P*(1+C1/C3)-m.sqrt(C1/(P*C3))/qp)
            K=C11/C1*(1+R6/R5)
            GSP=qp*(1+R6/R5)*(1+R6/R5)*m.sqrt((P*C3)/C1) 
        
            [R2m,R4m,R5m,R6m,C11m,C12m,C3m,GSPm]=Result(['R2','R4','R5','R6','C11','C12','C3','GSP'], [R2,R4,R5,R6,C11,C12,C3,GSP],p+40)
            [C11m,C12m,C3m,R5m],[R2m,R4m,R6m]=standardisation(['C11','C12','C3','R5'], [C11m,C12m,C3m,R5m], ['R2','R4','R6'], [R2m,R4m,R6m],p+40)
            C1m=C11m+C12m
            wp=m.sqrt(1/(R2m*C1m*R4m*C3m))
            fpr=wp/(2*m.pi)
            qpr=(m.sqrt((R4m*C1m)/(R2m*C3m)))/(1+C1m/C3m-R4m*R6m/(R5m*R2m))
            Km=(C11m/(C11m+C12m))*(1+R6m/R5m)
            n,d=getHP_ND(fpr, qpr, Km)                                     
            N,D=getHP_ND(fp, qp, K)
            plot=Aff(N, D, n, d,p)
            
            name=['fp','Qp','R2','R4','R5','R6','C11','C12','C3','GSP']
            data=[fpr,qpr,R2m,R4m,R5m,R6m,C11m,C12m,C3m,GSPm]
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                
            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)

                
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d2:
                
                st.write("S(C12):")
                C12s=1.01*C12
                C1s=C11+C12s
                Ks=(1+R6/R5)*C11/(C11+C12s)
                wps=m.sqrt(1/(C1s*R2*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1s)/(R2*C3)))/(1+C1s/C3-R4*R6/(R5*R2)) 
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(C12)',N,D,ns,ds,fp,var)
                
            with d3:
                
                st.write("S(C3):")
                C3s=1.01*C3
                wps=m.sqrt(1/(C1*R2*C3s*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1)/(R2*C3s)))/(1+C1/C3s-R4*R6/(R5*R2))
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(C3)',N,D,ns,ds,fp,var)
                
                
            with d1:
                st.write("S(C11):")
                C11s=1.01*C11
                C1s=C11s+C12
                Ks=(1+R6/R5)*C11s/(C11s+C12)
                wps=m.sqrt(1/(C1s*R2*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1s)/(R2*C3)))/(1+C1s/C3-R4*R6/(R5*R2))
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(C11)',N,D,ns,ds,fp,var)

            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d2:

                
                st.write("S(R4):")
                R4s=1.01*R4
                wps=m.sqrt(1/(C1*R2*C3*R4s))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4s*C1)/(R2*C3)))/(1+C1/C3-R4s*R6/(R5*R2))
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                
            with d3:

                
                st.write("S(R5):")
                R5s=1.01*R5
                Ks=(1+R6/R5s)*C11/(C11+C12)
                wps=m.sqrt(1/(C1*R2*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1)/(R2*C3)))/(1+C1/C3-R4*R6/(R5s*R2))
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                
                
            with d1:
                
                st.write("S(R2):")
                R2s=1.01*R2
                wps=m.sqrt(1/(C1*R2s*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1)/(R2s*C3)))/(1+C1/C3-R4*R6/(R5*R2s))
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                
                st.write("S(R6):")
                R6s=1.01*R6
                Ks=(1+R6s/R5)*C11/(C11+C12)
                wps=m.sqrt(1/(C1*R2*C3*R4))
                fprs=wps/(2*m.pi)
                qprs=(m.sqrt((R4*C1)/(R2*C3)))/(1+C1/C3-R4*R6s/(R5*R2))
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(R5)',N,D,ns,ds,fp,var)
    
    elif sel =='BR-LPN-HPN-MQ (Réjecteur de fréquence de Sallen-Key (double T), Q<5)':
        image='iBR-LPN-HPN-MQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fz,fp,qp,C1,C2,C3,C4,R9]=Param(['fz','fp','Qp','C1','C2','C3','C4','R9 (Optionnel)'],5,p)
            
            if fz==fp:
                st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que fz soit différente de fp**')
                
            else:
                
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
                    
                    R10=R9*q_circ*((1/(R8*CS*2*m.pi*fz))+(RS*CS*2*m.pi*fz)-((1+(C4/CS))*(fp/fz)/qp))
                    GSP=qp*((1+(R10/R9))*(1+(R10/R9)))*((m.sqrt(R5*C3/(R6*CS))+m.sqrt(RS*C2/(R7*C1)))/((1+(C4/CS))*(fp/fz)))
                    K=(1+(R10/R9))/(1+(C4/CS))
                    
                    if R10<=0.00:
                        st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que**  $R10>=0$')
                        st.write('Or, R10=',R10,'Ohms.')
                        st.markdown('**Note**: Il conviendra donc de : ')
                        st.write('- Diminuer la valeur de C3')
                        st.write('- Augmenter la valeur de Qp')
                        st.write('- Augmenter la valeur de C1 ou C2')
                        
                    else :    
                        [R5m,R6m,R7m,R8m,R9m,R10m,C1m,C2m,C3m,C4m,Km,GSPm]=Result(['R5','R6','R7','R8','R9','C1','C2','C3','C4','R10','K','GSP'], [R5,R6,R7,R8,R9,R10,C1,C2,C3,C4,K,GSP],p+60)
                        [C1m,C2m,C3m,C4m,R9m],[R5m,R6m,R7m,R8m,R10m]=standardisation(['C1','C2','C3','C4','R9'],  [C1m,C2m,C3m,C4m,R9m], ['R5','R6','R7','R8','R10'], [R5m,R6m,R7m,R8m,R10m],p+60)
                        CSm=(C1m*C2m)/(C1m+C2m)
                        RSm=R5m+R6m
                        Km=(1+(R10m/R9m))/(1+(C4m/CSm))
                        wz=m.sqrt(1/(R5m*R6m*CSm*C3m))
                        wp=wz*m.sqrt((1+RSm/R8m)/(1+C4m/CSm))
                        Qprimem=1/(2*m.sqrt((1+C2m/C1m)*(1+C2m/C3m)))
                        qpr=Qprimem*((1+C4m/CSm)*wp/wz)/(Qprimem*(1/(R8m*CSm*wz)+RSm*CSm*wz)-R10m/R9m)
                        fpr=wp/(2*m.pi)
                        fzr=wz/(2*m.pi)
                        n,d=getBR_ND(fpr, qpr, Km, fzr)
                        N,D=getBR_ND(fp, qp, K, fz)
                        plot=Aff(N, D,n,d,p)
                        
                        name=['fp','Qp','R5','R6','R7','R8','R9','C1','C2','C3','C4','R10','K','GSP']
                        data=[fpr,qpr,R5m,R6m,R7m,R8m,R9m,R10m,C1m,C2m,C3m,C4m,Km,GSPm]
                        
                        st.header("Analyse de sensibilité de Wp, Wz et Qp")
                        sensi=st.expander('Afficher la sensibilité')
                        d1,d2,d3=sensi.columns([1,1,1])
                        var=1
                        with d1:
                            st.write("S(Qp):") 
                            qprs=1.01*qp
                            ns,ds=getBR_ND(fp, qprs, K,fz)
                            draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                            
                            
                            
                        with d2:
                            st.write("S(Wp):")
                            fprs=fp*1.01
                            ns ,ds=getBR_ND(fprs, qp, K,fz)
                            draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                            
                            
                        with d3:
                            st.write("S(Wz):")
                            fzrs=fz*1.01
                            ns,ds=getBR_ND(fp, qp, K,fzrs)
                            draw_sensi('S(Wz)',N,D,ns,ds,fp,var)

                            
                        st.header("Analyse de sensibilité des capacités")
                        sensi=st.expander('Afficher la sensibilité')
                        d1,d2,d3=sensi.columns([1,1,1])
                        var=1
                        with d1:

                            
                            st.write("S(C1):")
                            C1s=1.01*C1
                            CSs=(C1s*C2)/(C1s+C2)
                            Ks=(1+(R10/R9))/(1+(C4/CSs))
                            wzs=m.sqrt(1/(R5*R6*CSs*C3))
                            wps=wzs*m.sqrt((1+RS/R8)/(1+C4/CSs))
                            Qprimes=1/(2*m.sqrt((1+C2/C1s)*(1+C2/C3)))
                            qprs=Qprimes*((1+C4/CSs)*wps/wzs)/(Qprimes*(1/(R8*CSs*wzs)+RS*CSs*wzs)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wzs/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, Ks,fzrs)
                            draw_sensi('S(C1)',N,D,ns,ds,fp,var)
                            
                            st.write("S(C4):")
                            C4s=1.01*C4
                            Ks=(1+(R10/R9))/(1+(C4s/CS))
                            wps=wz*m.sqrt((1+RS/R8)/(1+C4s/CS))
                            qprs=q_circ*((1+C4s/CS)*wps/wz)/(q_circ*(1/(R8*CS*wz)+RS*CS*wz)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wz/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, Ks,fzrs)
                            draw_sensi('S(C4)',N,D,ns,ds,fp,var)

                            
                            
                            
                        with d2:

                            
                            st.write("S(C2):")
                            C2s=1.01*C2
                            CSs=(C1*C2s)/(C1+C2s)
                            Ks=(1+(R10/R9))/(1+(C4/CSs))
                            wzs=m.sqrt(1/(R5*R6*CSs*C3))
                            wps=wzs*m.sqrt((1+RS/R8)/(1+C4/CSs))
                            Qprimes=1/(2*m.sqrt((1+C2s/C1)*(1+C2s/C3)))
                            qprs=Qprimes*((1+C4/CSs)*wps/wzs)/(Qprimes*(1/(R8*CSs*wzs)+RS*CSs*wzs)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wzs/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, Ks,fzrs)
                            draw_sensi('S(C2)',N,D,ns,ds,fp,var)
                            

                            
                        with d3:

                            
                            st.write("S(C3):")
                            C3s=1.01*C3
                            wzs=m.sqrt(1/(R5*R6*CS*C3s))
                            wps=wzs*m.sqrt((1+RS/R8)/(1+C4/CS))
                            Qprimes=1/(2*m.sqrt((1+C2/C1)*(1+C2/C3s)))
                            qprs=Qprimes*((1+C4/CS)*wps/wzs)/(Qprimes*(1/(R8*CS*wzs)+RS*CS*wzs)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wzs/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, K,fzrs)
                            draw_sensi('S(C3)',N,D,ns,ds,fp,var)

                            
                        st.header("Analyse de sensibilité des résistances")
                        sensi=st.expander('Afficher la sensibilité')
                        d1,d2,d3=sensi.columns([1,1,1])
                        var=1
                        with d3:

                            
                            st.write("S(R7):")
                            R7s=1.01*R7
                            wzs=m.sqrt(1/(RS*R7s*C1*C2))
                            wps=wzs*m.sqrt((1+RS/R8)/(1+C4/CS))
                            qprs=q_circ*((1+C4/CS)*wps/wzs)/(q_circ*(1/(R8*CS*wzs)+RS*CS*wzs)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wzs/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, K,fzrs)
                            draw_sensi('S(R7)',N,D,ns,ds,fp,var)
                            
                            st.write("S(R10):")
                            R10s=1.01*R10
                            Ks=(1+(R10s/R9))/(1+(C4/CS))
                            qprs=q_circ*((1+C4/CS)*wp/wz)/(q_circ*(1/(R8*CS*wz)+RS*CS*wz)-R10s/R9)
                            fprs=wp/(2*m.pi)
                            fzrs=wz/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, Ks,fzrs)
                            draw_sensi('S(R10)',N,D,ns,ds,fp,var)
                            
                            
                            
                        with d1:

                            
                            st.write("S(R5):")
                            R5s=1.01*R5
                            RSs=R5s+R6
                            wzs=m.sqrt(1/(R5s*R6*CS*C3))
                            wps=wzs*m.sqrt((1+RSs/R8)/(1+C4/CS))
                            qprs=q_circ*((1+C4/CS)*wps/wzs)/(q_circ*(1/(R8*CS*wzs)+RSs*CS*wzs)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wzs/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, K,fzrs)
                            draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                            
                            st.write("S(R8):")
                            R8s=1.01*R8
                            wps=wz*m.sqrt((1+RS/R8s)/(1+C4/CS))
                            qprs=q_circ*((1+C4/CS)*wps/wz)/(q_circ*(1/(R8s*CS*wz)+RS*CS*wz)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wz/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, K,fzrs)
                            draw_sensi('S(R8)',N,D,ns,ds,fp,var)
                            
                            
                        with d2:

                            
                            st.write("S(R6):")
                            R6s=1.01*R6
                            RSs=R5+R6s
                            wzs=m.sqrt(1/(R5*R6s*CS*C3))
                            wps=wzs*m.sqrt((1+RSs/R8)/(1+C4/CS))
                            qprs=q_circ*((1+C4/CS)*wps/wzs)/(q_circ*(1/(R8*CS*wzs)+RSs*CS*wzs)-R10/R9)
                            fprs=wps/(2*m.pi)
                            fzrs=wzs/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, K,fzrs)
                            draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                            
                            st.write("S(R9):")
                            R9s=1.01*R9
                            Ks=(1+(R10/R9s))/(1+(C4/CS))
                            qprs=q_circ*((1+C4/CS)*wp/wz)/(q_circ*(1/(R8*CS*wz)+RS*CS*wz)-R10/R9s)
                            fprs=wp/(2*m.pi)
                            fzrs=wz/(2*m.pi)
                            ns,ds=getBR_ND(fprs, qprs, Ks,fzrs)
                            draw_sensi('S(R9)',N,D,ns,ds,fp,var)
                            
    elif sel=='BPLQR (Passe-bande de Rauch (de type R), Q<2)':
        image='iBP-LQ-R.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C2,C3,k]=Param(['fp','Qp','C2','C3','K'],2,p)
            
            P=(qp*qp)*((2+(C2/C3)+(C3/C2)))
            R1=1/((2*m.pi*fp*m.sqrt(P*C2*C3)))
            R4=P*R1
            K0=(qp*qp)*(1+(C3/C2))
            GSP=K0
            
            if k==0.00:
                R11=R1
                R12=1e12
                K=K0
                
            elif (K0-k)<=0.00 :
                R11=R1
                R12=1e12
                K=K0
                
            else :
                K=k 
                R11=(K0/k )*R1
                R12=(K0/(K0-k))*R1
                
            [R11m,R12m,R4m,C2m,C3m,Km,GSPm]= Result(['R11','R12','R4','C2','C3','K','GSP'], [R11,R12,R4,C2,C3,K,GSP],p)
            [C2m,C3m], [R11m,R4m,R12m]=standardisation(['C2','C3'], [C2m,C3m], ['R11','R4','R12'], [R11m,R4m,R12m],p)
            R1m=(R11m*R12m)/(R11m+R12m)
            qpr=m.sqrt((R4m*C2m)/(R1m*C3m))/(1+C2m/C3m)
            K0m=(qpr*qpr)*(1+(C3m/C2m))
            Km=(R12m*K0m)/(R11m+R12m)
            wp=m.sqrt(1/(R1m*C2m*C3m*R4m))  
            fpr=wp/(2*m.pi)
            n,d=getPB_ND(fpr, qpr, Km)
            N,D=getPB_ND(fp, qp, K)
            plot=Aff(N, D,n,d,p)
            name=['fp','Qp','R11','R4','C2','C3','GSP']
            data=[fpr,qpr, R11m,R4m,C2m,C3m,GSPm]
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                
            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)

            
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d2:
                
                st.write("S(C3):")
                C3s=1.01*C3
                qprs=m.sqrt((R4*C2)/(R1*C3s))/(1+C2/C3s)
                K0s=(qprs*qprs)*(1+(C3s/C2))
                Ks=(R12*K0s)/(R11+R12)
                wps=m.sqrt(1/(R1*C2*C3s*R4))  
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C3)',N,D,ns,ds,fp,var)
                
            with d1:

                st.write("S(C2):")
                C2s=1.01*C2
                qprs=m.sqrt((R4*C2s)/(R1*C3))/(1+C2s/C3)
                K0s=(qprs*qprs)*(1+(C3/C2s))
                Ks=(R12*K0s)/(R11+R12)
                wps=m.sqrt(1/(R1*C2s*C3*R4))  
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C2)',N,D,ns,ds,fp,var)

            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d3:
                
                st.write("S(R4):")
                R4s=1.01*R4
                qprs=m.sqrt((R4s*C2)/(R1*C3))/(1+C2/C3)
                K0s=(qprs*qprs)*(1+(C3/C2))
                Ks=(R12*K0s)/(R11+R12)
                wps=m.sqrt(1/(R1*C2*C3*R4s))  
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(R11)',N,D,ns,ds,fp,var)
                
            with d1:
                
                st.write("S(R11):")
                R11s=1.01*R11
                R1s=(R11s*R12)/(R11s+R12)
                qprs=m.sqrt((R4*C2)/(R1s*C3))/(1+C2/C3)
                K0s=(qprs*qprs)*(1+(C3/C2))
                Ks=(R12*K0s)/(R11s+R12)
                wps=m.sqrt(1/(R1s*C2*C3*R4))  
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(R11)',N,D,ns,ds,fp,var)
                
            with d2:
                
                st.write("S(R12):")
                R12s=1.01*R12
                R1s=(R11*R12s)/(R11+R12s)
                qprs=m.sqrt((R4*C2)/(R1s*C3))/(1+C2/C3)
                K0s=(qprs*qprs)*(1+(C3/C2))
                Ks=(R12s*K0s)/(R11+R12s)
                wps=m.sqrt(1/(R1s*C2*C3*R4))  
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(R12)',N,D,ns,ds,fp,var)
                
            
    elif sel=='BPLQC (Passe-bande de Rauch (de type C), Q<2)':
        image='iBP-LQ-C.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C11,C12,C4]=Param(['fp','Qp','C11','C12','C4'],2,p)
            
            if (1/(2*(qp*qp)))*((C11+C12)/C4)>=2 :
                C1=C11+C12
                P=((C1/(2*(qp*qp)*C4))-1)+m.sqrt((((C1/(2*(qp*qp)*C4))-1)*((C1/(2*(qp*qp)*C4))-1))-1)
                R2=1/(2*m.pi*fp*m.sqrt(P*C1*C4))
                R3=P*R2
                GSP=qp*m.sqrt(C1/(P*C4))
                K=C11*GSP/C1
                
                [R2m,R3m,C11m,C12m,C4m,Km,GSPm]=Result(['R2','R3','C11','C12','C4','K','GSP'], [R2,R3,C11,C12,C4,K,GSP],p+100)
                [R2m,R3m],[C11m,C12m,C4m]=standardisation(['R2','R3'], [R2m,R3m], ['C11','C12','C4'], [C11m,C12m,C4m],p+100)
                C1m=C11m+C12m
                qpr=m.sqrt((R3m*C1m)/(R2m*C4m))/(1+R3m/R2m)
                wp=m.sqrt(1/(R2m*C1m*C4m*R3m))
                K0m=qpr*m.sqrt((C1m*R2m)/(C4m*R3m))
                Km=(C11m*K0m)/(C11m+C12m)
                fpr=wp/(2*m.pi)
                N,D=getPB_ND(fp, qp, K)
                n,d=getPB_ND(fpr, qpr, Km)
                plot=Aff(N, D,n,d,p)
                name=['fp','Qp','R2','R3','C11','C12','C4','GSP']
                data=[fpr,qpr, R2m,R3m,C11m,C12m,C4m,GSPm]
                
                st.header("Analyse de sensibilité de Wp et Qp")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d1:
                    st.write("S(Qp):") 
                    fprs=fp
                    qprs=1.01*qp
                    ns,ds=getPB_ND(fprs, qprs, K)
                    draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                    
                with d2:
                    st.write("S(Wp):")
                    fprs=fp*1.01
                    qprs=qp
                    ns,ds=getPB_ND(fprs, qprs, K)
                    draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des capacités")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2,d3=sensi.columns([1,1,1])
                var=1
                with d2:
                    
                    st.write("S(C12):")
                    C12s=1.01*C12
                    C1s=C11+C12s
                    qprs=m.sqrt((R3*C1s)/(R2*C4))/(1+R3/R2)
                    wps=m.sqrt(1/(R2*C1s*C4*R3))
                    K0s=qprs*m.sqrt((C1s*R2)/(C4*R3))
                    Ks=(C11*K0s)/(C11+C12s)
                    fprs=wps/(2*m.pi)
                    ns,ds=getPB_ND(fprs, qprs, Ks)
                    draw_sensi('S(C12)',N,D,ns,ds,fp,var)
                    
                with d3:
                    
                    st.write("S(C4):")
                    C4s=1.01*C4
                    qprs=m.sqrt((R3*C1)/(R2*C4s))/(1+R3/R2)
                    wps=m.sqrt(1/(R2*C1*C4s*R3))
                    K0s=qprs*m.sqrt((C1*R2)/(C4s*R3))
                    Ks=(C11*K0s)/(C11+C12)
                    fprs=wps/(2*m.pi)
                    ns,ds=getPB_ND(fprs, qprs, Ks)
                    draw_sensi('S(C4)',N,D,ns,ds,fp,var)
                    
                with d1:
                    st.write("S(C11):")
                    C11s=1.01*C11
                    C1s=C11s+C12
                    qprs=m.sqrt((R3*C1s)/(R2*C4))/(1+R3/R2)
                    wps=m.sqrt(1/(R2*C1s*C4*R3))
                    K0s=qprs*m.sqrt((C1s*R2)/(C4*R3))
                    Ks=(C11s*K0s)/(C11s+C12)
                    fprs=wps/(2*m.pi)
                    ns,ds=getPB_ND(fprs, qprs, Ks)
                    draw_sensi('S(C11)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des résistances")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d2:
                    
                    st.write("S(R3):")
                    R3s=1.01*R3
                    qprs=m.sqrt((R3s*C1)/(R2*C4))/(1+R3s/R2)
                    wps=m.sqrt(1/(R2*C1*C4*R3s))
                    K0s=qprs*m.sqrt((C1*R2)/(C4*R3s))
                    Ks=(C11*K0s)/(C11+C12)
                    fprs=wps/(2*m.pi)
                    ns,ds=getPB_ND(fprs, qprs, Ks)
                    draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                    
                with d1:
                    
                    st.write("S(R2):")
                    R2s=1.01*R2
                    qprs=m.sqrt((R3*C1)/(R2s*C4))/(1+R3/R2s)
                    wps=m.sqrt(1/(R2s*C1*C4*R3))
                    K0s=qprs*m.sqrt((C1*R2s)/(C4*R3))
                    Ks=(C11*K0s)/(C11+C12)
                    fprs=wps/(2*m.pi)
                    ns,ds=getPB_ND(fprs, qprs, Ks)
                    draw_sensi('S(R2)',N,D,ns,ds,fp,var)
            else :            
                st.markdown(':warning:**:red[ERREUR]**:warning: **Il faut que  **  $C11+C12>=4*Qp^2*C4$')
            
    
    elif sel=='BPMQR (Passe-bande de Rauch (de type R), Q<10)':
        image='iBP-MQ-R.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
              
            [fp,qp,C2,C3,k,R6]=Param(['fp','Qp','C2','C3','K','R6  (Optionnel)'],10,p)
        
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
                R12=1e12
                K=K0
            elif K0-k<=0:
                R11=R1
                R12=1e12
                K=K0       
            else:
                K=k
                R11=K0/K*R1
                R12=K0/(K0-K)*R1
                
            [R11m,R12m,R4m,R5m,R6m,C2m,C3m,Km,Pm,GSPm]= Result(['R11','R12','R4','R5','R6','C2','C3','K','P','GSP'], [R11,R12,R4,R5,R6,C2,C3,K,P,GSP],p)
            [R11m,R12m,R4m,R5m,R6m],[C2m,C3m]=standardisation(['R11','R12','R4','R5','R6'], [R11m,R12m,R4m,R5m,R6m],['C2','C3'], [C2m,C3m],p)
            R1m=(R11m*R12m)/(R11m+R12m)
            qpr=m.sqrt((R4m*C2m)/(R1m*C3m))/(1+C2m/C3m-R4m*R5m/(R1m*R6m))
            Km=((R12m*qpr)/(R11m+R12m))*(1+R5m/R6m)*m.sqrt((C3m*R4m)/(R1m*C2m))
            wp=m.sqrt(1/(R1m*C2m*C3m*R4m))
            fpr=wp/(2*m.pi)
            N,D=getPB_ND(fp, qp, K)
            n,d=getPB_ND(fpr, qpr, Km)
            plot=Aff(N, D,n,d,p)
            name=['fp','Qp','R11','R12','R4','R5','C2','C3','P','GSP']
            data=[fpr,qpr, R11m,R12m,R4m,R5m,C2m,C3m,Pm,GSPm]
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                
            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d2:
                
                st.write("S(C3):")
                C3s=1.01*C3
                qprs=m.sqrt((R4*C2)/(R1*C3s))/(1+C2/C3s-R4*R5/(R1*R6))
                Ks=((R12*qprs)/(R11+R12))*(1+R5/R6)*m.sqrt((C3s*R4)/(R1*C2))
                wps=m.sqrt(1/(R1*C2*C3s*R4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C3)',N,D,ns,ds,fp,var)
                
            with d1:
                st.write("S(C2):")
                C2s=1.01*C2
                qprs=m.sqrt((R4*C2s)/(R1*C3))/(1+C2s/C3-R4*R5/(R1*R6))
                Ks=((R12*qprs)/(R11+R12))*(1+R5/R6)*m.sqrt((C3*R4)/(R1*C2s))
                wps=m.sqrt(1/(R1*C2s*C3*R4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C2)',N,D,ns,ds,fp,var)
            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d3:
                
                st.write("S(R4):")
                R4s=1.01*R4
                qprs=m.sqrt((R4s*C2)/(R1*C3))/(1+C2/C3-R4s*R5/(R1*R6))
                Ks=((R12*qprs)/(R11+R12))*(1+R5/R6)*m.sqrt((C3*R4s)/(R1*C2))
                wps=m.sqrt(1/(R1*C2*C3*R4s))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                
            with d1:
                
                st.write("S(R11):")
                R11s=1.01*R11
                R1s=(R11s*R12)/(R11s+R12)
                qprs=m.sqrt((R4*C2)/(R1s*C3))/(1+C2/C3-R4*R5/(R1s*R6))
                Ks=((R12*qprs)/(R11s+R12))*(1+R5/R6)*m.sqrt((C3*R4)/(R1s*C2))
                wps=m.sqrt(1/(R1s*C2*C3*R4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R11)',N,D,ns,ds,fp,var)
                
                st.write("S(R5):")
                R5s=1.01*R5
                qprs=m.sqrt((R4*C2)/(R1*C3))/(1+C2/C3-R4*R5s/(R1*R6))
                Ks=((R12*qprs)/(R11+R12))*(1+R5s/R6)*m.sqrt((C3*R4)/(R1*C2))
                wps=m.sqrt(1/(R1*C2*C3*R4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                
            with d2:
                
                st.write("S(R12):")
                R12s=1.01*R12
                R1s=(R11*R12s)/(R11+R12s)
                qprs=m.sqrt((R4*C2)/(R1s*C3))/(1+C2/C3-R4*R5/(R1s*R6))
                Ks=((R12s*qprs)/(R11+R12s))*(1+R5/R6)*m.sqrt((C3*R4)/(R1s*C2))
                wps=m.sqrt(1/(R1s*C2*C3*R4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R12)',N,D,ns,ds,fp,var)
                
                st.write("S(R6):")
                R6s=1.01*R6
                qprs=m.sqrt((R4*C2)/(R1*C3))/(1+C2/C3-R4*R5/(R1*R6s))
                Ks=((R12*qprs)/(R11+R12))*(1+R5/R6s)*m.sqrt((C3*R4)/(R1*C2))
                wps=m.sqrt(1/(R1*C2*C3*R4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R6)',N,D,ns,ds,fp,var)
    
    elif sel=='BPMQC (Passe-bande de Rauch (de type C), Q<10)':
        image='iBP-MQ-C.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C11,C12,C4,R6]=Param(['fp','Qp','C11','C12','C4','R6  (Optionnel)'],10,p)
            
            C1=C11+C12
            P=(C1/C4)/(36*qp*qp)*(m.sqrt(1+12*qp*qp*(1+C4/C1))+1)*(m.sqrt(1+12*qp*qp*(1+C4/C1))+1)
            R2=1/(2*m.pi*fp*m.sqrt(P*C1*C4))
            R3=P*R2
            if R6==0:
                R6=1e4
            R5=R6*(C4/C1*(1+P)-m.sqrt(P*C4/C1)/qp)
            K=C11/C1*(1+R5/R6)*qp*m.sqrt(C1/(P*C4))
            GSP=qp*(1+R5/R6)*(1+R5/R6)*m.sqrt(C1/(P*C4))
             
            [R2m,R3m,R5m,C11m,C12m,C4m,R6m,Km,Pm,GSPm]=Result(['R2','R3','R5','C11','C12','C4','R6  (Optionnel)','K','P','GSP'], [R2,R3,R5,C11,C12,C4,R6,K,P,GSP],p)
            [R2m,R3m,R5m,R6m],[C11m,C12m,C4m]=standardisation(['R2','R3','R5','R6 '],  [R2m,R3m,R5m,R6m], ['C11','C12','C4'], [C11m,C12m,C4m],p)
            C1m=C11m+C12m
            qpr=m.sqrt((R3m*C1m)/(R2m*C4m))/(1+R3m/R2m-C1m*R5m/(C4m*R6m))
            wp=m.sqrt(1/(R2m*C1m*R3m*C4m))
            Km=C11m/C1m*(1+R5m/R6m)*qpr*m.sqrt((C1m*R2m)/(R3m*C4m))
            fpr=wp/(2*m.pi)
            N,D=getPB_ND(fp, qp, K)
            n,d=getPB_ND(fpr, qpr, Km)
            plot=Aff(N, D,n,d,p)
            name=['fp','Qp','R2','R3','R5','C11','C12','C4','R6  (Optionnel)','P','GSP']
            data=[fpr,qpr, R2m,R3m,R5m,C11m,C12m,C4m,R6m,Pm,GSPm]
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                
            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
            
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d2:
                
                st.write("S(C12):")
                C12s=1.01*C12
                C1s=C11+C12s
                qprs=m.sqrt((R3*C1s)/(R2*C4))/(1+R3/R2-C1s*R5/(C4*R6))
                wps=m.sqrt(1/(R2*C1s*R3*C4))
                Ks=C11/C1s*(1+R5/R6)*qprs*m.sqrt((C1s*R2)/(R3*C4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C12)',N,D,ns,ds,fp,var)
                
            with d3:
                
                st.write("S(C4):")
                C4s=1.01*C4
                qprs=m.sqrt((R3*C1)/(R2*C4s))/(1+R3/R2-C1*R5/(C4s*R6))
                wps=m.sqrt(1/(R2*C1*R3*C4s))
                Ks=C11/C1*(1+R5/R6)*qprs*m.sqrt((C1*R2)/(R3*C4s))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C4)',N,D,ns,ds,fp,var)
                
            with d1:
                st.write("S(C11):")
                C11s=1.01*C11
                C1s=C11s+C12
                qprs=m.sqrt((R3*C1s)/(R2*C4))/(1+R3/R2-C1s*R5/(C4*R6))
                wps=m.sqrt(1/(R2*C1s*R3*C4))
                Ks=C11s/C1s*(1+R5/R6)*qprs*m.sqrt((C1s*R2)/(R3*C4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C11)',N,D,ns,ds,fp,var)
            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d2:
                st.write("S(R3):")
                R3s=1.01*R3
                qprs=m.sqrt((R3s*C1)/(R2*C4))/(1+R3s/R2-C1*R5/(C4*R6))
                wps=m.sqrt(1/(R2*C1*R3s*C4))
                Ks=C11/C1*(1+R5/R6)*qprs*m.sqrt((C1*R2)/(R3s*C4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                
            with d3:
                
                st.write("S(R5):")
                R5s=1.01*R5
                qprs=m.sqrt((R3*C1)/(R2*C4))/(1+R3/R2-C1*R5s/(C4*R6))
                wps=m.sqrt(1/(R2*C1*R3*C4))
                Ks=C11/C1*(1+R5s/R6)*qprs*m.sqrt((C1*R2)/(R3*C4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                
            with d1:
                
                st.write("S(R2):")
                R2s=1.01*R2
                qprs=m.sqrt((R3*C1)/(R2s*C4))/(1+R3/R2s-C1*R5/(C4*R6))
                wps=m.sqrt(1/(R2s*C1*R3*C4))
                Ks=C11/C1*(1+R5/R6)*qprs*m.sqrt((C1*R2s)/(R3*C4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                
                st.write("S(R6):")
                R6s=1.01*R6
                qprs=m.sqrt((R3*C1)/(R2*C4))/(1+R3/R2-C1*R5/(C4*R6s))
                wps=m.sqrt(1/(R2*C1*R3*C4))
                Ks=C11/C1*(1+R5/R6s)*qprs*m.sqrt((C1*R2)/(R3*C4))
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R6)',N,D,ns,ds,fp,var)
        
    elif sel=='Passe-bas de Flieghe (Q<30)':
        image='iLP-HQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C]=Param(['fp','Qp','C'],30,p)
            R_optimal=1/(2*m.pi*fp*C)
            R_optimalint=int(R_optimal)
            minval=float(R_optimalint-10)
            maxval=float(R_optimalint+10)
            Rd=st.slider("Choix de Rd=R2=R3=R6 proche de R optimale calculée sur base de fp et C.",minval,maxval,R_optimal)
            C1=C
            C4=C
            R2=Rd
            R3=Rd
            R6=Rd
            R1=qp*R_optimal
            R7=(R_optimal*R_optimal)/Rd       
            K=1+R2/R6    
            
            [R1m,R2m,R3m,R6m,R7m,C1m,C4m]=Result(['R1','R2','R3','R6','R7','C1','C4'], [R1,R2,R3,R6,R7,C1,C4],p)
            [R1m,R2m,R3m,R6m,R7m],[C1m,C4m]=standardisation(['R1','R2','R3','R6','R7'], [R1m,R2m,R3m,R6m,R7m], ['C1','C4'],[C1m,C4m],p)
            Km=1+R2m/R6m
            wp=m.sqrt(R6m/(R2m*R3m*R7m*C1m*C4m))
            qpr=wp*R1m*C1m
            fpr=wp/(2*m.pi)
            N,D=getLP_ND(fp, qp, K)
            n,d=getLP_ND(fpr, qpr, Km)
            plot=Aff(N, D,n,d,p)
            name=['fp','Qp','R1','R2','R3','R6','R7','C1','C4']
            data=[fpr,qpr, R1m,R2m,R3m,R6m,R7m,C1m,C4m]
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getLP_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)

            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getLP_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)

            
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d2:
                st.write("S(C4):")
                C4s=1.01*C4
                Ks=1+R2/R6
                wps=m.sqrt(R6/(R2*R3*R7*C1*C4s))
                qprs=wps*R1*C1
                fprs=wps/(2*m.pi)
                ns,ds=getLP_ND(fprs, qprs, Ks)
                draw_sensi('S(C4)',N,D,ns,ds,fp,var)
                
            with d1:

                st.write("S(C1):")
                C1s=1.01*C1
                Ks=1+R2/R6
                wps=m.sqrt(R6/(R2*R3*R7*C1s*C4))
                qprs=wps*R1*C1s
                fprs=wps/(2*m.pi)
                ns,ds=getLP_ND(fprs, qprs, Ks)
                draw_sensi('S(C1)',N,D,ns,ds,fp,var)

            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d3:
                
                st.write("S(R3):")
                R3s=1.01*R3
                Ks=1+R2/R6
                wps=m.sqrt(R6/(R2*R3s*R7*C1*C4))
                qprs=wps*R1*C1
                fprs=wps/(2*m.pi)
                ns,ds=getLP_ND(fprs, qprs, Ks)
                draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                
            with d1:
                
                st.write("S(R1):")
                R1s=1.01*R1
                Ks=1+R2/R6
                wps=m.sqrt(R6/(R2*R3*R7*C1*C4))
                qprs=wps*R1s*C1
                fprs=wps/(2*m.pi)
                ns,ds=getLP_ND(fprs, qprs, Ks)
                draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                
                st.write("S(R6):")
                R6s=1.01*R6
                Ks=1+R2/R6s
                wps=m.sqrt(R6s/(R2*R3*R7*C1*C4))
                qprs=wps*R1*C1
                fprs=wps/(2*m.pi)
                ns,ds=getLP_ND(fprs, qprs, Ks)
                draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                
            with d2:
                
                st.write("S(R2):")
                R2s=1.01*R2
                Ks=1+R2s/R6
                wps=m.sqrt(R6/(R2s*R3*R7*C1*C4))
                qprs=wps*R1*C1
                fprs=wps/(2*m.pi)
                ns,ds=getLP_ND(fprs, qprs, Ks)
                draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                
                st.write("S(R7):")
                R7s=1.01*R7
                Ks=1+R2/R6
                wps=m.sqrt(R6/(R2*R3*R7s*C1*C4))
                qprs=wps*R1*C1
                fprs=wps/(2*m.pi)
                ns,ds=getLP_ND(fprs, qprs, Ks)
                draw_sensi('S(R7)',N,D,ns,ds,fp,var)
    
    elif sel=='Passe-bande de Flieghe (Q<30)':
        image='iBP-HQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            
            [fp,qp,C]=Param(['fp','Qp','C'],30,p)
            R_optimal=1/(2*m.pi*fp*C)
            Rd=R_optimal
            C3=C
            C8=C
            R2=Rd
            R1=Rd
            R6=Rd
            R7=qp*R_optimal
            R4=(R_optimal*R_optimal)/Rd  
            K=1+R2/R6
            
            [R1m,R2m,R4m,R6m,R7m,C3m,C8m]= Result(['R1','R2','R4','R6','R7','C3','C8'], [R1,R2,R4,R6,R7,C3,C8],p)
            [C3m,C8m],[R1m,R2m,R4m,R6m,R7m]=standardisation(['C3','C8'], [C3m,C8m], ['R1','R2','R4','R6','R7'], [R1m,R2m,R4m,R6m,R7m],p)
            Km=1+R2m/R6m
            wp=m.sqrt(R2m/(R1m*R4m*R6m*C3m*C8m))
            qpr=wp*R7m*C8m
            fpr=wp/(2*m.pi)
            N,D=getPB_ND(fp, qp, K)
            n,d=getPB_ND(fpr, qpr, Km)
            plot=Aff(N, D,n,d,p)
            data=[fpr,qpr,R1m,R2m,R4m,R6m,R7m,C3m,C8m]
            name=['fp','Qp','R1','R2','R4','R6','R7','C3','C8']
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                
            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getPB_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
            
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d2:
                
                st.write("S(C8):")
                C8s=1.01*C8
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4*R6*C3*C8s))
                qprs=wps*R7*C8s
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C8)',N,D,ns,ds,fp,var)
                
            with d1:

                st.write("S(C3):")
                C3s=1.01*C3
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4*R6*C3s*C8))
                qprs=wps*R7*C8
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(C3)',N,D,ns,ds,fp,var)
                
            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d3:
                
                st.write("S(R4):")
                R4s=1.01*R4
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4s*R6*C3*C8))
                qprs=wps*R7*C8
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                
            with d1:

                
                st.write("S(R1):")
                R1s=1.01*R1
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1s*R4*R6*C3*C8))
                qprs=wps*R7*C8
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                
                st.write("S(R6):")
                R6s=1.01*R6
                Ks=1+R2/R6s
                wps=m.sqrt(R2/(R1*R4*R6s*C3*C8))
                qprs=wps*R7*C8
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                
            with d2:
                
                st.write("S(R2):")
                R2s=1.01*R2
                Ks=1+R2s/R6
                wps=m.sqrt(R2s/(R1*R4*R6*C3*C8))
                qprs=wps*R7*C8
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                
                st.write("S(R7):")
                R7s=1.01*R7
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4*R6*C3*C8))
                qprs=wps*R7s*C8
                fprs=wps/(2*m.pi)
                ns,ds=getPB_ND(fprs, qprs, Ks)
                draw_sensi('S(R7)',N,D,ns,ds,fp,var)
    
    elif sel=='Passe-haut de Flieghe (Q<30)':
        image='iHP-HQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
            [fp,qp,C]=Param(['fp','Qp','C'],30,p)
         
            R_optimal=1/(2*m.pi*fp*C)
            Rd=R_optimal
            C3=C
            C7=C
            R2=Rd
            R1=Rd
            R6=Rd
            R8=qp*R_optimal
            R4=(R_optimal*R_optimal)/Rd           
            K=1+R2/R6   
            
            [R1m,R2m,R4m,R6m,R8m,C3m,C7m]= Result(['R1','R2','R4','R6','R8','C3','C7'], [R1,R2,R4,R6,R8,C3,C7],p)
            [C3m,C7m],[R1m,R2m,R4m,R6m,R8m]=standardisation(['C3','C7'], [C3m,C7m], ['R1','R2','R4','R6','R8'], [R1m,R2m,R4m,R6m,R8m],p)
            Km=1+R2m/R6m
            wp=m.sqrt(R2m/(R1m*R4m*R6m*C3m*C7m))
            qpr=wp*R8m*C7m
            fpr=wp/(2*m.pi)
            N,D=getHP_ND(fp, qp, K)
            n,d=getHP_ND(fpr, qpr, Km)
            plot=Aff(N, D,n,d,p)
            data=[fpr,qpr,R1m,R2m,R4m,R6m,R8m,C3m,C7m]
            name=['fp','Qp','R1','R2','R4','R6','R8','C3','C7']
            
            st.header("Analyse de sensibilité de Wp et Qp")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d1:
                st.write("S(Qp):") 
                fprs=fp
                qprs=1.01*qp
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                
            with d2:
                st.write("S(Wp):")
                fprs=fp*1.01
                qprs=qp
                ns,ds=getHP_ND(fprs, qprs, K)
                draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
            
            st.header("Analyse de sensibilité des capacités")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2=sensi.columns([1,1])
            var=1
            with d2:
                
                st.write("S(C7):")
                C7s=1.01*C7
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4*R6*C3*C7s))
                qprs=wps*R8*C7s
                fprs=wps/(2*m.pi)
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(C7)',N,D,ns,ds,fp,var)
                
            with d1:
                st.write("S(C3):")
                C3s=1.01*C3
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4*R6*C3s*C7))
                qprs=wps*R8*C7
                fprs=wps/(2*m.pi)
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(C3)',N,D,ns,ds,fp,var)
            
            st.header("Analyse de sensibilité des résistances")
            sensi=st.expander('Afficher la sensibilité')
            d1,d2,d3=sensi.columns([1,1,1])
            var=1
            with d3:
                
                st.write("S(R4):")
                R4s=1.01*R4
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4s*R6*C3*C7))
                qprs=wps*R8*C7
                fprs=wps/(2*m.pi)
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                
            with d1:
                
                st.write("S(R1):")
                R1s=1.01*R1
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1s*R4*R6*C3*C7))
                qprs=wps*R8*C7
                fprs=wps/(2*m.pi)
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                
                st.write("S(R6):")
                R6s=1.01*R6
                Ks=1+R2/R6s
                wps=m.sqrt(R2/(R1*R4*R6s*C3*C7))
                qprs=wps*R8*C7
                fprs=wps/(2*m.pi)
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                
            with d2:
                
                st.write("S(R2):")
                R2s=1.01*R2
                Ks=1+R2s/R6
                wps=m.sqrt(R2s/(R1*R4*R6*C3*C7))
                qprs=wps*R8*C7
                fprs=wps/(2*m.pi)
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                
                st.write("S(R8):")
                R8s=1.01*R8
                Ks=1+R2/R6
                wps=m.sqrt(R2/(R1*R4*R6*C3*C7))
                qprs=wps*R8s*C7
                fprs=wps/(2*m.pi)
                ns,ds=getHP_ND(fprs, qprs, Ks)
                draw_sensi('S(R8)',N,D,ns,ds,fp,var)
    
    elif sel=='Réjecteur de fréquence de Flieghe (Q<30)':
        image='iHP-HQ.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=p*sel):
           
            [fz,fp,qp,C]=Param(['fz','fp','Qp','C'],30,p)
            R_optimal=1/(2*m.pi*fp*C)
            Rd=R_optimal
            C2=C
            C7=C
            R3=Rd
            R1=Rd
            R8=qp*R_optimal    
           
            if fz>fp:
                R4=R8*(((fz/fp)*(fz/fp))-1)
                R5=(R_optimal*R_optimal)/R4
                [R1m,R3m,R4m,R5m,R8m,C2m,C7m]= Result(['R1','R3','R4','R5','R8','C2','C7'], [R1,R3,R4,R5,R8,C2,C7],p)
                [C2m,C7m],[R1m,R3m,R4m,R5m,R8m]=standardisation(['C2','C7'], [C2m,C7m], ['R1','R3','R4','R5','R8'], [R1m,R3m,R4m,R5m,R8m],p)
                wpr=m.sqrt(R3m/(R1m*R4m*R5m*C2m*C7m))
                qpr=wpr*C7m*R8m
                wzrlpn=wpr*m.sqrt(1+R4m/R8m)
                fpr=wpr/(2*m.pi)
                fzr=wzrlpn/(2*m.pi)
                N,D=getBR_ND(fp, qp, 1, fz)
                n,d=getBR_ND(fpr, qpr, 1, fzr)
                plot=Aff(N, D,n,d,p)
                data=[fzr,fpr,qpr,R1m,R3m,R4m,R5m,R8m,C2m,C7m]
                name=['fz','fp','Qp','R1','R3','R4','R5','R8','C2','C7']
                
                st.header("Analyse de sensibilité de Wp, Wz et Qp")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2,d3=sensi.columns([1,1,1])
                var=1
                with d1:
                    st.write("S(Qp):") 
                    fprs=fp
                    qprs=1.01*qp
                    fzrs=fz
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                    
                with d2:
                    st.write("S(Wp):")
                    fprs=fp*1.01
                    qprs=qp
                    fzrs=fz
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                    
                with d3:
                    st.write("S(Wz):")
                    fzrs=fz*1.01
                    qprs=qp
                    fprs=fp
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(Wz)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des capacités")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d1:
                    
                    st.write("S(C2):")
                    C2s=1.01*C2
                    wprs=m.sqrt(R3/(R1*R4*R5*C2s*C7))
                    qprs=wprs*C7*R8
                    wzrlpns=wprs*m.sqrt(1+R4/R8)
                    fprs=wprs/(2*m.pi)
                    fzrs=wzrlpns/(2*m.pi)
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(C2)',N,D,ns,ds,fp,var)
                    
                with d2:
                    
                    st.write("S(C7):")
                    C7s=1.01*C7
                    wprs=m.sqrt(R3/(R1*R4*R5*C2*C7s))
                    qprs=wprs*C7s*R8
                    wzrlpns=wprs*m.sqrt(1+R4/R8)
                    fprs=wprs/(2*m.pi)
                    fzrs=wzrlpns/(2*m.pi)
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(C7)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des résistances")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2,d3=sensi.columns([1,1,1])
                var=1
                with d2:
                    
                    st.write("S(R3):")
                    R3s=1.01*R3
                    wprs=m.sqrt(R3s/(R1*R4*R5*C2*C7))
                    qprs=wprs*C7*R8
                    wzrlpns=wprs*m.sqrt(1+R4/R8)
                    fprs=wprs/(2*m.pi)
                    fzrs=wzrlpns/(2*m.pi)
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R8):")
                    R8s=1.01*R8
                    wprs=m.sqrt(R3/(R1*R4*R5*C2*C7))
                    qprs=wprs*C7*R8s
                    wzrlpns=wprs*m.sqrt(1+R4/R8s)
                    fprs=wprs/(2*m.pi)
                    fzrs=wzrlpns/(2*m.pi)
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(R8)',N,D,ns,ds,fp,var)
                    
                with d3:
                    
                    st.write("S(R4):")
                    R4s=1.01*R4
                    wprs=m.sqrt(R3/(R1*R4s*R5*C2*C7))
                    qprs=wprs*C7*R8
                    wzrlpns=wprs*m.sqrt(1+R4s/R8)
                    fprs=wprs/(2*m.pi)
                    fzrs=wzrlpns/(2*m.pi)
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                    
                with d1:
                    
                    st.write("S(R1):")
                    R1s=1.01*R1
                    wprs=m.sqrt(R3/(R1s*R4*R5*C2*C7))
                    qprs=wprs*C7*R8
                    wzrlpns=wprs*m.sqrt(1+R4/R8)
                    fprs=wprs/(2*m.pi)
                    fzrs=wzrlpns/(2*m.pi)
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R5):")
                    R5s=1.01*R5
                    wprs=m.sqrt(R3/(R1*R4*R5s*C2*C7))
                    qprs=wprs*C7*R8
                    wzrlpns=wprs*m.sqrt(1+R4/R8)
                    fprs=wprs/(2*m.pi)
                    fzrs=wzrlpns/(2*m.pi)
                    ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                    draw_sensi('S(R5)',N,D,ns,ds,fp,var)
        
            elif fz<fp:
                R4=R8*(1-((fz/fp)*(fz/fp)))
                R5=(R_optimal*R_optimal)/R4
                [R1m,R3m,R4m,R5m,R8m,C2m,C7m]= Result(['R1','R3','R4','R5','R8','C2','C7'], [R1,R3,R4,R5,R8,C2,C7],p)
                [C2m,C7m],[R1m,R3m,R4m,R5m,R8m]=standardisation(['C2','C7'], [C2m,C7m], ['R1','R3','R4','R5','R8'], [R1m,R3m,R4m,R5m,R8m],p)
                wpr=m.sqrt(R3m/(R1m*R4m*R5m*C2m*C7m))
                qpr=wpr*C7m*R8m
                racinewzrhpn=1-(R1m*R4m)/(R3m*R8m)
                if racinewzrhpn<0:
                    st.markdown(":warning: **Il faut que** $$$\dfrac{R1*R4}{R3*R8}<1$$$")
                else:
                    wzrhpn=wpr*m.sqrt(racinewzrhpn)
                    fpr=wpr/(2*m.pi)
                    fzr=wzrhpn/(2*m.pi)
                    N,D=getBR_ND(fp, qp, 1, fz)
                    n,d=getBR_ND(fpr, qpr, 1, fzr)
                    plot=Aff(N, D,n,d,p)
                    data=[fzr,fpr,qpr,R1m,R3m,R4m,R5m,R8m,C2m,C7m]
                    name=['fz','fp','Qp','R1','R3','R4','R5','R8','C2','C7']
                    
                    st.header("Analyse de sensibilité de Wp, Wz et Qp")
                    sensi=st.expander('Afficher la sensibilité')
                    d1,d2,d3=sensi.columns([1,1,1])
                    var=1
                    with d1:
                        st.write("S(Qp):") 
                        fprs=fp
                        qprs=1.01*qp
                        fzrs=fz
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                        
                    with d2:
                        st.write("S(Wp):")
                        fprs=fp*1.01
                        qprs=qp
                        fzrs=fz
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(Wp)',N,D,ns,ds,fp,var)

                    with d3:
                        st.write("S(Wz):")
                        fzrs=fz*1.01
                        qprs=qp
                        fprs=fp
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(Wz)',N,D,ns,ds,fp,var)
                    
                    st.header("Analyse de sensibilité des capacités")
                    sensi=st.expander('Afficher la sensibilité')
                    d1,d2=sensi.columns([1,1])
                    var=1
                    with d1:
                        
                        st.write("S(C2):")
                        C2s=1.01*C2
                        wps=m.sqrt(R3/(R1*R4*R5*C2s*C7))
                        qprs=wps*C7*R8
                        wzrhpns=wps*m.sqrt(1-(R1*R4)/(R3*R8))
                        fprs=wps/(2*m.pi)
                        fzrs=wzrhpns/(2*m.pi)
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(C2)',N,D,ns,ds,fp,var)
                        
                    with d2:
                        
                        st.write("S(C7):")
                        C7s=1.01*C7
                        wps=m.sqrt(R3/(R1*R4*R5*C2*C7s))
                        qprs=wps*C7s*R8
                        wzrhpns=wps*m.sqrt(1-(R1*R4)/(R3*R8))
                        fprs=wps/(2*m.pi)
                        fzrs=wzrhpns/(2*m.pi)
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(C7)',N,D,ns,ds,fp,var)


                    
                    st.header("Analyse de sensibilité des résistances")
                    sensi=st.expander('Afficher la sensibilité')
                    d1,d2,d3=sensi.columns([1,1,1])
                    var=1
                    with d2:
                        
                        st.write("S(R3):")
                        R3s=1.01*R3
                        wps=m.sqrt(R3s/(R1*R4*R5*C2*C7))
                        qprs=wps*C7*R8
                        wzrhpns=wps*m.sqrt(1-(R1*R4)/(R3s*R8))
                        fprs=wps/(2*m.pi)
                        fzrs=wzrhpns/(2*m.pi)
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                        
                        st.write("S(R8):")
                        R8s=1.01*R8
                        wps=m.sqrt(R3/(R1*R4*R5*C2*C7))
                        qprs=wps*C7*R8s
                        wzrhpns=wps*m.sqrt(1-(R1*R4)/(R3*R8s))
                        fprs=wps/(2*m.pi)
                        fzrs=wzrhpns/(2*m.pi)
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(R8)',N,D,ns,ds,fp,var)
                        
                    with d3:
                        
                        st.write("S(R4):")
                        R4s=1.01*R4
                        wps=m.sqrt(R3/(R1*R4s*R5*C2*C7))
                        qprs=wps*C7*R8
                        wzrhpns=wps*m.sqrt(1-(R1*R4s)/(R3*R8))
                        fprs=wps/(2*m.pi)
                        fzrs=wzrhpns/(2*m.pi)
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                        
                    with d1:
                        
                        st.write("S(R1):")
                        R1s=1.01*R1
                        wps=m.sqrt(R3/(R1s*R4*R5*C2*C7))
                        qprs=wps*C7*R8
                        wzrhpns=wps*m.sqrt(1-(R1s*R4)/(R3*R8))
                        fprs=wps/(2*m.pi)
                        fzrs=wzrhpns/(2*m.pi)
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                        
                        st.write("S(R5):")
                        R5s=1.01*R5
                        wps=m.sqrt(R3/(R1*R4*R5s*C2*C7))
                        qprs=wps*C7*R8
                        wzrhpns=wps*m.sqrt(1-(R1*R4)/(R3*R8))
                        fprs=wps/(2*m.pi)
                        fzrs=wzrhpns/(2*m.pi)
                        ns,ds=getBR_ND(fprs, qprs, 1, fzrs)
                        draw_sensi('S(R5)',N,D,ns,ds,fp,var)
            
            else:
                st.markdown(":warning: **fz doit être différente de fp**")
            
    elif sel=='Cellule Universelle de Tow-Thomas (Q<100)':
        clès=p+p*8887
        image='Tow_Thomas.jpg'
        st.image(image,width=800)
        if st.checkbox('**Choisir ce filtre**:+1:',key=clès):
            
            typ=st.selectbox("Quel est le type de section?",['Passe-Bas','Passe-Haut','Passe-Bande','Réjecteur de fréquence'],key=clès+2)
            if typ=='Passe-Bas':
                sel+=' (passe-bas)'
                [fp,qp,C]=Param(['fp','Qp','C=C9=C10'],100,p)
                
                R_optimal=1/(2*m.pi*fp*C)
                Rd=R_optimal
                C9=C
                C10=C
                R2=Rd
                R3=Rd
                R8=Rd
                R7=(R_optimal**2)/Rd
                R1=qp*m.sqrt(Rd*R7)
                R4=float('inf')
                R6=float('inf')
                R5=Rd
                K3=R8/(R7*R3*R5*C9*C10)
                [R1m,R2m,R3m,R5m,R7m,R8m,C9m,C10m]=Result(['R1','R2','R3','R5','R7','R8','C9','C10'], [R1,R2,R3,R5,R7,R8,C9,C10],p)
                [R1m,R2m,R3m,R5m,R7m,R8m],[C9m,C10m]=standardisation(['R1','R2','R3','R5','R7','R8'], [R1m,R2m,R3m,R5m,R7m,R8m], ['C9','C10'], [C9m,C10m],p)
                fpr=(m.sqrt(R8m/(R2m*R3m*R7m*C9m*C10m)))/(2*m.pi)
                qpr=R1m*m.sqrt(R8m*C9m/(R2m*R3m*R7m*C10m))
                K3r=R8m/(R7m*R3m*R5m*C9m*C10m)
                N,D=getLPTT_ND(fp, qp, K3)
                n,d=getLPTT_ND(fpr, qpr, K3r)
                plot=Aff(N, D,n,d,p)
                data=[fpr,qpr,R1m,R2m,R3m,R5m,R7m,R8m,C9m,C10m]
                name=['fp','Qp','R1','R2','R3','R5','R7','R8','C9','C10']
                
                st.header("Analyse de sensibilité de Wp et Qp")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d1:
                    st.write("S(Qp):") 
                    fprs=fp
                    qprs=1.01*qp
                    ns,ds=getLPTT_ND(fprs, qprs, K3)
                    draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                    
                with d2:
                    st.write("S(Wp):")
                    fprs=fp*1.01
                    qprs=qp
                    ns,ds=getLPTT_ND(fprs, qprs, K3)
                    draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des capacités")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d2:
                    
                    st.write("S(C10):")
                    C10s=1.01*C10
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10s)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10s))
                    K3s=R8/(R7*R3*R5*C9*C10s)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(C10)',N,D,ns,ds,fp,var)
                    
                with d1:
                    
                    st.write("S(C9):")
                    C9s=1.01*C9
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9s*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9s/(R2*R3*R7*C10))
                    K3s=R8/(R7*R3*R5*C9s*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(C9)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des résistances")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2,d3=sensi.columns([1,1,1])
                var=1
                with d3:
                    
                    st.write("S(R3):")
                    R3s=1.01*R3
                    fprs=(m.sqrt(R8/(R2*R3s*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3s*R7*C10))
                    K3s=R8/(R7*R3s*R5*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R6):")
                    R6s=1.01*R6
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K3s=R8/(R7*R3*R5*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                    
                with d1:
                    
                    st.write("S(R1):")
                    R1s=1.01*R1
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1s*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K3s=R8/(R7*R3*R5*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R4):")
                    R4s=1.01*R4
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K3s=R8/(R7*R3*R5*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R7):")
                    R7s=1.01*R7
                    fprs=(m.sqrt(R8/(R2*R3*R7s*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7s*C10))
                    K3s=R8/(R7s*R3*R5*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R7)',N,D,ns,ds,fp,var)
                    
                with d2:
                    
                    st.write("S(R2):")
                    R2s=1.01*R2
                    fprs=(m.sqrt(R8/(R2s*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2s*R3*R7*C10))
                    K3s=R8/(R7*R3*R5*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R5):")
                    R5s=1.01*R5
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K3s=R8/(R7*R3*R5s*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R8):")
                    R8s=1.01*R8
                    fprs=(m.sqrt(R8s/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8s*C9/(R2*R3*R7*C10))
                    K3s=R8s/(R7*R3*R5*C9*C10)
                    ns,ds=getLPTT_ND(fprs, qprs, K3s)
                    draw_sensi('S(R8)',N,D,ns,ds,fp,var)
                
            elif typ=='Passe-Haut':
                [fp,qp,C]=Param(['fp','Qp','C=C9=C10'],100,p)
                sel+='(passe-haut)'
                R_optimal=1/(2*m.pi*fp*C)
                Rd=R_optimal
                C9=C
                C10=C
                R2=Rd
                R3=Rd
                R8=Rd
                R7=(R_optimal**2)/Rd
                R1=qp*m.sqrt(Rd*R7)
                R4=float('inf')
                R5=float('inf')
                R6=Rd
                K1=-R8/R6
                [R1m,R2m,R3m,R6m,R7m,R8m,C9m,C10m]=Result(['R1','R2','R3','R6','R7','R8','C9','C10'], [R1,R2,R3,R6,R7,R8,C9,C10],p)
                [R1m,R2m,R3m,R6m,R7m,R8m],[C9m,C10m]=standardisation(['R1','R2','R3','R6','R7','R8'], [R1m,R2m,R3m,R6m,R7m,R8m], ['C9','C10'], [C9m,C10m],p)
                fpr=(m.sqrt(R8m/(R2m*R3m*R7m*C9m*C10m)))/(2*m.pi)
                qpr=R1m*m.sqrt(R8m*C9m/(R2m*R3m*R7m*C10m))
                K1r=-R8m/R6m
                N,D=getHPTT_ND(fp, qp, K1)
                n,d=getHPTT_ND(fpr, qpr, K1r)
                plot=Aff(N, D,n,d,p)
                data=[fpr,qpr,R1m,R2m,R3m,R6m,R7m,R8m,C9m,C10m]
                name=['R1','R2','R3','R6','R7','R8','C9','C10']
                
                st.header("Analyse de sensibilité de Wp et Qp")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d1:
                    st.write("S(Qp):") 
                    fprs=fp
                    qprs=1.01*qp
                    ns,ds=getHPTT_ND(fprs, qprs, K1)
                    draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                    
                with d2:
                    st.write("S(Wp):")
                    fprs=fp*1.01
                    qprs=qp
                    ns,ds=getHPTT_ND(fprs, qprs, K1)
                    draw_sensi('S(Wp)',N,D,ns,ds,fp,var)

                
                st.header("Analyse de sensibilité des capacités")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d2:
                    
                    st.write("S(C10):")
                    C10s=1.01*C10
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10s)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10s))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(C10)',N,D,ns,ds,fp,var)
                    
                with d1:
                    st.write("S(C9):")
                    C9s=1.01*C9
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9s*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9s/(R2*R3*R7*C10))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(C9)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des résistances")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2,d3=sensi.columns([1,1,1])
                var=1
                with d3:
                    
                    st.write("S(R3):")
                    R3s=1.01*R3
                    fprs=(m.sqrt(R8/(R2*R3s*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3s*R7*C10))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R6):")
                    R6s=1.01*R6
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K1s=-R8/R6s
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                    
                with d1:
                    
                    st.write("S(R1):")
                    R1s=1.01*R1
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1s*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R4):")
                    R4s=1.01*R4
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R7):")
                    R7s=1.01*R7
                    fprs=(m.sqrt(R8/(R2*R3*R7s*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7s*C10))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R7)',N,D,ns,ds,fp,var)
                    
                with d2:
                    
                    st.write("S(R2):")
                    R2s=1.01*R2
                    fprs=(m.sqrt(R8/(R2s*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2s*R3*R7*C10))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R5):")
                    R5s=1.01*R5
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K1s=-R8/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R8):")
                    R8s=1.01*R8
                    fprs=(m.sqrt(R8s/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8s*C9/(R2*R3*R7*C10))
                    K1s=-R8s/R6
                    ns,ds=getHPTT_ND(fprs, qprs, K1s)
                    draw_sensi('S(R8)',N,D,ns,ds,fp,var) 
                
            elif typ=='Passe-Bande':
                sel+='(passe-bande)'
                [fp,qp,C]=Param(['fp','Qp','C=C9=C10'],100,p)
                
                R_optimal=1/(2*m.pi*fp*C)
                Rd=R_optimal
                C9=C
                C10=C
                R2=Rd
                R3=Rd
                R8=Rd
                R7=(R_optimal**2)/Rd
                R1=qp*m.sqrt(Rd*R7)
                R6=float('inf')
                R5=float('inf')
                R4=Rd
                K2=R8/(C9*R7*R4)
                [R1m,R2m,R3m,R4m,R7m,R8m,C9m,C10m]=Result(['R1','R2','R3','R4','R7','R8','C9','C10'], [R1,R2,R3,R4,R7,R8,C9,C10],p)
                [R1m,R2m,R3m,R4m,R7m,R8m],[C9m,C10m]=standardisation(['R1','R2','R3','R4','R7','R8'], [R1m,R2m,R3m,R4m,R7m,R8m], ['C9','C10'], [C9m,C10m],p)
                fpr=(m.sqrt(R8m/(R2m*R3m*R7m*C9m*C10m)))/(2*m.pi)
                qpr=R1m*m.sqrt(R8m*C9m/(R2m*R3m*R7m*C10m))
                K2r=R8m/(C9m*R7m*R4m)
                N,D=getBPTT_ND(fp, qp, K2)
                n,d=getBPTT_ND(fpr, qpr, K2r)
                plot=Aff(N, D,n,d,p)
                data=[fpr,qpr,R1m,R2m,R3m,R4m,R7m,R8m,C9m,C10m]
                name=['fp','Qp','R1','R2','R3','R4','R7','R8','C9','C10']
                
                st.header("Analyse de sensibilité de Wp et Qp")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d1:
                    st.write("S(Qp):") 
                    fprs=fp
                    qprs=1.01*qp
                    ns,ds=getBPTT_ND(fprs, qprs, K2)
                    draw_sensi('S(Qp)',N,D,ns,ds,fp,var)
                    
                with d2:
                    st.write("S(Wp):")
                    fprs=fp*1.01
                    qprs=qp
                    ns,ds=getBPTT_ND(fprs, qprs, K2)
                    draw_sensi('S(Wp)',N,D,ns,ds,fp,var)

                
                st.header("Analyse de sensibilité des capacités")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2=sensi.columns([1,1])
                var=1
                with d2:
                    
                    st.write("S(C10):")
                    C10s=1.01*C10
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10s)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10s))
                    K2s=R8/(C9*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(C10)',N,D,ns,ds,fp,var)
                    
                with d1:
                    st.write("S(C9):")
                    C9s=1.01*C9
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9s*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9s/(R2*R3*R7*C10))
                    K2s=R8/(C9s*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(C9)',N,D,ns,ds,fp,var)
                
                st.header("Analyse de sensibilité des résistances")
                sensi=st.expander('Afficher la sensibilité')
                d1,d2,d3=sensi.columns([1,1,1])
                var=1
                with d3:
                    
                    st.write("S(R3):")
                    R3s=1.01*R3
                    fprs=(m.sqrt(R8/(R2*R3s*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3s*R7*C10))
                    K2s=R8/(C9*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R6):")
                    R6s=1.01*R6
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K2s=R8/(C9*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                    
                with d1:
                    
                    st.write("S(R1):")
                    R1s=1.01*R1
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1s*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K2s=R8/(C9*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R4):")
                    R4s=1.01*R4
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K2s=R8/(C9*R7*R4s)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R7):")
                    R7s=1.01*R7
                    fprs=(m.sqrt(R8/(R2*R3*R7s*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7s*C10))
                    K2s=R8/(C9*R7s*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R7)',N,D,ns,ds,fp,var)
                    
                with d2:
                    
                    st.write("S(R2):")
                    R2s=1.01*R2
                    fprs=(m.sqrt(R8/(R2s*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2s*R3*R7*C10))
                    K2s=R8/(C9*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R5):")
                    R5s=1.01*R5
                    fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                    K2s=R8/(C9*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                    
                    st.write("S(R8):")
                    R8s=1.01*R8
                    fprs=(m.sqrt(R8s/(R2*R3*R7*C9*C10)))/(2*m.pi)
                    qprs=R1*m.sqrt(R8s*C9/(R2*R3*R7*C10))
                    K2s=R8s/(C9*R7*R4)
                    ns,ds=getBPTT_ND(fprs, qprs, K2s)
                    draw_sensi('S(R8)',N,D,ns,ds,fp,var) 
                
            elif typ=='Réjecteur de fréquence':
                sel+='(réjecteur de fréquence)'
                [fp,fz,qp,C]=Param(['fp','fz','Qp','C=C9=C10'],100,p)
                if fz==fp:
                    st.markdown(":warning: **fz doit être différente de fp**")
                else:
                    R_optimal=1/(2*m.pi*fp*C)
                    Rd=R_optimal
                    C9=C
                    C10=C
                    R2=Rd
                    R3=Rd
                    R4=Rd
                    R8=Rd
                    R7=(R_optimal**2)/Rd
                    R1=qp*m.sqrt(Rd*R7)
                    R6=R4*R7/R1
                    R5=R6/(((2*m.pi*fz)**2)*R3*R7*C9*C10)
                    K=-R8/R6
                    [R1m,R2m,R3m,R4m,R5m,R6m,R7m,R8m,C9m,C10m]=Result(['R1','R2','R3','R4','R5','R6','R7','R8','C9','C10'], [R1,R2,R3,R4,R5,R6,R7,R8,C9,C10],p)
                    [R1m,R2m,R3m,R4m,R5m,R6m,R7m,R8m],[C9m,C10m]=standardisation(['R1','R2','R3','R4','R5','R6','R7','R8'], [R1m,R2m,R3m,R4m,R5m,R6m,R7m,R8m], ['C9','C10'], [C9m,C10m],p)
                    
                    fpr=(m.sqrt(R8m/(R2m*R3m*R7m*C9m*C10m)))/(2*m.pi)
                    qpr=R1m*m.sqrt(R8m*C9m/(R2m*R3m*R7m*C10m))
                    fzr=(m.sqrt(R6m/(R3m*R5m*R7m*C9m*C10m)))/(2*m.pi)
                    Kr=-R8m/R6m
                    N,D=getBRTT_ND(fp, qp, K,fz)
                    n,d=getBRTT_ND(fpr, qpr, Kr,fzr)
                    plot=Aff(N, D,n,d,p)
                    data=[fzr,fpr,qpr,R1m,R2m,R3m,R4m,R5m,R6m,R7m,R8m,C9m,C10m]
                    name=['fz','fp','Qp','R1','R2','R3','R4','R5','R6','R7','R8','C9','C10']
                    
                    st.header("Analyse de sensibilité de Wp, Wz et Qp")
                    sensi=st.expander('Afficher la sensibilité')
                    d1,d2,d3=sensi.columns([1,1,1])
                    var=1
                    with d1:
                        st.write("S(Qp):") 
                        fprs=fp
                        qprs=1.01*qp
                        Ks=K
                        fzrs=fz
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(Qp)',N,D,ns,ds,fp,var)

                        
                    with d2:
                        st.write("S(Wp):")
                        fprs=fp*1.01
                        qprs=qp
                        Ks=K
                        fzrs=fz
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(Wp)',N,D,ns,ds,fp,var)
                        
                    with d3:
                                                
                        st.write("S(Wz):")
                        fprs=fp
                        qprs=qp
                        Ks=K
                        fzrs=fz*1.01
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(Wz)',N,D,ns,ds,fp,var)
                    
                    st.header("Analyse de sensibilité des capacités")
                    sensi=st.expander('Afficher la sensibilité')
                    d1,d2=sensi.columns([1,1])
                    var=1
                    with d2:
                        
                        st.write("S(C10):")
                        C10s=1.01*C10
                        fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10s)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10s))
                        fzrs=(m.sqrt(R6/(R3*R5*R7*C9*C10s)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(C10)',N,D,ns,ds,fp,var)
                        
                    with d1:
                        st.write("S(C9):")
                        C9s=1.01*C9
                        fprs=(m.sqrt(R8/(R2*R3*R7*C9s*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9s/(R2*R3*R7*C10))
                        fzrs=(m.sqrt(R6/(R3*R5*R7*C9s*C10)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(C9)',N,D,ns,ds,fp,var)
                    
                    st.header("Analyse de sensibilité des résistances")
                    sensi=st.expander('Afficher la sensibilité')
                    d1,d2,d3=sensi.columns([1,1,1])
                    var=1
                    with d3:
                        
                        
                        st.write("S(R3):")
                        R3s=1.01*R3
                        fprs=(m.sqrt(R8/(R2*R3s*R7*C9*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9/(R2*R3s*R7*C10))
                        fzrs=(m.sqrt(R6/(R3s*R5*R7*C9*C10)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R3)',N,D,ns,ds,fp,var)
                        
                        st.write("S(R6):")
                        R6s=1.01*R6
                        fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                        fzrs=(m.sqrt(R6s/(R3*R5*R7*C9*C10)))/(2*m.pi)
                        Ks=-R8/R6s
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R6)',N,D,ns,ds,fp,var)
                        
                    with d1:
                        
                        st.write("S(R1):")
                        R1s=1.01*R1
                        fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                        qprs=R1s*m.sqrt(R8*C9/(R2*R3*R7*C10))
                        fzrs=(m.sqrt(R6/(R3*R5*R7*C9*C10)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R1)',N,D,ns,ds,fp,var)
                        
                        st.write("S(R4):")
                        R4s=1.01*R4
                        fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                        fzrs=(m.sqrt(R6/(R3*R5*R7*C9*C10)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R4)',N,D,ns,ds,fp,var)
                        
                        st.write("S(R7):")
                        R7s=1.01*R7
                        fprs=(m.sqrt(R8/(R2*R3*R7s*C9*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9/(R2*R3*R7s*C10))
                        fzrs=(m.sqrt(R6/(R3*R5*R7s*C9*C10)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R7)',N,D,ns,ds,fp,var)
                        
                    with d2:
                        
                        st.write("S(R2):")
                        R2s=1.01*R2
                        fprs=(m.sqrt(R8/(R2s*R3*R7*C9*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9/(R2s*R3*R7*C10))
                        fzrs=(m.sqrt(R6/(R3*R5*R7*C9*C10)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R2)',N,D,ns,ds,fp,var)
                        
                        st.write("S(R5):")
                        R5s=1.01*R5
                        fprs=(m.sqrt(R8/(R2*R3*R7*C9*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8*C9/(R2*R3*R7*C10))
                        fzrs=(m.sqrt(R6/(R3*R5s*R7*C9*C10)))/(2*m.pi)
                        Ks=-R8/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R5)',N,D,ns,ds,fp,var)
                        
                        st.write("S(R8):")
                        R8s=1.01*R8
                        fprs=(m.sqrt(R8s/(R2*R3*R7*C9*C10)))/(2*m.pi)
                        qprs=R1*m.sqrt(R8s*C9/(R2*R3*R7*C10))
                        fzrs=(m.sqrt(R6/(R3*R5*R7*C9*C10)))/(2*m.pi)
                        Ks=-R8s/R6
                        ns,ds=getBRTT_ND(fprs, qprs, Ks,fzrs)
                        draw_sensi('S(R8)',N,D,ns,ds,fp,var) 
                        

    return sel,image,name,data,plot

