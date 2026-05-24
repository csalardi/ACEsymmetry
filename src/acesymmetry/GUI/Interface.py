import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="ACEsymmetry app",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",)
st.logo(Path(__file__).parent/"assets/epfl-logo.svg", size="large" , link="https://www.epfl.ch/en/", icon_image=None,)
    
st.title("Welcome to our ACEsymmetry app !")
st.write("This app is an interactive application developed at EPFL for the Practical programming in Chemistry Course. ")
st.write("This app allows the user to: ")
st.write("- find the point group of a molecule and the corresponding symmetry elements via the Point Group option.")
st.write("- to practice finding the group point of a molecule by following a flowchart via the Learning mode option.")
st.write("This app does not work with molecule containing metals !!!")
col1, col2, col3 = st.columns([1,5,2])
col3.markdown("-- The ACESymmetry Team")
if col3.button("Point Group"):
    st.session_state.current = 0
    st.switch_page("pages/Point_Group.py")
elif col3.button("Learning Mode"):
    st.session_state.current = 0
    st.switch_page("pages/Learning_Mode.py")