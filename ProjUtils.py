# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 09:48:06 2023

@author: Loren
"""

import streamlit as st
import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc
from  matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams
import plotly


def Param(TAB,maxq):
    RET=[]
    case = st.form(key="form_settings")
    expander = case.expander("Entrée des paramètres du filtre")
    col1, col2, col3 = expander.columns([1, 1, 1])
    for i in range(len(TAB)):
        stp=1.00
        if TAB[i][0]=='f':
            Name='**Choix de '
            Name+=TAB[i]
            Name+='**'
            v=1000.00
            maxv=None
            form=None
            unit='Hertz'
            c=col1
        elif  TAB[i][0]=='Q':
            Name='**Choix de Qp**'
            v=1.00
            maxv=float(maxq)
            form=None
            unit=''
            c=col1
        elif TAB[i][0]=='C':
            Name='**Choix de '
            Name+=TAB[i]
            Name+='**'
            v=0.0000000001
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
            maxv=None
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
        
        RET.append(c.number_input(Name,min_value=0.00,value=v,max_value=maxv,step=stp,format=form,key=i+50,))
        with case :
            st.write('Valeur de',TAB[i],': ',RET[i],unit)
            
    case.form_submit_button('**Valider les données**:+1:')
  
    return RET

def Result(NAME,DATA,NUM,DEN):
    res=st.form('résultats')
    res.header('Données calculées:')
    data='data'
    with open(data, 'w') as file:
        for i in range(len(NAME)):
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
            with res:    
                st.write(Name,DATA[i], unit) 
                file.write(Name)
                #file.write(DATA[i])
                file.write(unit)
        expander=res.expander('Voir plus')
        c1,c2=expander.columns([1,1])
        with expander:
            st.markdown('**Réponse fréquentielle :**')
            z=st.slider('Zoom (base 10)',0.0,5.0,2.0)
            expander.form_submit_button('Actualiser')
            w1=m.log10(m.sqrt(DEN[2]))+z+0.1
            w2=m.log10(m.sqrt(DEN[2]))-z-0.1
            draw_repfreq('Rep freq',NUM,DEN,w1,w2)
            zplane('P/Z',NUM,DEN,r=2.5)
    res.form_submit_button('**Valider les données**:+1:')

    # with open(data, "rb") as file:
    #     dwl = st.download_button(
    #         label="Télécharger",
    #         data=DATA,
    #         file_name="DATA")
    
def getLP_ND(fp,qp,k):
    N=[]
    D=[]
    N.append(k*fp**2)
    
    D.append(1)
    D.append(fp/qp)
    D.append(fp**2)
    return N,D
def getHP_ND(fp,qp,k):
    N=[]
    D=[]
    N.append(k)
    N.append(0)
    N.append(0)
    D.append(1)
    D.append(fp/qp)
    D.append(fp**2)
    return N,D
def getPB_ND(fp,qp,k):
    N=[]
    D=[]
    N.append(0)
    N.append(k*fp/qp)
    N.append(0)
    D.append(1)
    D.append(fp/qp)
    D.append(fp**2)
    return N,D
def getBR_ND(fp,qp,k,fz):
    N=[]
    D=[]
    N.append(k)
    N.append(0)
    N.append(k*(fz**2))
    D.append(1)
    D.append(fp/qp)
    D.append(fp**2)
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
    
    plt.semilogx(wOut, 20*np.log10(np.abs(hOut)))
    plt.xlabel('Fréquence [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.legend([leg])
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
