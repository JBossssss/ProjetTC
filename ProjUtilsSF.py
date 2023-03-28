# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:13:03 2023

@author: Loren
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:48:06 2023

@author: Loren
"""


'''SANS LES FORMS'''


import streamlit as st
import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from  matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams
import plotly


def Param(TAB,maxq,maxk=None):
    RET=[]
    h=0
    nc=0
    #case = st.container()
    c1,c2=st.columns([1,2])
    expander = c2.expander("Entrée des paramètres du filtre")
    col1, col2, col3 = expander.columns([1, 1, 1])
    for i in range(len(TAB)):
        stp=1.00
        form='%0.2f'
        if TAB[i][0]=='f':
            h=h+1
            Name='**Choix de '
            Name+=TAB[i]
            Name+='**'
            v=1000.00
            if h==2:
                v=2000.00
            maxv=None
            form=None
            unit='Hertz'
            c=col1
            stp=100.00
        elif  TAB[i][0]=='Q':
            Name='**Choix de Qp**'
            v=0.5
            maxv=float(maxq)
            form=None
            unit=''
            c=col1
        elif TAB[i][0]=='C':
            nc=nc+1
            Name='**Choix de '
            Name+=TAB[i]
            Name+='**'
            v=0.000001000
            if nc==1:
                v=0.000010000
            if nc==3:
                v=0.000000010
            stp=0.000001
            maxv=None
            form='%0.10f'
            unit='Farad'
            c=col2
        elif  TAB[i][0]=='K':
            Name='**Choix de '
            Name+=TAB[i]
            Name+='**'
            v=0.5
            stp=0.1
            if maxk!=None :
                maxv=float(maxk)
            form=None
            unit=''
            c=col3
        elif   TAB[i][0]=='R':
            Name='**Choix de '
            Name+=TAB[i]
            Name+='**'
            v=1000.00
            maxv=None
            form=None
            unit='ohm'
            c=col3
        with c2:    
            RET.append(c.number_input(Name,min_value=0.00,value=v,max_value=maxv,step=stp,format=form,key=i+50))
        with c1:
            st.write('Valeur de',TAB[i],': ',RET[i],unit)
    #case.form_submit_button('**Valider les données**:+1:')
            
    return RET

def Result(NAME,DATA):
    
        
    #res=st.form('résultats')
    st.header('Données calculées:')
    col1,col2=st.columns([1,2])
    data='data'
    modif=col2.expander('Modifier les données calculées')
    modif.write("Boutons + et - modifient la valeur par pas de 1%")
    d1,d2,d3=modif.columns([1,1,1])
    with open(data, 'w') as file:
        for i in range(len(NAME)):
            with col2:
                with modif:
                    f=i%3
                    if f==0: DATA[i]=d1.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.4f',step=0.01*DATA[i],key=i+20)
                    elif f==1 :DATA[i]=d2.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.4f',step=0.01*DATA[i],key=i+20)
                    else:DATA[i]=d3.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.4f',step=0.01*DATA[i],key=i+20)
            if NAME[i][0]=='C':
                Name='**'
                Name+=NAME[i]
                Name+=' =**'
                unit='Farad'
            elif  NAME[i][0]=='K':
                Name='**'
                Name+=NAME[i]
                Name+=' =**'
                unit=''
            elif   NAME[i][0]=='R':
                Name='**'
                Name+=NAME[i]
                Name+=' =**'
                unit='ohm'
            else:
                Name='**'
                Name+=NAME[i]
                Name+=' =**'
                unit=''
            with col1:     
                st.write(Name,DATA[i], unit) 
                file.write(Name)
                #file.write(DATA[i])
                file.write(unit)
    return DATA
            
       
        #res.form_submit_button('**Valider les données**:+1:')
    
        # with open(data, "rb") as file:
        #     dwl = st.download_button(
        #         label="Télécharger",
        #         data=DATA,
        #         file_name="DATA")
        
def Aff(N,D,n=None,d=None):
    expander=st.expander('Fonction de transfert et réponse fréquentielle')
        
    with expander:  
        chx=st.radio('Choisir de voir la fonction de transfert :', ['Théorique', 'Réelle, avec les composants calculés/choisis','Superposition'])
        G1,G2=expander.columns([1,1])
        if chx=='Superposition':
            with G1: st.write('''$$$Ht(p)=\dfrac{''',N[0],''' p^2+''',N[1],''' p+''',N[2],'''}{''',D[0],''' p^2+''',D[1],''' p+''',D[2],'''}$$$''',color=[0.5,0,0.5])
            with G2: st.write('''$$$Hr(p)=\dfrac{''',n[0],''' p^2+''',n[1],''' p+''',n[2],'''}{''',d[0],''' p^2+''',d[1],''' p+''',d[2],'''}$$$''',color='p')
            z=st.slider('Zoom (base 10)',0.0,5.0,2.0)
            w1=m.log10(m.sqrt(D[2]))+z+0.1
            w2=m.log10(m.sqrt(D[2]))-z-0.1
            a,b,c=expander.columns([1,2,1])
            with b:
                draw_supp(N, D, n, d, w1, w2)
        else: 
            if chx=='Théorique':
                NUM=N
                DEN=D
            else:
                NUM=n
                DEN=d
            st.markdown('**Fonction de transfert :**')
            st.write('''$$$H(p)=\dfrac{''',NUM[0],''' p^2+''',NUM[1],''' p+''',NUM[2],'''}{''',DEN[0],''' p^2+''',DEN[1],''' p+''',DEN[2],'''}$$$''')
            st.markdown('**Réponse fréquentielle :**')
            z=st.slider('Zoom (base 10)',0.0,5.0,2.0)
            #expander.form_submit_button('Actualiser')
            w1=m.log10(m.sqrt(DEN[2]))+z+0.1
            w2=m.log10(m.sqrt(DEN[2]))-z-0.1
            c1,c2=expander.columns([2,1])
            with c1:
                draw_repfreq('''H(p)''',NUM,DEN,w1,w2)
            with c2:
                zplane('P/Z',NUM,DEN,r=2.5)
    
def getLP_ND(fp,qp,k):
    wp=2*m.pi*fp
    N=[0,0,k*wp**2]
    D=[1,wp/qp,wp**2]
    return N,D
def getHP_ND(fp,qp,k):
    wp=2*m.pi*fp
    N=[k,0,0]
    D=[1,wp/qp,wp**2]
    return N,D
def getPB_ND(fp,qp,k):
    wp=2*m.pi*fp
    N=[0,k*wp/qp,0]
    D=[1,wp/qp,wp**2]
    return N,D
def getBR_ND(fp,qp,k,fz):
    wp=2*m.pi*fp
    wz=2*m.pi*fz
    N=[k,0,k*(wz**2)]
    D=[1,wp/qp,wp**2]
    return N,D
def getLPTT_ND(fp,qp,k3):
    wp=2*m.pi*fp
    N=[0,0,k3]
    D=[1,wp/qp,wp**2]
    return N,D
def getHPTT_ND(fp,qp,k1):
    wp=2*m.pi*fp
    N=[k1,0,0]
    D=[1,wp/qp,wp**2]
    return N,D
def getBPTT_ND(fp,qp,k2):
    wp=2*m.pi*fp
    N=[0,k2,0]
    D=[1,wp/qp,wp**2]
    return N,D
def getBRTT_ND(fp,qp,k,fz):
    wp=2*m.pi*fp
    wz=2*m.pi*fz
    N=[k,0,k*(wz**2)]
    D=[1,wp/qp,wp**2]
    return N,D

def draw_repfreq(leg,num, den, w_min, w_max):

    '''
    Dessine la réponse en fréquence du filtre en fonction des polynômes de H(p) = Num(p)/Den(p) entre
    les valeurs 10^w_min et 10^w_max. Ainsi, si w_min = 0 et w_max = 1, la courbe de Bode sera dressée
    entre 10^0 et 10^1 en échelle logarithmique

    Example : H(p) = (p+1)/(p+2) 
    inputs : num=[1,1], den=[1,2] (<= facteurs multiplicatifs du polynôme), w_min = 0, w_max = 1
    outputs : None
    '''
    fig,ax = plt.subplots(figsize=(10,5))
    
    # plt.figure()
    num = np.array(num) 
    den = np.array(den)

    wIn = np.logspace(w_min, w_max, 100)
    wOut, hOut = sc.freqs(num, den, wIn)
    fOut=wOut/(2*m.pi)
    plt.semilogx(fOut, 20*np.log10(np.abs(hOut)))
    plt.xlabel('Fréquence [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.legend([leg])
    plt.show()
    st.pyplot(fig,ax)
def draw_supp(num, den,N,D,w_min, w_max):

    '''
    Dessine la réponse en fréquence du filtre en fonction des polynômes de H(p) = Num(p)/Den(p) entre
    les valeurs 10^w_min et 10^w_max. Ainsi, si w_min = 0 et w_max = 1, la courbe de Bode sera dressée
    entre 10^0 et 10^1 en échelle logarithmique

    Example : H(p) = (p+1)/(p+2) 
    inputs : num=[1,1], den=[1,2] (<= facteurs multiplicatifs du polynôme), w_min = 0, w_max = 1
    outputs : None
    '''
    fig,ax = plt.subplots(figsize=(10,5))
    
    # plt.figure()
    num = np.array(num) 
    den = np.array(den)
    N=np.array(N)
    D=np.array(D)
    wIn = np.logspace(w_min, w_max, 100)
    wOut, hOut = sc.freqs(num, den, wIn)
    w2,h2=sc.freqs(N, D,wIn)
    
    plt.semilogx(wOut, 20*np.log10(np.abs(hOut)),color=[0.5,0,0.5])
    plt.semilogx(w2,20*np.log10(np.abs(h2)),color=[1,0.5,0])
    plt.xlabel('Fréquence [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.legend(['Courbe Théorique','Courbe Réelle'])
    plt.show()
    st.pyplot(fig,ax)

def zplane(leg,num,den,r=2.5,filename=None):

    """Plot the complex z-plane given a transfer function.
    inputs :
    - num, den (<= facteurs multiplicatifs du polynôme)
    - r (<= échelle de la figure)
    - filename (<= nom de la figure à sauvegarder. Si =None, l'affiche et ne la sauvegarde pas)
    outputs : zéros, pôles, k (facteur multiplicatif)

    """
    r=max(num[2],den[2])
    if num[0]!=0.00:
        r=max(num[2]/num[0],den[2])
    r=m.sqrt(r)*1.1
    fig,ax = plt.subplots(figsize=(6,4))
    b = np.array(num)
    a = np.array(den)
    # get a figure/plot
    ax = plt.subplot(111)

    # create the unit circle
    # uc = patches.Circle((0,0), radius=1, fill=False,
    #                     color='black', ls='dashed')
    # ax.add_patch(uc)

    # The coefficients are less than 1, normalize the coeficients
    # if np.max(b) > 1:
    #     kn = np.max(b)
    #     b = b/float(kn)
    # else:
    #     kn = 1

    # if np.max(a) > 1:
    #     kd = np.max(a)
    #     a = a/float(kd)
    # else:
    #     kd = 1
        
    # Get the poles and zeros
    p = np.roots(a)
    z = np.roots(b)
    k = 1
    # Plot the zeros and set marker properties    
    t1 = plt.plot(z.real, z.imag, 'go', ms=10)
    plt.setp( t1, markersize=10.0, markeredgewidth=1.0,
              markeredgecolor='k', markerfacecolor='g')

    # Plot the poles and set marker properties
    t2 = plt.plot(p.real, p.imag, 'rx', ms=10)
    plt.setp( t2, markersize=12.0, markeredgewidth=3.0,
              markeredgecolor='r', markerfacecolor='r')

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # for i in range(len(z)):
    #     maxzreal=0
    #     if z.real(i)>=maxzreal:
    #         maxzreal=z.real(i)
    # for i in range(len(z)):
    #     maxzimag=0
    #     if z.imag(i)>=maxzimag:
    #         maxzimag=z.imag(i)
    # for i in range(len(p)):
    #     maxpimag=0
    #     if p.imag(i)>=maxpimag:
    #         maxpimag=p.imag(i)
    # for i in range(len(p)):
    #     maxpreal=0
    #     if p.real(i)>=maxpreal:
    #         maxpreal=p.real(i)
    
    # absc=max(maxzreal,maxpreal)*1.1
    # ordo=max(maxzimag,maxpimag)*1.1
    
    plt.axis('scaled')
    plt.axis([-r,r,-r,r])
    # ticks = [-2*r,-1.5*r,-1*r,-0.5*r,0.5*r,1*r,1.5*r]; plt.xticks(ticks); plt.yticks(ticks)
    # absc=max(z.real.all(),p.real.all())*10
    # ordo=max(z.imag.all(),p.imag.all())*10
    # st.write(absc,ordo,'pute')
    # plt.axis('scaled')
    # plt.axis([-ordo,ordo, -ordo, ordo])

    if filename is None:
        plt.title(leg)
        plt.show()
    else:
        plt.savefig(filename)
    st.pyplot(fig,ax)
    return z,p,k             

def zplanesupp(leg,num,den,N,D,r=2.5,filename=None):

    """Plot the complex z-plane given a transfer function.
    inputs :
    - num, den (<= facteurs multiplicatifs du polynôme)
    - r (<= échelle de la figure)
    - filename (<= nom de la figure à sauvegarder. Si =None, l'affiche et ne la sauvegarde pas)
    outputs : zéros, pôles, k (facteur multiplicatif)

    """
    r=max(num[len(num)-1]/(num[0]+0.0001),den[len(den)-1]/den[0])
    r=m.sqrt(r)+0.05*m.sqrt(r)
    fig,ax = plt.subplots(figsize=(6,4))
    b = np.array(num)
    a = np.array(den)
    # get a figure/plot
    ax = plt.subplot(111)

    # create the unit circle
    # uc = patches.Circle((0,0), radius=1, fill=False,
    #                     color='black', ls='dashed')
    # ax.add_patch(uc)

    # The coefficients are less than 1, normalize the coeficients
    if np.max(b) > 1:
        kn = np.max(b)
        b = b/float(kn)
    else:
        kn = 1

    if np.max(a) > 1:
        kd = np.max(a)
        a = a/float(kd)
    else:
        kd = 1
        
    # Get the poles and zeros
    p = np.roots(a)
    z = np.roots(b)
    k = kn/float(kd)
    # Plot the zeros and set marker properties    
    t1 = plt.plot(z.real, z.imag, 'go', ms=10)
    plt.setp( t1, markersize=10.0, markeredgewidth=1.0,
              markeredgecolor='k', markerfacecolor='g')

    # Plot the poles and set marker properties
    t2 = plt.plot(p.real, p.imag, 'rx', ms=10)
    plt.setp( t2, markersize=12.0, markeredgewidth=3.0,
              markeredgecolor='r', markerfacecolor='r')

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.axis('scaled')
    plt.axis([-r,r, -r, r])
    #ticks = [-2*r,-1.5*r,-1*r,-0.5*r,0.5*r,1*r,1.5*r]; plt.xticks(ticks); plt.yticks(ticks)

    if filename is None:
        plt.title(leg)
        plt.show()
    else:
        plt.savefig(filename)
    st.pyplot(fig,ax)
    print(z,p)
    return z,p,k             