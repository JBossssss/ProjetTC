
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
from fpdf import FPDF



def Param(TAB,maxq,p,maxk=None):
    p=p+150*p
    RET=[]
    h=0
    nc=0
    #case = st.container()
    c1,c2=st.columns([1,2])
    c1.header('Paramètres du filtre')
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
            unit='Farads'
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
            unit='Ohms'
            c=col3
        with c2:    
            RET.append(c.number_input(Name,min_value=0.00,value=v,step=stp,format=form,key=p+i))
        with c1:
            st.write('Valeur de',TAB[i],': ',RET[i],unit)
        if maxv==True:
            if RET[i]>maxq:
                warning('Le Q est supérieur à la valeur recommandée')
    #case.form_submit_button('**Valider les données**:+1:')
            
    return RET
def Result(NAME,DATA,p):
    
    p=p+402*p
    st.header('Données calculées:')
    col1,col2=st.columns([1,2])
    data='data'
    modif=col2.expander('Modifier les données calculées')
    modif.caption("Boutons + et - modifient la valeur par pas de 1%")
    d1,d2,d3=modif.columns([1,1,1])
    with open(data, 'w') as file:
        for i in range(len(NAME)):
            with col2:
                if  NAME[i][0]=='K':
                    pass
                elif NAME[i][0]=='C':
                    with modif:
                        f=i%3
                        if f==0: DATA[i]=d1.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.11f',step=0.01*DATA[i],key=p+i)
                        elif f==1 :DATA[i]=d2.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.11f',step=0.01*DATA[i],key=p+i)
                        else:DATA[i]=d3.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.11f',step=0.01*DATA[i],key=p+i)
                else:
                    with modif:
                        f=i%3
                        if f==0: DATA[i]=d1.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.2f',step=0.01*DATA[i],key=p+i)
                        elif f==1 :DATA[i]=d2.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.2f',step=0.01*DATA[i],key=i+p)
                        else:DATA[i]=d3.number_input(NAME[i],min_value=0.00,value=float(DATA[i]),format='%0.2f',step=0.01*DATA[i],key=i+p)
            if NAME[i][0]=='C':
                Name='**'
                Name+=NAME[i]
                Name+=' =**'
                unit='Farads'
            elif  NAME[i][0]=='K':
                Name='**'
                Name+=NAME[i]
                Name+=' =**'
                unit=''
            elif   NAME[i][0]=='R':
                Name='**'
                Name+=NAME[i]
                Name+=' =**'
                unit='Ohms'
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

def Aff(N,D,n,d,p):
    p=p+401*p
    st.header('Fonction de transfert et réponse fréquentielle') 
    G1,G2=st.columns([1,1])
    with G1: 
        st.subheader('Théorique')
        st.write('fp = ',m.sqrt(D[2]))
        st.write('Qp = ',m.sqrt(D[2])*D[1])
        Write_fnT(N, D)
    with G2: 
        st.subheader('Réelle')
        st.write('fp = ',m.sqrt(d[2]))
        st.write('Qp = ',m.sqrt(d[2])*d[1])
        Write_fnT(n,d)    
    z=G1.slider('Zoom (base 10)',0.0,5.0,2.0,key=p)
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
    
    plt.semilogx(wOut/(2*m.pi), 20*np.log10(np.abs(hOut)),color=[0.5,0,0.5])
    plt.semilogx(w2/(2*m.pi),20*np.log10(np.abs(h2)),color=[1,0.5,0])
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

def sauvegarder(p):
    col1,col2=st.columns([7,2])
    with col2:
        if st.checkbox('**Sauvegarder ce filtre**',key=p+23458):
            return True
