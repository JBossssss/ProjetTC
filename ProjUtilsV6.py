
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
def normalisation(Name1,dat1,Name2,dat2):
    if st.checkbox('Normaliser les composants',key=Name1):
        TEST1=[0.0000001,0.000001,0.001,0.1,1,10,100,1000,10000]
        TEST2=[0.0000005,0.000005,0.0005,0.05,1,5,50,500,5000,50000]
        d0,d1,d2,d3=st.columns([3,2,2,3])        
        # RES=d1.form('huluberlu')
        # CAP=d2.form('kiki')
        with d1:     
            st.markdown('**Résistances**')
            cR=st.radio('Choissisez votre table :',['TEST 1','TEST 2'],key=80)
            if cR=='TEST 1': VR=TEST1
            if cR=='TEST 2': VR=TEST2
            # st.form_submit_button('Valider')
            dat1,dat2=cp_norm(Name1,dat1,Name2,dat2, VR,'R')
            tab11,tab12=st.columns([1,2])           
            for i in range(len(Name1)):
                if Name1[i][0]=='R':
                    tab11.write(Name1[i])
                    tab12.write(dat1[i],format='%0.2f')   
            for i in range(len(Name2)):
                if Name2[i][0]=='R':
                    tab11.write(Name2[i])
                    tab12.write(dat2[i],format='%0.2f')
                    
        with d2:    
            
            st.markdown('**Capacités**')
            cC=st.radio('Choissisez votre table :',['TEST 1 ','TEST 2 '],key=95)
            if cC=='TEST 1 ': VC=TEST1
            if cC=='TEST 2 ': VC=TEST2
            dat1,dat2=cp_norm(Name1,dat1,Name2,dat2, VC,'C')
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


def cp_norm(name1, dat1, name2, dat2, v2, typ):
    v2_array = np.array(v2)
    dat1 = list(dat1)
    dat2 = list(dat2)
    for i in range(len(name1)):
        if name1[i][0] == typ:
            dat1[i] = v2_array[np.abs(v2_array - dat1[i]).argmin()]
    for i in range(len(name2)):
        if name2[i][0] == typ:
            dat2[i] = v2_array[np.abs(v2_array - dat2[i]).argmin()]
    return tuple(dat1), tuple(dat2)

def warning(leg):
    c1,c2=st.columns([1,20])
    c1.write(':warning:')
    c2.markdown(f'<p style="color:red">{leg}</p>', unsafe_allow_html=True) 