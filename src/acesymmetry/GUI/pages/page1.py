import streamlit as st
import streamlit_ketcher as stk
import pubchempy as pc
import pointgroup as pg
from pathlib import Path
from acesymmetry import Visual_Display as vd, Format_Conversion as conv

st.set_page_config(
    page_title="ACEsymmetry",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.logo(Path(__file__).parent/"assets/epfl-logo.svg", size="large" , link="https://www.epfl.ch/en/", icon_image=None,)
st.title(" Welcome to ACEsymmetry app")
def previous_page():
    if st.button("← Previous"):
        st.session_state.current -= 1
        st.rerun()
def next_page(submitted, condition=True):
    if submitted and condition:
            st.session_state.current += 1 
            st.rerun()

def Molecule_notation_page(): 
    '''Permet de choisir le type d'entrée pour la molecule entre SMILES, IUPAC et Dessin
    le nom de la molecule en SMILES en enregistrer dans st.session_state.molecule_name.'''
    col11, col12 = st.columns([2,3])
    SMILES_or_IUPAC = col11.radio("How would you like to enter your molecule?", ("IUPAC name", "SMILES notation", "Draw the molecule"), index=None)
    molecule_name = None
    IUPAC_molecule_name = None
    submitted = False
    st.set_page_config(initial_sidebar_state="collapsed")
    if SMILES_or_IUPAC == "SMILES notation": 
        with col12:
            with st.form("smiles", enter_to_submit=True):
                molecule_name = st.text_input("Enter the SMILES of your molecule")
                st.session_state.molecule_name = molecule_name
                submitted = st.form_submit_button("Submit")
                next_page(submitted, st.session_state.molecule_name)
    elif SMILES_or_IUPAC == "IUPAC name":
        with col12:
            with st.form("IUPAC", enter_to_submit=True):
                IUPAC_molecule_name = st.text_input("Write the IUPAC name of your molecule.")
                submitted = st.form_submit_button("Submit")
                if submitted : 
                    try:
                        molecule_name = conv.smiles_from_name(IUPAC_molecule_name)
                        if molecule_name is None:
                            st.error("The IUPAC name of your molecule is invalid, try again !", icon = "❌")
                        else : 
                            st.session_state.molecule_name = molecule_name
                            next_page(submitted, st.session_state.molecule_name)  
                    except ImportError : 
                        st.error("Sorry, your molecule is unknown. Please check if your molecule is spelled correctly. ")  
    elif SMILES_or_IUPAC == "Draw the molecule":
        with col12:
            molecule_name = stk.st_ketcher() #SMILES
            if molecule_name:
                try:
                    molecule_info = pc.get_compounds(molecule_name, "smiles")[0]
                    IUPAC_molecule_name = molecule_info.iupac_name
                    molecule_name1 = conv.smiles_from_name(IUPAC_molecule_name)
                    st.session_state.molecule_name = molecule_name1
                    with st.form("Drawing", enter_to_submit=True):
                        st.write("The molecule you drew corresponds to", IUPAC_molecule_name,".")
                        submitted = st.form_submit_button("Next")
                except:
                    st.error("The molecule you draw is not valid ! Sorry", icon= "🚨")
        next_page(submitted, st.session_state.molecule_name)
    previous_page()

def nb_conformer_choice_page():
    submitted = None
    col11, col12 = st.columns([1, 2])
    col21, col22, col23 = st.columns([1, 2,0.5])
    Y_or_N_conformer = col11.radio("Do you want to choose the number of conformers generated in the computations?", ("Yes", "No"), index=None, horizontal=True, help="The default number is 1000 conformers. The more conformers are generetad accurate the result, but the longer the running time of the programm.")
    st.session_state.number_of_conformer = None
    if Y_or_N_conformer == "Yes":
        st.session_state.number_of_conformer = col12.slider("Number of conformer",1,10000)
        submitted = col23.button("Submit")
    elif Y_or_N_conformer == "No":
            st.session_state.number_of_conformer = 1000
            submitted = col22.button("Next →")
    
    previous_page()
    next_page(submitted, st.session_state.number_of_conformer)

def name_files_page():
    col21, col22 = st.columns([5, 5])
    col21.write("Two 3D structure files will be generated and saved on your computer.")
    Y_or_No_name_files = col21.radio("Would you like to rename them or keep the default names ?", ("Rename the files", "Keep the default names"), index=None, help= "The default name of your files are IUPAC.xyz and IUPAC.SDF.")
    st.session_state.name_xyz_files = "default"
    st.session_state.name_SDF_files = "default"
    if Y_or_No_name_files == "Rename the files": 
        col22.write("Special characters and space are not allowed except underscores (_) and hyphens (-).")
        name_xyz_files = col22.text_input("Enter the name of your xyz file.")
        name_SDF_file = col22.text_input("Enter the name of your SDF file.")
        st.session_state.name_xyz_files = name_xyz_files + ".xyz" 
        st.session_state.name_SDF_files = name_SDF_file + ".SDF"
        submitted = st.button("Next →")
    else : 
        submitted = st.button("Next →")
    if st.button("← Previous"):
        st.switch_page("Interface.py")
    next_page(submitted, st.session_state.name_SDF_files)
def point_group_page() : 
    SDF_file_name = None
    xyz_file_name = None
    image = None
    if st.session_state.molecule_name :
        try:
            SDF_file_name, xyz_file_name = conv.overall_conversion_from_smiles(st.session_state.molecule_name, st.session_state.number_of_conformer, st.session_state.name_SDF_files, st.session_state.name_xyz_files)
            Symbols=vd.read_xyz_file(xyz_file_name)[0]
            Positions=vd.read_xyz_file(xyz_file_name)[1]
            point_group=pg.PointGroup(symbols=Symbols, positions=Positions).get_point_group()
            Symmetry_Elements=vd.get_symmetry_set(point_group)
            image = vd.display(xyz_file_name)
            st.image(image)
            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
            with st.container(border=True):
                for label in Symmetry_Elements : 
                    st.write(label)
        except: 
            st.error("Your molecule is invalid or contains metals", icon="🚨")
    previous_page()
pages = [Molecule_notation_page, nb_conformer_choice_page,name_files_page, point_group_page]

if "current" not in st.session_state:
    st.session_state.current = 0

pages[st.session_state.current]()
