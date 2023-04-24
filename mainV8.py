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

test=True
data=[]

side=st.sidebar
tabs = st.tabs(['filtre 1','filtre 2','filtre 3','filtre 4','filtre 5'])
cont1=side.container()
cont2=side.container()
p=1           
while(test==True):

    test=False
    st.write(p,len(tabs))
    with tabs[p-1]:
        sel,image,name,dat=filter(p)
        if (sauvegarder(p)):
            test=True
            with cont1:
                save_side(sel,image,name, dat, p)
            tb=[sel,image,name, dat, p]
            data.append(tb)                  
    p=p+1
    # Filtre='Filtre '
    # Filtre+=str(p)
    # st.session_state["tabs"].append(Filtre)
with cont2:
    download_pdf(data)

# if "tabs" not in st.session_state:
#     st.session_state["tabs"] = ["Filter Data", "Raw Data", "📈 Chart"]
    # if "tabs" not in st.session_state:
    #     st.session_state["tabs"] = ['Filtre 1']
    # tabs = st.tabs(st.session_state["tabs"])
    
    
# tabs = st.tabs(st.session_state["tabs"])

# new_tab = st.text_input("Tab label", "New Tab")
# if st.button("Add tab"):
#     st.session_state["tabs"].append(new_tab)
#     st.experimental_rerun()      
