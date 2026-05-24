import streamlit as st
import streamlit_ketcher as stk
import pubchempy as pc
import time
from acesymmetry import Visual_Display, Format_Conversion


st.set_page_config(
    page_title="ACEsymmetry app",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",)
st.logo("assets/epfl-logo.svg", size="large" , link="https://www.epfl.ch/en/", icon_image=None,)
    
st.title("Welcome in our ACEsymmetry app")
st.write("This app is an interactive application developed at EPFL for the Practical programming in Chemistry. etc. ")
st.text("This app allows users to: - analyse molecular symmetry")
col1, col2, col3 = st.columns([1,5,2])
col3.markdown("-- ACESymmetry")
if col3.button("Group Point"):
    st.session_state.current = 0
    st.switch_page("pages/page1.py")
elif col3.button("Learning mode"):
    st.session_state.current = 0
    st.switch_page("pages/learning_mode.py")