def download_pdf(DATA):
    # Création du PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",style='B', size=12)
    
    for j in range(len(DATA)):
        if j != 0:
            pdf.add_page()  # Ajouter une nouvelle page pour chaque itération sauf la première
        p=1
        [sel,image,name1, dat1, p]=DATA[j]
    
        text='FILTRE '
        text+=str(p)
        text+="\n"
        text+=sel
        pdf.cell(1, 20, str(text), ln=True)
        pdf.set_draw_color(0, 0, 0)  # Couleur du trait: noir
        pdf.line(pdf.x, pdf.y + 10, pdf.x + pdf.get_string_width("Mon texte souligné"), pdf.y + 10)  # Dessine une ligne sous le texte
        pdf.ln()
        
        # Ajout de l'image
        pdf.image(image, x=35, y=175, w=150, h=100)
        
        # Liste des données
    
        for i in range(len(name1)):
            if name1[i][0]=='C':
                Name=name1[i]
                Name+=' = '
                unit=' Farad'
            elif  name1[i][0]=='K':
                Name=name1[i]
                Name+=' = '
                unit=''
            elif   name1[i][0]=='R':
                
                Name=name1[i]
                Name+=' =  '
                unit=' ohm'
            elif   name1[i][0]=='f':
                
                Name=name1[i]
                Name+=' =  '
                unit=' hertz'
            else:
                Name=name1[i]
                Name+=' = '
                unit=''
            text=Name
            text+=str(dat1[i])
            text+=unit
            pdf.cell(0, 10, str(text), ln=True)
    
    # Sauvegarde du PDF
    pdf.output("data.pdf")

    # Téléchargement du PDF
    
    with open("data.pdf", "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="Télécharger le PDF",
        data=pdf_bytes,
        file_name="data.pdf",
        mime="application/pdf",
        key=DATA
    )

def save_side(sel,image,name1,dat1,p):

    filtre="Filtre "
    filtre+=str(p)
    st.header(filtre)
    SEL='**'
    SEL+=sel
    SEL+='**'
    st.write(sel)
    st.write('Données')
    for i in range(len(name1)):
        if name1[i][0]=='C':
            Name='**'
            Name+=name1[i]
            Name+=' =**'
            unit='Farad'

        elif   name1[i][0]=='R':
            Name='**'
            Name+=name1[i]
            Name+=' =**'
            unit='ohm'
        elif   name1[i][0]=='f':
            Name='**'
            Name+=name1[i]
            Name+=' =**'
            unit='hertz'
        else:
            Name='**'
            Name+=name1[i]
            Name+=' =**'
            unit=''
        st.write("<small>",Name,dat1[i], unit,"</small>", unsafe_allow_html=True)

def standardisation(name1,dat1,name2,dat2,p):
    
    p=p+701*p
    if st.checkbox('**Standardiser les composants**',key=p):
            #with st.sidebar:
            d0,d1,d2,d3=st.columns([2,2,2,3])        
            with d1:     
                st.markdown('**Résistances**')
                series1=st.radio('Choissisez votre série de standadisation (précision) :',['E24 (+-5%)','E48 (+-2%)','E96 (+-1%)'],key=dat1)
            
                dat1,dat2=cp_norm(name1,dat1,name2,dat2,'R',series1)
                tab11,tab12=st.columns([1,2])           
                for i in range(len(name1)):
                    if name1[i][0]=='R':
                        tab11.write(name1[i])
                        tab12.write(dat1[i],format='%0.2f')   
                for i in range(len(name2)):
                    if name2[i][0]=='R':
                        tab11.write(name2[i])
                        tab12.write(dat2[i],format='%0.2f')
                    
            with d2:    
            
                st.markdown('**Capacités**')
                series2=st.radio('Choissisez votre série de standadisation (précision) :',['E24 (+-10%)','E48 (+-5%)','E96 (+-2%)'],key=dat2)
                dat1,dat2=cp_norm(name1,dat1,name2,dat2,'C',series2)
                #st.form_submit_button('Valider') 
                tab21,tab22=st.columns([1,2])            
                for i in range(len(name1)):
                    if name1[i][0]=='C':
                        tab21.write(name1[i])
                        tab22.write(dat1[i],format='%0.6f')
                for i in range(len(name2)):
                    if name2[i][0]=='C':
                        tab21.write(name2[i])
                        tab22.write(dat2[i],format='%0.6f')
    return dat1,dat2

