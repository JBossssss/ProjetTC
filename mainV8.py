"""
Created on Tue Apr 18 14:03:01 2023
@author: Loren
"""
from CodeV8 import *
from ProjUtilsV8 import *
import streamlit as st

st.set_page_config(page_title='Filtres RCAO',layout="wide",page_icon='📈',initial_sidebar_state="collapsed")

st.title("Synthèse de filtres RCAO")

test=True
data=[]

side=st.sidebar

# tabs = st.tabs(['filtre 1','filtre 2','filtre 3','filtre 4','filtre 5'])
# for i in range(len(tabs)-1):
#     with tabs[i+1]:
#        st.caption("Veuillez d'abord créer le filtre précédant avant de créer celui-ci")
cont1=side.container()
cont2=side.container()
p=1
# while(test==True):

    # test=False
        # with tabs[p-1]:  
sel,image,name,dat,plot=filter(p)
if (sauvegarder(p)):
    test=True
    with cont1:
        save_side(sel,image,name, dat, p)
    tb=[sel,image,name, dat, p,plot]
    data.append(tb)
    p=p+1
with cont2:
    if p!=1:
        download_pdf(data)

