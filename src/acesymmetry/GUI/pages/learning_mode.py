from acesymmetry import Symmetry_Elements_Dico
from acesymmetry.Visual_Display import get_symmetry_set
from typing import Union

symmetry_set:set[str]=get_symmetry_set(point_group=)
symmetry_list:list[str]=list(symmetry_set)

def check_linearity(point_group:str)->str:
    '''
    Checks the linearity of the molecules (true only if it is Cinfv or Dinfv)

    :param point_group: point group of the molecule provided by the appropriate programm
    :type point_group: str

    :return "true" (str) if the molecule is linear
    :return "false" (str) if the molecule is not linear
    '''
    if point_group == "Cinfv" or point_group == "Dinfv":
        answer:str="true"
    else:
        answer:str="false"
    return answer

def check_inversion_centre()->str:
    '''
    Checks the presence of an inversion center

    :param None
    :type None

    :return "true" if the molecule has a pointgroup
    :return "false" if the molecule has not that symmetry element
    '''
    if i in symmetry_set:
        answer:str="true"
    else:
        answer:str="false"
    return answer

def check_main_axis_multiplicity(point_group:str)->str:
    '''
    Checks the presence of multiple main axes whose order is greater than 2
    (true only for Ih, I, Oh, O, Td, T)

    :param pointgroup: point group of the molecule provided by the appropriate program
    :type str

    
    :return "true" (str) if the molecule has multiple main axes whose order is greater than 2
    :return "false" (str) if not
    '''
    if point_group == "Ih" or point_group == "I" or point_group == "Oh"or point_group == O or point_group == "Td" or point_group == "T":
        answer:str="true"
    else:
        answer:str="false"
    return answer

def check_rotation_axis()->Union[tuple[str, int], str]:
    '''
    Checks the presence of rotation axis in the molecule

    :param None
    :type None

    :return "true" (str) if the molecule has rotation axis
    :return "false" (str) if not
    '''
    n_max:int = 0
    for element in symmetry_list:
        if element.startswith("C") == True:
            answer:str="true"
            break
    if answer == "true":
        for element in symmetry_list:
            n:int=str(element[1])
            if element.startswith("C") == True and n>n_max:
                n_max=n
        return {answer, n}
    else:
        answer:str="false"
        return answer

            

