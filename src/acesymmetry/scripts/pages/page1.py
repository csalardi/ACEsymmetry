import streamlit as st
import streamlit_ketcher as stk
import pubchempy as pc
import time

from Visual_Display import get_symmetry_set
from Conversion_xyz_From_SMILES import mol_from_SMILES, conformer_selection, overall_conversion

st.set_page_config(
    page_title="Molecular symetry by ACE",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.logo("epfl-logo.svg", size="large" , link="https://www.epfl.ch/en/", icon_image=None,)
st.title(" Molecular symetry app")
st.markdown("## Welcome")

def previous_page():
    if st.button("← Previous", disabled=st.session_state.current == 0):
        st.session_state.current -= 1
        st.rerun()
def next_page(submitted, condition=True):
    if submitted and condition:
            st.session_state.current += 1 
            st.rerun()

def Moleccule_notation(): 
    '''Permet de choisir le type d'entrée pour la molecule entre SMILES, IUPAC et Dessin
    le nom de la molecule en SMILES en enregistrer dans st.session_state.molecule_name.'''
    col11, col12 = st.columns([2,3])
    SMILES_or_IUPAC = col11.radio("How would you like to enter your molecule?", ("IUPAC name", "SMILES notation", "Draw your molecule"), index=None)
    molecule_name = None
    submitted = False
    if SMILES_or_IUPAC == "SMILES notation": 
        with col12:
            with st.form("smiles", enter_to_submit=True):
                molecule_name = st.text_input("Enter the SMILES of your molecule")
                submitted = st.form_submit_button("Submit", icon_position="right")
    elif SMILES_or_IUPAC == "IUPAC name":
        with col12:
            with st.form("IUPAC", enter_to_submit=True):
                molecule_name = st.text_input("Write the IUPAC name of your molecule.")
                submitted = st.form_submit_button("Submit", icon_position="right")
    elif SMILES_or_IUPAC == "Draw your molecule":
        with col12:
            molecule_name = stk.st_ketcher()
            if molecule_name:
                molecule_info = pc.get_compounds(molecule_name, "smiles")[0]
                molecule_name = molecule_info.iupac_name
                with st.form("Drawing", enter_to_submit=True):
                    st.write("The molecule you drew corresponds to", molecule_name,".")
                    submitted = st.form_submit_button("Next",icon_position="right")
    st.session_state.molecule_name = molecule_name
    next_page(submitted, molecule_name)
    previous_page()

def nb_conformer_choice():
    col21, col22 = st.columns([1, 2])
    Y_or_N_conformer = col21.radio("Do you want to choose the number of conformer?", ("Yes", "No"), index=None, help="The default number of conformer is automatically selected.")
    with col21.expander("See explanation"): 
        st.write("The default number of conformer is...")
    if Y_or_N_conformer == "Yes":
            number_of_conformer = None
            number_of_conformer = col22.number_input("Number of conformer",1,10)
            number_of_conformer2 = col22.slider("Number of conformer",1,100)
    previous_page()


pages = [Moleccule_notation, nb_conformer_choice]

if "current" not in st.session_state:
    st.session_state.current = 0

pages[st.session_state.current]()

point_group = None
if point_group: 
    try:
        symmetry_set = get_symmetry_set(point_group)
        st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", symmetry_set,"." )
        with st.container(border=True):
            for axe in symmetry_set : 
                st.write(axe) 
    except:
        st.error("Sorry, your point group is invalid. Try again please.", icon="🚨")    
            

#if SMILES: 
    #try: 
#    treatment_of_SMILES = mol_from_SMILES(SMILES)
#    most_stable_conformer = conformer_selection(treatment_of_SMILES)
 #   fichier_xyz = overall_conversion(most_stable_conformer)
  #  st.write("Your fichier xyz is", fichier_xyz)
    #except: 
   # st.write("Sorry, it seems that your SMILES is incorrect, please make sure to write a valid SMILES !!!")
