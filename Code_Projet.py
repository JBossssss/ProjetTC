# -*- coding: utf-8 -*-
from Utils_Projet import *
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams
import scipy.signal as sc
import math as m

'''
Visualisation d'une PWM avec les conditions de la Q1 et comparaison avec la sinusoïde d'entrée
'''

t=np.arange(0,50,0.01)
fct= np.sin(0.2*m.pi*t) > 1.2*sc.sawtooth(2*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(0.2*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM','Sinusoïde en entrée'])
plt.show()

#%%

'''
Analyse de l'influence de la fréquence du signal triangulaire
'''

'Basse fréquence'
fct= np.sin(0.2*m.pi*t) > 1.2*sc.sawtooth(0.2*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(0.2*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM basse fréquence','Sinusoïde en entrée'])
plt.show()

'Haute fréquence'
fct= np.sin(0.2*m.pi*t) > 1.2*sc.sawtooth(3*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(0.2*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM haute fréquence','Sinusoïde en entrée'])
plt.show()

#%%

'''
Analyse de l'influence de l'amplitude du signal triangulaire
'''

'Basse amplitude'
fct= np.sin(0.2*m.pi*t) > 0.2*sc.sawtooth(2*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(0.2*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM basse amplitude','Sinusoïde en entrée'])
plt.show()

'Haute amplitude'
fct= np.sin(0.2*m.pi*t) > 10*sc.sawtooth(2*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(0.2*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM haute amplitude','Sinusoïde en entrée'])
plt.show()

#%%

'''
Visualisation d'une PWM avec les conditions de la Q4 et comparaison avec la sinusoïde d'entrée
'''

t=np.arange(0,5*1e-3,1e-6)
fct= np.sin(2000*m.pi*t) > sc.sawtooth(40000*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(2000*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM','Sinusoïde en entrée'])
plt.show()

#%%

'''
Analyse de l'influence de la fréquence d'échantillonnage
'''

'Fe/2'
t=np.arange(0,5*1e-3,2e-6)
fct= np.sin(2000*m.pi*t) > sc.sawtooth(40000*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(2000*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM avec Fe/2','Sinusoïde en entrée'])
plt.show()

'Fe/3'
t=np.arange(0,5*1e-3,3e-6)
fct= np.sin(2000*m.pi*t) > sc.sawtooth(40000*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(2000*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM avec Fe/3','Sinusoïde en entrée'])
plt.show()

'Fe/10'
t=np.arange(0,5*1e-3,1e-5)
fct= np.sin(2000*m.pi*t) > sc.sawtooth(40000*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(2000*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM avec Fe/10','Sinusoïde en entrée'])
plt.show()

'Fe limite = 2 * F tri = 40 kHz'
t=np.arange(0,5*1e-3,1/40000)
fct= np.sin(2000*m.pi*t) > sc.sawtooth(40000*m.pi*t,width=0.5)
plt.plot(t,fct)
plt.plot(t,0.5+np.sin(2000*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM avec Fe limite','Sinusoïde en entrée'])
plt.show()

#%%

'''
Visualisation du signal amplifié avec comparaison à la sinusoïde d'entrée
'''
t=np.arange(0,5*1e-3,1e-6)
fct= np.sin(2000*m.pi*t) > sc.sawtooth(40000*m.pi*t,width=0.5)
plt.plot(t,100*fct)
plt.plot(t,0.5+np.sin(2000*m.pi*t)/2)
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude [V]')
plt.legend(['PWM','Sinusoïde en entrée'])
plt.show()

#%%

'''
Analyse de la transformée de fourier du signal amplifié
'''

'Transformée complète'
w,h=sc.freqz(fct,1,2048,fs=1e6)
hdb=20*np.log10(abs(h))
plt.plot(w,hdb,'purple')
plt.xlabel('Fréquence [Hz]')
plt.ylabel('Amplitude [dB]')
plt.legend(['Transformée de Fourier de la PWM amplifiée'])
plt.show()

'Zoom sur les basses fréquences'
plt.plot(w,hdb,'purple')
plt.xlabel('Fréquence [Hz]')
plt.ylabel('Amplitude [dB]')
plt.legend(['Transformée zoomée sur les basses fréquences'])
plt.xlim(0,40000)
plt.show()

'Zoom sur la fréquence du sinus (1000 Hz)'
plt.plot(w,hdb,'purple')
plt.xlabel('Fréquence [Hz]')
plt.ylabel('Amplitude [dB]')
plt.legend(['Transformée zoomée sur la fréquence du sinus'])
plt.xlim(0,2000)
plt.show()

'Zoom sur les harmoniques (Autour de 20 kHz)'
plt.plot(w,hdb,'purple')
plt.xlabel('Fréquence [Hz]')
plt.ylabel('Amplitude [dB]')
plt.legend(['Transformée zoomée sur la fréquence des harmoniques'])
plt.xlim(15000,25000)
plt.show()

#%%

'''
Normalisation + visualisation des pôles et zéros + réponse en fréquence de chaque type de filtre
'''

'Butterford'

[n,wn]=sc.buttord(1, 19/16, 1, 40, analog=True,fs=None)
[N,D]=sc.butter(n,wn,analog=True)
M=D.shape
print('===========================')
print('Degré du filtre Butterford')
print('===========================')
print(M[0]-1)
zplane('Pôles et zéros Butterford',N,D,r=2.5)                  #'Visualisation pôles et zéros'      
draw_repfreq('Butterford',N, D,-0.2, 0.2)                      #'Réponse en fréquence'
draw_filtre('Butterford',N, D,-0.2, 0.1, 1, 19/16, 1, 40)      #'Réponse en fréquence + limites du filtre'

'Chebychev I'

[n1,wn1]=sc.cheb1ord(1, 19/16, 1, 40, analog=True,fs=None)
[N1,D1]=sc.cheby1(n1,1,wn1,analog=True);
M1=D1.shape
print('===========================')
print('Degré du filtre Chebychev I')
print('===========================')
print(M1[0]-1)
zplane('Pôles et zéros Chebychev I',N1,D1,r=2.5)                #'Visualisation pôles et zéros'
draw_repfreq('Chebychev I',N1, D1,-1, 1)                        #'Réponse en fréquence'
draw_filtre('Chebychev I',N1, D1,-0.2, 0.1, 1, 19/16, 1, 40)    #'Réponse en fréquence + limites du filtre'

'Cauer'

[n2,wn2]=sc.ellipord(1, 19/16, 1, 40, analog=True,fs=None)
[N2,D2]=sc.ellip(n2,1,40,wn2,analog=True)
M2=D2.shape
print('===========================')
print('Degré du filtre Cauer')
print('===========================')
print(M2[0]-1)
zplane('Pôles et zéros Cauer',N2,D2,r=2.5)                #'Visualisation pôles et zéros'
draw_repfreq('Cauer',N2, D2,-2, 2)                        #'Réponse en fréquence'
draw_filtre('Cauer',N2, D2,-0.2, 0.1, 1, 19/16, 1, 40)    #'Réponse en fréquence + limites du filtre'

'Cauer après modification de A start = 1.6'

[n2,wn2]=sc.ellipord(1, 19/16, 1.6, 40, analog=True,fs=None)
[N2,D2]=sc.ellip(n2,1.6,40,wn2,analog=True)
M2=D2.shape
print('===========================')
print('Degré du filtre Cauer avec Astart=1.6')
print('===========================')
print(M2[0]-1)
zplane('Pôles et zéros Cauer sélectionné',N2,D2,r=2.5)                  #'Visualisation pôles et zéros'
draw_repfreq('Cauer sélectionné',N2, D2,-2, 2)                          #'Réponse en fréquence'
draw_filtre('Cauer sélectionné',N2, D2,-0.2, 0.1, 1, 19/16, 1.6, 40)    #'Réponse en fréquence + limites du filtre'

#%%


'''
Séparation de H(p) en H1(p), H2(p) et H3(p)
'''

'Composition des numérateurs et dénominateurs de H1, H2 et H3'
[z,p,k]=sc.ellipap(5,1.6,40)

'Numérateurs'
Z2=np.poly([z[0],z[2]])
Z3=np.poly([z[1],z[3]])
# print('Z2,Z3',Z2,Z3)


'Dénominateurs'
P1=[1,-p[0]]
P2=np.poly([p[1],p[3]])
P3=np.poly([p[2],p[4]])
# print('P1,P2,P3',P1,P2,P3)

''' 
On doit lier les plus proches, donc Z2 avec P3 + répartition du gain

Nous allons répartir le gain afin d'avoir un gain en continu unitaire (O dB) dans chaque fonction de transfert

H1 = K1 * (1/P1)     H2 = K2 * (Z2/P2)     H3 = K3 * (Z3/P3)

H3: meilleur facteur de qualité
'''

K1=P1[1]
K2=P2[2]/Z2[2]
K3=P3[2]/Z3[2]

print('===========================')
print('Gain de H1(p)')
print('===========================')
print(K1)
print('===========================')
print('Gain de H2(p)')
print('===========================')
print(K2)
print('===========================')
print('Gain de H3(p)')
print('===========================')
print(K3)

K=K1*K2*K3
print('===========================')
print('Gain de H(p)=H1(p)*H2(p)*H3(p)')
print('===========================')
print(K)

'Tracé de H1, H2 et H3'
draw_repfreq('H1(p)',[K1], P1, -2, 2)
draw_repfreq('H2(p)',K2*Z2, P2, -2, 2)
draw_repfreq('H3(p)',K3*Z3, P3, -2, 2)

"ADDITION DES 3"
wIn = np.logspace(-2, 2, 10000000)

wOut, hOut1 = sc.freqs(K3*Z3, P3, wIn)
wOut, hOut2 = sc.freqs(K2*Z2, P2, wIn)
wOut, hOut3 = sc.freqs([K1], P1, wIn)

hOut=hOut1*hOut2*hOut3

#%%

'Tracé de H(p)=H1(p)*H2(p)*H3(p)'
plt.semilogx(wOut, 20*np.log10(np.abs(hOut)))
plt.xlabel('Fréquence Normalisée [Hz]')
plt.ylabel('Amplitude [dB]')
plt.legend(['H(p)'])
plt.show()

"Calcul des éléments de la cellule du premier degrés : H1(p)=K/(1+Tp)"

T=-1/p[0]
K=-p[0]

"Dénormalisation :"
T=T/16000

print('===========================')
print('Gain de H1(p) dénormalisée')
print('===========================')
print(K)
NUM=[1]
DEN=[T,1]

draw_repfreq('H1(p) dénormalisée',NUM, DEN, 0, 5)

#%%

'''
Visualisation des fonctions de transfert dénormalisées
'''

"Conception du filtre non normalisé"

[n2,wn2]=sc.ellipord(16000, 19000, 1.6, 40, analog=True,fs=None)
[N2,D2]=sc.ellip(n2,1.6,40,wn2,analog=True)

zeros=compute_roots(N2)
poles=compute_roots(D2)



n1=[zeros[2],zeros[3]]
p3=[poles[0],poles[1]]
n2=[zeros[0],zeros[1]]
p2=[poles[2],poles[3]]


Z2=np.poly(n1)
Z3=np.poly(n2)

P1=[1,-poles[4]]
P2=np.poly(p2)
P3=np.poly(p3)

K1=P1[1]
K2=P2[2]/Z2[2]
K3=P3[2]/Z3[2]


'''
On doit lier les plus proches, donc Z2 avec P3 + répartir le gain

H3: meilleur facteur de qualité
'''
'Tracé de H1, H2 et H3'

draw_repfreq('H1(p)',[K1], P1,  0, 5)
draw_repfreq('H2(p)',K2*Z2, P2, 0, 5)
draw_repfreq('H3(p)',K3*Z3, P3, 0, 5)

"ADDITION DES 3"
wIn = np.logspace(4, 4.6, 10000000)

wOut, hOut1 = sc.freqs(K3*Z3, P3, wIn)
wOut, hOut2 = sc.freqs(K2*Z2, P2, wIn)
wOut, hOut3 = sc.freqs([K1], P1, wIn)

hOut=hOut1*hOut2*hOut3
   
plt.semilogx(wOut, 20*np.log10(np.abs(hOut)))
plt.xlabel('Fréquence [Hz]')
plt.ylabel('Amplitude [Db]')
plt.title('H(p) dénormalisée')
plt.show()

draw_filtre('H(p) dénormalisée',N2, D2, 4, 4.6, 16000, 19000, 1.6, 40)

