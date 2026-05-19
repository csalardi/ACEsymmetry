import streamlit as st
import streamlit_ketcher as stk
import pubchempy as pc
import time
from ace_symmetry import Visual_Display, Conversion_xyz_From_SMILES


st.set_page_config(
    page_title="Molecular symmetry by ACE",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",)
st.logo("epfl-logo.svg", size="large" , link="https://www.epfl.ch/en/", icon_image=None,)
    
st.title(" Molecular symmetry app")
st.subheader("Welcome in our molecular symetry app ")
st.markdown("## Welcome in our molecular symetry app ")
st.write("This app is an interactive application developed at EPFL for the Practical programming in Chemistry. etc. ")
st.text("This app allows users to: - analyse molecular symmetry")
col1, col2, col3 = st.columns([1,5,2])
col3.markdown("-- ACESymetry")
if col3.button("Next →"):
    st.session_state.current = 0
    st.switch_page("pages/page1.py")
