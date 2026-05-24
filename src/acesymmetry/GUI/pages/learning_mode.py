from acesymmetry import Symmetry_Elements_Dico
from acesymmetry.Visual_Display import get_symmetry_set
from typing import Union

#symmetry_set:set[str]=get_symmetry_set(point_group)
#symmetry_list:list[str]=list(symmetry_set)

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
    Checks the linearity of the molecules (true only if it is Cinfv or Dinfh)

    :param point_group: point group of the molecule provided by the appropriate programm
    :type point_group: str

    :return "yes" (str) if the molecule is linear
    :return "no" (str) if the molecule is not linear
    '''
    if point_group == "Cinfv" or point_group == "Dinfh":
        return "yes"
    else:
        return "no"

def check_inversion_centre(symmetry_set: set[str])->str:
    '''
    Checks the presence of an inversion center

    :param symmetry_set
    :type set of strings

    :return "yes" if the molecule has a pointgroup
    :return "no" if the molecule has not that symmetry element
    '''
    if "i" in symmetry_set:
        return "yes"
    else:
        return "no"
    

def check_main_axis_multiplicity(point_group:str)->str:
    '''
    Checks the presence of multiple main axes whose order is greater than 2
    (true only for Ih, I, Oh, O, Td, T)

    :param pointgroup: point group of the molecule provided by the appropriate program
    :type str

    
    :return "yes" (str) if the molecule has multiple main axes whose order is greater than 2
    :return "no" (str) if not
    '''
    if point_group in {"Ih", "I", "Oh", "O", "Td", "T"}:
        return "yes"
    else:
        return "no"

def check_rotation_axis(symmetry_list:list[str])->tuple[str, int]:
    '''
    Checks the presence of rotation axis in the molecule

    :param symmetry_list
    :type list of strings

    :return "yes" (str) if the molecule has rotation axis
    :return n_max (int) which is the order of the axis
    :return ("no" (str) if the molecule has no rotation axis
    :return 0 if the molecule has no rotation axis (associated with the "no")
    '''
    n_max = 0

    for element in symmetry_list:
        _, label = parse_symmetry_element(element)

        if label.startswith("C"):
            try:
                n = int(label[1:])
                if n > n_max:
                    n_max = n
            except ValueError:
                pass

    if n_max > 0:
        return ("yes", n_max)
    else:
        return ("no", 0)
    
def check_horizontal_plane(symmetry_set:set[str])->str:
    '''
    Checks the presence of horizontal planes
    :param symmetry_set
    :type set of strings

    :return "yes" (str) if the molecule has horizontal planes
    :return "no" (str) if not
    '''
    for element in symmetry_set:
        _, label = parse_symmetry_element(element)
        if label == "Sigma_h":
            return "yes"
    return "no"
    
def check_vertical_plane(symmetry_set:set[str])->str:
    '''
    Checks the presence of vertical planes
    :param symmetry_set
    :type set of strings

    :return "yes" (str) if the molecule has vertical planes
    :return "no" (str) if not
    '''
    for element in symmetry_set:
        _, label = parse_symmetry_element(element)
        if label == "Sigma_v":
            return "yes"
    return "no"
    
def check_dihedral_plane(symmetry_set:set[str])->str:
    '''
    Checks the presence of dihedral planes
    :param symmetry_set
    :type set of strings

    :return "yes" (str) if the molecule has dihedral planes
    :return "no" (str) if not
    '''
    for element in symmetry_set:
        _, label = parse_symmetry_element(element)
        if label == "Sigma_d":
            return "yes"
    return "no"

def check_improper_rotation_axis(symmetry_list:list[str], n:int)->str:
    '''
    Checks the presence of improper rotation axes with order 2n_ref for molecules with Cn axis
    :param symmetry_set
    :type set of strings
    :param n 
    :type int

    :return "yes" (str) if the molecule has improper rotation axes with order 2n 
    :return "no" (str) if not
    '''
    for element in symmetry_list:
        _, label = parse_symmetry_element(element)

        if label.startswith("S") == True:
            try:
                if int(label[1:]) == 2 * n:
                    return "yes"
            except ValueError:
                pass

    return "no"

def check_icosahedral_symmetry(point_group:str)->str:
    '''
    Checks wether the molecule is icosahedral
    :param point_group
    :type str

    :return "yes" (str) if the molecule is Ih
    :return "no" (str) if not
    '''
    if point_group == "Ih":
        return "yes"
    else:
        return "no"

def check_C2_multiplicity(point_group:str) -> str:
    '''
    Checks the presence of n C2 axes for molecules with Cn axes. It corresponds to Dn, Dnh and Dnd.
    Therefore, this function is equivalent to verify is the pointgroup of the 
    studied molecule belongs to one of the three mentioned pointgoups

    :param pointgroup
    :type str

    :return "yes" (str) if the molecule is Dn, Dnhn Dnd
    :return "no" (str) if not
    '''
    if point_group.startswith("D") == True:
        return "yes"
    else
        return "no"

def check_dihedral_plane_multiplicity(symmetry_list:list[str], n:int)->str:
    '''
    Checks the  presence of n dihedral planes for molecules with Cn axis
    :param point_group
    :type str
    :param n
    :type int

    :return "yes" (str) if the molecule has n dihedral planes 
    :return "no" (str) if not
    '''
    counter = 0

    for element in symmetry_list:
        mult, label = parse_symmetry_element(element)

        if label == "Sigma_d":
            counter += mult

    if counter == n:
        return "yes"
    return "no"

def check_vertical_plane_multiplicity(symmetry_list:list[str], n:int)->str:
    '''
    Checks the  presence of n vertical planes for molecules with Cn axis
    :param point_group
    :type str
    :param n
    :type int

    :return "yes" (str) if the molecule has n vertical planes
    :return "no" (str) if not
    '''
    counter = 0

    for element in symmetry_list:
        mult, label = parse_symmetry_element(element)

        if label == "Sigma_v":
            counter += mult

    if counter == n:
        return "yes"
    return "no"