
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
    c1.header('Paramètre du filtre')
    c2.subheader("Entrée des paramètres du filtre")
    col1, col2, col3 = c2.columns([1, 1, 1])
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
            v=float(maxq*0.75)
            maxv=True
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
            RET.append(c.number_input(Name,min_value=0.00,value=v,step=stp,format=form,key=i+50))
        with c1:
            st.write('Valeur de',TAB[i],': ',RET[i],unit)
        if maxv==True:
            if RET[i]>maxq:
                warning('Le Q est supérieur à la valeur recommandée')
    #case.form_submit_button('**Valider les données**:+1:')
            
    return RET
def Result(NAME,DATA):
    
        
    #res=st.form('résultats')
    st.header('Données calculées:')
    col1,col2=st.columns([1,2])
    data='data'
    modif=col2.expander('Modifier les données calculées')
    modif.caption("Boutons + et - modifient la valeur par pas de 1%")
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
def standardisation(Name1,dat1,Name2,dat2):
    if st.checkbox('**Standardiser les composants**',key=Name1):
        with st.sidebar:
            # d0,d1,d2,d3=st.columns([2,2,2,3])        
            # with d1:     
            st.markdown('**Résistances**')
            series1=st.radio('Choissisez votre série de standadisation (précision) :',['E12 (+10%)','E24 (+-5%)','E48 (+-2%)'],key=80)
            # st.form_submit_button('Valider')
            dat1,dat2=cp_norm(Name1,dat1,Name2,dat2,'R',series1)
            tab11,tab12=st.columns([1,2])           
            for i in range(len(Name1)):
                if Name1[i][0]=='R':
                    tab11.write(Name1[i])
                    tab12.write(dat1[i],format='%0.2f')   
            for i in range(len(Name2)):
                if Name2[i][0]=='R':
                    tab11.write(Name2[i])
                    tab12.write(dat2[i],format='%0.2f')
                    
            # with d2:    
            
            st.markdown('**Capacités**')
            series2=st.radio('Choissisez votre série de standadisation (précision) :',['E12 (+20%)','E24 (+-10%)','E48 (+-5%)'],key=95)
            dat1,dat2=cp_norm(Name1,dat1,Name2,dat2,'C',series2)
            #st.form_submit_button('Valider') 
            tab21,tab22=st.columns([1,2])            
            for i in range(len(Name1)):
                if Name1[i][0]=='C':
                    tab21.write(Name1[i])
                    tab22.write(dat1[i],format='%0.6f')
            for i in range(len(Name2)):
                if Name2[i][0]=='C':
                    tab21.write(Name2[i])
                    tab22.write(dat2[i],format='%0.6f')   
            # with d3:
            st.write('')
            st.caption("E12: circuits audio,vidéo et de puissance")
            st.caption("E24: applications de précision (instruments de mesure, les circuits de commande de précision et les amplificateurs audio de haute qualité)\n")
            st.caption("E48: applications de précision extrême (telles que les oscillateurs, les filtres actifs et les circuits de traitement du signal)")
                     
    return dat1,dat2


def Aff(N,D,n=None,d=None):
    st.header('Fonction de transfert et réponse fréquentielle') 
    #chx=st.radio('Choisir de voir la fonction de transfert :', ['Théorique', 'Réelle, avec les composants calculés/choisis','Superposition'])
    G1,G2=st.columns([1,1])
    with G1: Write_fnT(N, D)
    with G2: Write_fnT(n,d)    
    z=G1.slider('Zoom (base 10)',0.0,5.0,2.0)
    w1=m.log10(m.sqrt(D[2]))+z+0.1
    w2=m.log10(m.sqrt(D[2]))-z-0.1
    a,b=st.columns([2,1])
    with a:
        draw_supp(N, D, n, d, w1, w2)
    with b:
        zplanesupp('', N, D, n, d)