def cp_norm(name1, dat1, name2, dat2, typ,series):

    for i in range(len(name1)):
        if name1[i][0] == typ:
            if typ=='R':
                dat1[i] = standardize(dat1[i], series,'R')
            if typ=='C':
                dat1[i] = standardize(dat1[i], series,'C')
    for i in range(len(name2)):
        if name2[i][0] == typ:
            if typ=='R':
                dat2[i] = standardize(dat2[i], series,'R')
            if typ=='C':
                dat2[i] = standardize(dat2[i], series,'C')
    return dat1,dat2
   
def standardize(c, series,typ):
   
    if typ=='R':
        vmax=1e7
        vmin=1
    elif typ=='C':
        vmax=10
        vmin=1e-13
       
    E24_VALUES = [100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300, 330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910]
    E48_VALUES = [ 100, 105, 110, 115, 121, 127, 133, 140, 147, 154, 162, 169, 178, 187, 196, 205, 215, 226, 237, 249, 261, 274, 287, 301, 316, 332, 348, 365, 383, 402, 422, 442, 464, 487, 511, 536, 562, 590, 619, 649, 681, 715, 750, 787, 825, 866, 909, 953 ]
    E96_VALUES = [100, 102, 105, 107, 110, 113, 115, 118, 121, 124, 127, 130, 133, 137, 140, 143, 147, 150, 154, 158, 162, 165, 169, 174, 178, 182, 187,
           191, 196, 200, 205, 210, 215, 221, 226, 232, 237, 243, 249, 255, 261, 267, 274, 280, 287, 294, 301, 309, 316, 324, 332, 340, 348, 357,
           365, 374, 383, 392, 402, 412, 422, 432, 442, 453, 464, 475, 487, 499, 511, 523, 536, 549, 562, 576, 590, 604, 619, 634, 649, 665, 681,
           698, 715, 732, 750, 768, 787, 806, 825, 845, 866, 887, 909, 931, 953, 976]

   
    if series[:3] == 'E96':
        values = E96_VALUES
    elif series[:3] == 'E24':
        values = E24_VALUES
    elif series[:3] == 'E48':
        values = E48_VALUES
    else:
        raise ValueError("Invalid E-series")
   
    if c<vmin:
        standardized_value=vmin
    elif c>vmax:
        standardized_value=vmax
    else:
        i=0
        j=0
        while(c<985):
            c=c*10
            i=i-1
        while(c>976):
            c=c/10
            j=j+1
   
        index = np.abs(np.asarray(values) - c).argmin()
       
        # Calculate the standardized value
        standardized_value = values[index]*(10**(j+i))      
    return standardized_value

def warning(leg):
    c1,c2=st.columns([1,20])
    c1.write(':warning:')
    c2.markdown(f'<p style="color:red">{leg}</p>', unsafe_allow_html=True) 


def draw_sensi(nom,N,D,num,den,fp,variation):
    fig,ax = plt.subplots(figsize=(10,5))
    
    # plt.figure()
    num = np.array(num) 
    den = np.array(den)
    N=np.array(N)
    D=np.array(D)
    dfc=4*m.pi*fp
    wIn = np.linspace(0, dfc, 100)
    wOut, hOut = sc.freqs(num, den, wIn)
    wbase, hbase = sc.freqs(N, D, wIn)
    wIn = np.linspace(0, 2, 100)
    hsensi=[]
    for i in range(len(wIn)):
        h3=((np.abs(hOut[i])-np.abs(hbase[i]))*100)/(variation*np.abs(hbase[i]))
        hsensi.append(h3)
    plt.plot(wIn, hsensi,color=[0.5,0,0.5])
    plt.xlabel('Fréquence normalisée [Hz] (1==fp)')
    plt.ylabel(nom)
    plt.legend(['Courbe de sensibilité'])
    plt.show()
    st.pyplot(fig,ax)