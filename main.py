# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 14:03:01 2023

@author: Loren
"""
from CodeV8 import *
from ProjUtilsV8 import *
import streamlit as st


st.set_page_config(page_title='Filtre RCAO',layout="wide",page_icon='📈',initial_sidebar_state="expanded")   

st.title("Synthèse de filtres RCAO")

p=1
test=True
data=[]

tabs = st.tabs(['filtre 1','filtre 2','filtre 3','filtre 4','filtre 5','filtre 6','filtre 7','filtre 8','filtre 9','filtre 10'])
side=st.sidebar
cont1=side.container()
cont2=side.container()
 
while(test):
    
    with tabs[p-1]:
        test=False
        sel,image,name,dat=filter(p)
        
        if (sauvegarder(p)):
            test=True
            with cont1:
                save_side(sel,image,name, dat, p)
            tb=[sel,image,name, dat, p]
            data.append(tb)
            p=p+1
            with cont2:
                download_pdf(data)


     
    