def Write_fnT(N,D):
    N_str=''
    D_str=''
    for i in range(len(N)-1):
        if N[i]!=0:
            N_str+=f"{N[i]} p^{len(N)-i-1} + "
        if D[i]!=0:
            D_str+=f"{D[i]} p^{len(N)-i-1} + "
    N_str+=f"{N[2]}"
    D_str+=f"{D[2]}"
    st.write('''$$$H(p) = \dfrac{''',N_str,'''}{''',D_str,'''}$$$''')
    
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
    r=max(num[2],den[2],N[2],D[2])
    if num[0]!=0.00:
        r=max(num[2]/num[0],den[2],N[2]/N[0],D[2])
    r=m.sqrt(r)*1.1
    fig,ax = plt.subplots(figsize=(6,4))
    b = np.array(num)
    a = np.array(den)
    d = np.array(N)
    c = np.array(D)
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
    if np.max(c) > 1:
        kv = np.max(c)
        c= c/float(kv)
    else:
        kc=1
    if np.max(d) > 1:
        kf = np.max(d)
        d = d/float(kf)
    else:
        kf = 1

        
    # Get the poles and zeros
    p = np.roots(a)
    z = np.roots(b)
    k = kn/float(kd)
    p2= np.roots(c)
    z2 =np.roots(d)
    
    # Plot the zeros and set marker properties    
    t1 = plt.plot(z.real, z.imag, 'go', ms=10)
    plt.setp( t1, markersize=10.0, markeredgewidth=1.0,
              markeredgecolor=[0.5,0,0.5], markerfacecolor=[0.5,0,0.5])

    # Plot the poles and set marker properties
    t2 = plt.plot(p.real, p.imag, 'rx', ms=10)
    plt.setp( t2, markersize=12.0, markeredgewidth=3.0,
              markeredgecolor=[0.5,0,0.5], markerfacecolor=[0.5,0,0.5])
    
    t3 = plt.plot(z2.real, z2.imag, 'go', ms=10)
    plt.setp( t3, markersize=10.0, markeredgewidth=1.0,
              markeredgecolor=[1,0.5,0], markerfacecolor=[1,0.5,0])

    # Plot the poles and set marker properties
    t4 = plt.plot(p2.real, p2.imag, 'rx', ms=10)
    plt.setp( t4, markersize=12.0, markeredgewidth=3.0,
              markeredgecolor=[1,0.5,0], markerfacecolor=[1,0.5,0])

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

def sauvegarder(k):
    col1,col2=st.columns([1,2])
    with col2:
        if st.checkbox('Sauvegarder ce filtr,e',key=k):
            return True
def save_side(sel,Ld,Wd,Lt,Wt,p):

    st.write('Filtre ',p)
    SEL='**'
    SEL+=sel
    SEL+='**'
    st.write(sel)
    exp=st.expander('Données')
    with exp:
        for i in range(len(Ld)):
            if Ld[i][0]=='C':
                Name='**'
                Name+=Ld[i]
                Name+=' =**'
                unit='Farad'
            elif  Ld[i][0]=='K':
                Name='**'
                Name+=Ld[i]
                Name+=' =**'
                unit=''
            elif   Ld[i][0]=='R':
                Name='**'
                Name+=Ld[i]
                Name+=' =**'
                unit='ohm'
            elif   Ld[i][0]=='f':
                Name='**'
                Name+=Ld[i]
                Name+=' =**'
                unit='hertz'
            else:
                Name='**'
                Name+=Ld[i]
                Name+=' =**'
                unit=''
            st.write(Name,Wd[i], unit)
        for i in range(len(Lt)):
            
            if Lt[i][0]=='C':
                Name='**'
                Name+=Lt[i]
                Name+=' =**'
                unit='Farad'
            elif  Lt[i][0]=='K':
                Name='**'
                Name+=Lt[i]
                Name+=' =**'
                unit=''
            elif   Lt[i][0]=='R':
                Name='**'
                Name+=Lt[i]
                Name+=' =**'
                unit='ohm'
            else:
                Name='**'
                Name+=Lt[i]
                Name+=' =**'
                unit=''
            st.write(Name,Wt[i], unit)
    p=p+1
    return p


def cp_norm(name1, dat1, name2, dat2, typ,series):

    dat1 = list(dat1)
    dat2 = list(dat2)
    for i in range(len(name1)):
        if name1[i][0] == typ:
            if typ=='R':
                dat1[i] = standardize_resistor(dat1[i], series)
            if typ=='C':
                dat1[i] = standardize_capacitor(dat1[i], series)
    for i in range(len(name2)):
        if name2[i][0] == typ:
            if typ=='R':
                dat2[i] = standardize_resistor(dat2[i], series)
            if typ=='C':
                dat2[i] = standardize_capacitor(dat2[i], series)
    return tuple(dat1), tuple(dat2)

