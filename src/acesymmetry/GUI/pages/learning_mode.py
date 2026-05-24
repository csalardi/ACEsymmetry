from acesymmetry.Visual_Display import get_symmetry_set
from typing import Union
from acesymmetry import Visual_Display as vd, Format_Conversion as conv
import streamlit as st
import streamlit_ketcher as stk
import pubchempy as pc
import pointgroup as pg

st.set_page_config(
    page_title="ACEsymmetry App",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.logo("assets/epfl-logo.svg", size="large" , link="https://www.epfl.ch/en/", icon_image=None,)
st.title(" ACEsymmetry app")
st.subheader("Learning mode")
if "current" not in st.session_state:
    st.session_state.current = 0
def previous_page():
    if st.button("← Previous"):
        st.session_state.current -= 1
        st.rerun()
def next_page(submitted, condition=True):
    if submitted and condition:
            st.session_state.current += 1 
            st.rerun()
def flowchart_page():
    col11, col12 = st.columns([1,2])
    col21, col22, col23 = st.columns([1,3,0.5])
    with col11: 
        st.write("A molecule point group can be determined by folling this flowchart :")
        st.write("This learning mode follows the steps in the flowchart and checks your answer after each question until you find the correct group point. ")
    col12.image("assets/Flowchart.png")
    if col23.button("Next →"):
        next_page(True, True)
    if col21.button("← Previous"):
        st.switch_page("Interface.py")

def Molecule_notation_page(): 
    '''Permet de choisir le type d'entrée pour la molecule entre SMILES, IUPAC et Dessin
    le nom de la molecule en SMILES en enregistrer dans st.session_state.molecule_name.'''
    col11, col12 = st.columns([2,3])
    SMILES_or_IUPAC = col11.radio("How would you like to enter your molecule?", ("IUPAC name", "SMILES notation", "Draw your molecule"), index=None)
    molecule_name = None
    IUPAC_molecule_name = None
    submitted = False
    st.set_page_config(initial_sidebar_state="collapsed")
    if SMILES_or_IUPAC == "SMILES notation": 
        with col12:
            with st.form("smiles", enter_to_submit=True):
                molecule_name = st.text_input("Enter the SMILES of your molecule")
                submitted = st.form_submit_button("Submit")
    elif SMILES_or_IUPAC == "IUPAC name":
        with col12:
            with st.form("IUPAC", enter_to_submit=True):
                IUPAC_molecule_name = st.text_input("Write the IUPAC name of your molecule.")
                submitted = st.form_submit_button("Submit")
                if submitted : 
                    molecule_name = conv.smiles_from_name(IUPAC_molecule_name)
                    if molecule_name is None:
                        st.error("The IUPAC name of your molecule is invalid, try again !", icon = "❌")
                      
    elif SMILES_or_IUPAC == "Draw your molecule":
        st.set_page_config(initial_sidebar_state="collapsed")
        with col12:
            molecule_name = stk.st_ketcher()
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
    st.session_state.molecule_name = molecule_name
    next_page(submitted, st.session_state.molecule_name)
    previous_page()
def name_files_page():
    col21, col22 = st.columns([5, 5])
    col21.write("Two 3D structure files will be generated and saved on your computer.")
    Y_or_No_name_files = col21.radio("Would you like to rename them or keep the default names ?", ("Rename the files", "Keep the default names"), help= "The default name of your files are IUPAC.xyz and IUPAC.SDF.")
    st.session_state.name_xyz_files = "default"
    st.session_state.name_SDF_files = "default"
    if Y_or_No_name_files == "Rename the files": 
        col22.write("Special characters and space are not allowed except underscores (_) and hyphens (-).")
        st.session_state.name_xyz_files = col22.text_input("Enter the name of your xyz file.")
        st.session_state.name_SDF_files = col22.text_input("Enter the name of your SDF file.")
        submitted = st.button("Next →")
    else : 
        submitted = st.button("Next →")
    previous_page()
    next_page(submitted, st.session_state.name_SDF_files)

def normalize_label(label: str) -> str:
    '''
    Removes the prime symbols from the elements
    param
    :label
    :type str

    return
    :label (str) modified label (symmetry element)
    '''
    label = label.split("(")[0]
    label = label.replace("''", "")
    label = label.replace("'", "")
    return label

def parse_symmetry_element(element: str) -> tuple[int, str]:
    '''
    param
    :element
    :type: str

    return multiplicity, label (tuple of an integer and a string)
    '''

    element = element.strip()
    parts = element.split(maxsplit=1)

    if len(parts) == 1:
        return 1, normalize_label(parts[0])

    try:
        mult = int(parts[0])
        label = normalize_label(parts[1])
        return mult, label
    except ValueError:
        return 1, normalize_label(element)

def check_linearity(point_group:str)->str:
    '''
    Checks the linearity of the molecules (Yes only if it is Cinfv or Dinfh)

    :param point_group: point group of the molecule provided by the appropriate programm
    :type point_group: str

    :return "Yes" (str) if the molecule is linear
    :return "No" (str) if the molecule is not linear
    '''
    if point_group == "Cinfv" or point_group == "Dinfh":
        return "Yes"
    else:
        return "No"

def check_inversion_centre(symmetry_set: set[str])->str:
    '''
    Checks the presence of an inversion center

    :param symmetry_set
    :type set of strings

    :return "Yes" if the molecule has a pointgroup
    :return "No" if the molecule has not that symmetry element
    '''
    if "i" in symmetry_set:
        return "Yes"
    else:
        return "No"
    

def check_main_axis_multiplicity(point_group:str)->str:
    '''
    Checks the presence of multiple main axes whose order is greater than 2
    (Yes only for Ih, I, Oh, O, Td, T)

    :param pointgroup: point group of the molecule provided by the appropriate program
    :type str

    
    :return "Yes" (str) if the molecule has multiple main axes whose order is greater than 2
    :return "No" (str) if not
    '''
    if point_group in {"Ih", "I", "Oh", "O", "Td", "T"}:
        return "Yes"
    else:
        return "No"

def check_rotation_axis(symmetry_set:set[str]) -> str:
    '''
    Checks the presence of rotation axis in the molecule

    :param symmetry_list
    :type list of strings

    :return "Yes" (str) if the molecule has rotation axis
    :return "No" (str) if not
    '''
    n_max = 0

    for element in symmetry_set:
        _, label = parse_symmetry_element(element)

        if label.startswith("C"):
            try:
                n = int(label[1:])
                if n > n_max:
                    n_max = n
            except ValueError:
                pass

    if n_max > 0:
        return "Yes"
    else:
        return "No"
    
def check_horizontal_plane(symmetry_set:set[str])->str:
    '''
    Checks the presence of horizontal planes
    :param symmetry_set
    :type set of strings

    :return "Yes" (str) if the molecule has horizontal planes
    :return "No" (str) if not
    '''
    if "Sigma_h"in symmetry_set:
        return "Yes"
    else:
        return "No"
    
def check_vertical_plane(symmetry_set:set[str])->str:
    '''
    Checks the presence of vertical planes
    :param symmetry_set
    :type set of strings

    :return "Yes" (str) if the molecule has vertical planes
    :return "No" (str) if not
    '''
    if "Sigma_v"in symmetry_set:
        return "Yes"
    else:
        return "No"
    
def check_dihedral_plane(symmetry_set:set[str])->str:
    '''
    Checks the presence of dihedral planes
    :param symmetry_set
    :type set of strings

    :return "Yes" (str) if the molecule has dihedral planes
    :return "No" (str) if not
    '''
    if "Sigma_d"in symmetry_set:
        return "Yes"
    else:
        return "No"

def check_improper_rotation_axis(group_point)->str:
    '''
    Checks the presence of improper rotation axes with order 2n_ref for molecules with Cn axis

    :return "Yes" (str) if the molecule has improper rotation axes with order 2n_ref
    :return "No" (str) if not
    '''
    if group_point.startswith("S"):
        return "Yes"
    else: 
        return "No"

def check_icosahedral_symmetry(point_group:str)->str:
    '''
    Checks wether the molecule is icosahedral
    :param point_group
    :type str

    :return "Yes" (str) if the molecule is Ih
    :return "No" (str) if not
    '''
    if point_group == "Ih":
        return "Yes"
    else:
        return "No"
def check_C2_multiplicity(point_group) -> str:
    '''
    Checks the presence of n C2 axes 
    :return: "Yes" if condition is satisfied, "no" otherwise
    '''
    if point_group.startswith("D"):
        if point_group.endswith("h"):
            return "Yes"
        elif point_group.endswith("d"):
            return "Yes"
        else:
            return "No"
    else: 
        return "No"

    
def check_vertical_plane_multiplicity(point_group)->str:
    '''
    Checks the  presence of n vertical planes for molecules with Cn axis
    :param point_group


    :return "Yes" (str) if the molecule has n vertical planes
    :return "No" (str) if not
    '''
    if point_group.startswith("D"):
        if point_group.endswith("d"):
            return "Yes"
        else : 
            return "No"
    elif point_group.startswith("C"):
        if point_group.endswith("v"):
            return "Yes"
        else: 
            return "No"
    else: 
        "No"

def Questions_page() : 
    c = "Correct !"
    i = "Incorrect !"
    xyz_file_name = None
    response = None
    if st.session_state.molecule_name :
        try:
            st.session_state.number_of_conformer = 1000
            xyz_file_name = conv.overall_conversion_from_smiles(st.session_state.molecule_name, st.session_state.number_of_conformer, st.session_state.name_SDF_files, st.session_state.name_xyz_files)[1]
            Symbols=vd.read_xyz_file(xyz_file_name)[0]
            Positions=vd.read_xyz_file(xyz_file_name)[1]
            point_group=pg.PointGroup(symbols=Symbols, positions=Positions).get_point_group()
            Symmetry_Elements=vd.get_symmetry_set(point_group)
            image = vd.display(xyz_file_name)
            st.image(image)
            response = st.radio("Is your molecule linear ?", ("Yes", "No"), index=None, horizontal= True)
            if response: 
                if response == check_linearity(point_group):
                    st.write(c)
                else : 
                    st.write(i)
                if check_linearity(point_group) == "Yes" : 
                    response = st.radio("Does your molecule have an inversion centre ?", ("Yes", "No"), index=None, horizontal= True)
                    if response : 
                        if response == check_inversion_centre(Symmetry_Elements):
                            st.write(c)
                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                        else: 
                            st.write(i)
                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                elif check_linearity(point_group) == "No": 
                    response = st.radio("Does your molecule have two or more n-fold proper rotation axis with n > 2 ? (Cn, n > 2)", ("Yes", "No"), index=None, horizontal=True)
                    if response : 
                        if response == check_main_axis_multiplicity(point_group):
                            st.write(c)
                        else :
                            st.write(i)
                        if check_main_axis_multiplicity(point_group) == "Yes": 
                            response = st.radio("Does your molecule have an inversion centre ?", ("Yes", "No"), index=None, horizontal=True)
                            if response : 
                                if response == check_inversion_centre(Symmetry_Elements):
                                    st.write(c)   
                                else : 
                                    st.write(i) 
                                if check_inversion_centre(Symmetry_Elements) == "No":
                                    st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                elif check_inversion_centre(Symmetry_Elements) == "Yes":
                                    response = st.radio("Does your molecule have a 5-fold proper rotation axis, (C5) ?", ("Yes", "No"), index=None, horizontal=True)
                                    if  response : 
                                        if response == check_icosahedral_symmetry(point_group) :
                                            st.write(i)
                                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                        else : 
                                            st.write(i) 
                                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                        if check_main_axis_multiplicity(point_group) == "No": 
                            response = st.radio("Does your molecule have an n-fold rotation axis, (Cn) ?", ("Yes", "No"), index=None, horizontal=True)
                            if response : 
                                if response == check_rotation_axis(Symmetry_Elements): 
                                    st.write(c)
                                else : 
                                    st.write(i)
                                if check_rotation_axis(Symmetry_Elements) == "No": 
                                    response = st.radio("Does your molecule have a horizontal plane (sigma_h) ?", ("Yes", "No"), index=None, horizontal=True)
                                    if response: 
                                        if response == check_horizontal_plane(Symmetry_Elements):
                                            st.write(c)
                                        else:
                                            st.write(i)
                                        if check_horizontal_plane(Symmetry_Elements) == "Yes":
                                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                        elif check_horizontal_plane(Symmetry_Elements) == "No":
                                            response = st.radio("Does your molecule have an inversion centre ?", ("Yes", "No"), index=None, horizontal=True)
                                            if response : 
                                                if response == check_inversion_centre(Symmetry_Elements):
                                                    st.write(c)
                                                    st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                                else : 
                                                    st.write(i)
                                                    st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                elif check_rotation_axis(Symmetry_Elements) == "Yes":
                                    response = st.radio("Does the Cn axis of your molecule have n perpendicular C2 axis ?",("Yes", "No"), index=None, horizontal=True)
                                    if response : 
                                        if response == check_C2_multiplicity(point_group): 
                                            st.write(c)
                                        else: 
                                            st.write(i)
                                        if check_C2_multiplicity(point_group) == "Yes":
                                            response = st.radio("Does your molecule have a horizontal plane (sigma_h) ?",("Yes", "No"), index=None, horizontal=True)
                                            if response : 
                                                if response == check_horizontal_plane(Symmetry_Elements) : 
                                                    st.write(c)
                                                else : 
                                                    st.write(i)
                                                if check_horizontal_plane(Symmetry_Elements) == "Yes":
                                                   st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                                if check_horizontal_plane(Symmetry_Elements) == "No" :
                                                    response = st.radio("Does your molecule have a principal n-fold rotation axis (Cn) with n vertical mirror planes (n sigma_v) ?",("Yes", "No"), index=None, horizontal=True)
                                                    if response : 
                                                        if response == check_vertical_plane_multiplicity(point_group) : 
                                                            st.write(c)
                                                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                                        else : 
                                                            st.write(i)
                                                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                        elif check_C2_multiplicity(point_group) == "No":
                                            response = st.radio("Does your molecule have a horizontal plane (sigma_h) ?",("Yes", "No"), index=None, horizontal=True)
                                            if response : 
                                                if response == check_horizontal_plane(Symmetry_Elements) : 
                                                    st.write(c)
                                                else : 
                                                    st.write(i)
                                                if check_horizontal_plane(Symmetry_Elements) == "Yes":
                                                    st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                                elif check_horizontal_plane(Symmetry_Elements) == "No":
                                                    response = st.radio("Does your molecule have a principal n-fold rotation axis (Cn) with n vertical mirror planes (n sigma_v) ?",("Yes", "No"), index=None, horizontal=True)
                                                    if response : 
                                                        if response == check_vertical_plane_multiplicity(point_group) : 
                                                            st.write(c)
                                                        else : 
                                                            st.write(i)
                                                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                                        if check_vertical_plane_multiplicity(point_group) == "Yes": 
                                                            st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                                        elif check_vertical_plane_multiplicity(point_group) == "No":
                                                            response = st.radio("Does your molecule contain a improper axe of symmetry S_2n ?",("Yes", "No"), index=None, horizontal=True)
                                                            if response: 
                                                                if response == check_improper_rotation_axis(point_group): 
                                                                    st.write(c)
                                                                    st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )
                                                                else : 
                                                                    st.write(i)
                                                                    st.write("The point group of your molecule is", point_group,"and the corresponding symmetry set is :", Symmetry_Elements,"." )                                    
        except: 
            st.error("Your molecule is invalid or contains metals", icon="🚨")
    previous_page()       

pages = [flowchart_page, Molecule_notation_page, name_files_page, Questions_page]

if "current" not in st.session_state:
    st.session_state.current = 0

pages[st.session_state.current]()