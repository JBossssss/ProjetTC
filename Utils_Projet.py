import numpy as np 
import matplotlib.pyplot as plt
import scipy.signal as sc
from  matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams
    

def draw_repfreq(leg,num, den, w_min, w_max):

    '''
    Dessine la réponse en fréquence du filtre en fonction des polynômes de H(p) = Num(p)/Den(p) entre
    les valeurs 10^w_min et 10^w_max. Ainsi, si w_min = 0 et w_max = 1, la courbe de Bode sera dressée
    entre 10^0 et 10^1 en échelle logarithmique

    Example : H(p) = (p+1)/(p+2) 
    inputs : num=[1,1], den=[1,2] (<= facteurs multiplicatifs du polynôme), w_min = 0, w_max = 1
    outputs : None
    '''

    plt.figure()
    num = np.array(num) 
    den = np.array(den)

    wIn = np.logspace(w_min, w_max, 10000000)
    wOut, hOut = sc.freqs(num, den, wIn)
    
    plt.semilogx(wOut, 20*np.log10(np.abs(hOut)))
    plt.xlabel('Fréquence Normalisée [Hz]')
    plt.ylabel('Amplitude [dB]')
    plt.legend([leg])
    plt.show()
def draw_filtre(leg,num, den, w_min, w_max, w1,w2,A1,A2):

     
     'Cette partie nous sert à tracer les limites du filtre voulu'
     plt.figure()
     num = np.array(num) 
     den = np.array(den)
     t=np.arange(0,10000,0.01)
     Astartx=[10**(w_min),w1]
     Astarty=[-A1,-A1]
     Astopx=[w2,10**(w_max)]
     Astopy=[-A2,-A2]
     fstartx=[w1,w1]
     fstarty=[-A1,-A2]
     fstopx=[w2,w2]
     fstopy=[-A1,-A2]
     
     'Cette partie vient de drawrepfreq'

     wIn = np.logspace(w_min, w_max, 10000000)
     wOut, hOut = sc.freqs(num, den, wIn)
     
     plt.semilogx(wOut, 20*np.log10(np.abs(hOut)))
     plt.plot(Astartx,Astarty,'red')
     plt.plot(Astopx,Astopy,'red')
     plt.plot(fstartx,fstarty,'red')
     plt.plot(fstopx,fstopy,'red')
     # plt.plot(w2,t)
     # plt.plot(t,A1)
     # plt.plot(t,A2)
     plt.xlabel('Fréquence Normalisée [Hz]')
     plt.ylabel('Amplitude [dB]')
     plt.legend([leg,'limites du filtre'])
     plt.show()   

def compute_roots(poly):

    '''
    Calcule la racine d'un polynôme 

    Example : F(p) = (p+1) 
    inputs : num=[1,1]
    outputs : racine du polynôme
    '''
    return np.roots(np.array(poly))

# Copyright (c) 2011 Christopher Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# The following is derived from the slides presented by
# Alexander Kain for CS506/606 "Special Topics: Speech Signal Processing"
# CSLU / OHSU, Spring Term 2011.

def zplane(leg,num,den,r=2.5,filename=None):

    """Plot the complex z-plane given a transfer function.
    inputs :
    - num, den (<= facteurs multiplicatifs du polynôme)
    - r (<= échelle de la figure)
    - filename (<= nom de la figure à sauvegarder. Si =None, l'affiche et ne la sauvegarde pas)
    outputs : zéros, pôles, k (facteur multiplicatif)

    """

    b = np.array(num)
    a = np.array(den)
    # get a figure/plot
    ax = plt.subplot(111)

    # create the unit circle
    uc = patches.Circle((0,0), radius=1, fill=False,
                        color='black', ls='dashed')
    ax.add_patch(uc)

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

    # set the ticks
    plt.axis('scaled'); plt.axis([-r, r, -r, r])
    ticks = [-2,-1.5,-1,-0.5,0.5,1,1.5]; plt.xticks(ticks); plt.yticks(ticks)

    if filename is None:
        plt.title(leg)
        plt.show()
    else:
        plt.savefig(filename)
    

    return z, p, k