def standardize_resistor(r, series):
    """Standardize a resistor value using a given E-series.
    
    Args:
        r (float): the resistor value to be standardized, in ohms
        series (str): the E-series to use. Default is 'E24'.
    
    Returns:
        float: the standardized resistor value, in ohms
        
    """
    E12_VALUES = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]
    E24_VALUES = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91]
    E48_VALUES = [10, 10.2, 10.5, 10.7, 11, 11.3, 11.5, 12, 12.1, 12.4, 12.7, 13, 13.3, 13.7, 14, 14.3,
                      15, 15.4, 15.8, 16.2, 16.5, 17, 17.4, 18, 18.2, 18.7, 19.1, 19.6, 20, 20.5, 21, 21.5, 22, 
                      22.6, 23.2, 23.7, 24.3, 24.9, 25.5, 26.1, 27, 27.4, 28.7, 29.4, 30.1, 30.9, 31.6, 32.4, 33, 33.2,
                      34.8, 35.7, 36.5, 37.4, 38.3, 39, 39.2, 40.2, 41.2, 42.2, 43.2, 44.2, 45.3, 46.4, 47.5, 48.7, 49.9,
                      51.1, 52.3, 53.6, 54.9, 56.2, 57.6, 59, 60.4, 61.9, 63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2, 75, 76.8, 
                      78.7, 80.6, 82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6]
    # Define the chosen E-series
    if series[:3] == 'E12':
        values = E12_VALUES
    elif series[:3] == 'E24':
        values = E24_VALUES
    elif series[:3] == 'E48':
        values = E48_VALUES
    else:
        raise ValueError("Invalid E-series")
    i=0
    j=0
    while(r<9.85):
        r=r*10
        i=i-1
    while(r>96.86):
        r=r/10
        j=j+1
            
    # Find the nearest standard value in the E-series
    closest_value = min(values, key=lambda x: abs(x-r))
    
    # Calculate the normalized value
    normalized_value = r / closest_value
    
    # Choose the normalized value closest to 1.0
    normalized_values = [1.0]
    normalized_values.extend([i/10 for i in range(2, 10)])
    normalized_values.extend([i/100 for i in range(10, 100, 10)])
    normalized_values.extend([i/1000 for i in range(100, 1000, 100)])
    normalized_values.extend([i/10000 for i in range(1000, 10000, 1000)])
    closest_normalized_value = min(normalized_values, key=lambda x: abs(x-normalized_value))
    
    # Calculate the standardized value
    standardized_value = closest_value * closest_normalized_value*10**j*10**i
    
    return standardized_value

def standardize_capacitor(c, series):
    """Standardize a capacitor value using a given E-series.
    
    Args:
        c (float): the capacitor value to be standardized, in farads
        series (str): the E-series to use. Default is 'E6'.
    
    Returns:
        float: the standardized capacitor value, in farads
    """
    E12_VALUES = [100, 120, 150, 180, 220, 270, 330, 390, 470, 560, 680, 820]
    E24_VALUES = [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910]
    E48_VALUES = [100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301,
                              316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909]
    # Define the chosen E-series
    
    if series[:3] == 'E12':
        values = E12_VALUES
    elif series[:3] == 'E24':
        values = E24_VALUES
    elif series[:3] == 'E48':
        values = E48_VALUES
    else:
        raise ValueError("Invalid E-series")
    i=0
    j=0
    while(c<95):
        c=c*10
        i=i-1
    while(c>960):
        c=c/10
        j=j+1

    # Find the nearest standard value in the E-series
    closest_value = min(values, key=lambda x: abs(x-c))
    
    # Calculate the normalized value
    normalized_value = c / closest_value
    
    # Choose the normalized value closest to 1.0
    normalized_values = [1.0]
    normalized_values.extend([i/10 for i in range(2, 10, 2)])
    closest_normalized_value = min(normalized_values, key=lambda x: abs(x-normalized_value))
    
    # Calculate the standardized value
    standardized_value = closest_value * closest_normalized_value*10**j*10**i
    
    return standardized_value


def warning(leg):
    c1,c2=st.columns([1,20])
    c1.write(':warning:')
    c2.markdown(f'<p style="color:red">{leg}</p>', unsafe_allow_html=True) 
